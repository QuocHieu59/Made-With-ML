#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$PWD
mkdir results

# Test data
export RESULTS_FILE=results/test_data_results.txt
export DATASET_LOC="https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/dataset.csv"
pytest --dataset-loc=$DATASET_LOC tests/data --verbose --disable-warnings > $RESULTS_FILE
cat $RESULTS_FILE

# Test code
export RESULTS_FILE=results/test_code_results.txt
python -m pytest tests/code --verbose --disable-warnings > $RESULTS_FILE
cat $RESULTS_FILE

# Train
export EXPERIMENT_NAME="llm"
export RESULTS_FILE=results/training_results.json
export DATASET_LOC="https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/dataset.csv"
python madewithml/train.py \
    --experiment-name "$EXPERIMENT_NAME" \
    --dataset-loc "$DATASET_LOC" \
    --num-workers 1 \
    --cpu-per-worker 2 \
    --gpu-per-worker 0 \
    --num-epochs 10 \
    --batch-size 8 \
    --results-fp $RESULTS_FILE

# Get and save run ID
# export RUN_ID=$(python -c "import os; from madewithml import utils; d = utils.load_dict(os.getenv('RESULTS_FILE')); print(d['run_id'])")
# export RUN_ID_FILE=results/run_id.txt
# echo $RUN_ID > $RUN_ID_FILE  # used for serving later

# Evaluate
export RESULTS_FILE=results/evaluation_results.json
export HOLDOUT_LOC="https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/holdout.csv"
python madewithml/evaluate.py \
    --dataset-loc $HOLDOUT_LOC \
    --results-fp $RESULTS_FILE

# Test model
RESULTS_FILE=results/test_model_results.txt
pytest tests/model --verbose --disable-warnings > $RESULTS_FILE
cat $RESULTS_FILE

# Save to S3
export MODEL_REGISTRY=$(python -c "from madewithml import config; print(config.MODEL_REGISTRY)")
aws s3 cp $MODEL_REGISTRY s3://madewithml/$GITHUB_USERNAME/mlflow/ --recursive
aws s3 cp results/ s3://madewithml/$GITHUB_USERNAME/results/ --recursive
