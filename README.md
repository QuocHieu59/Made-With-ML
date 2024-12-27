<div align="center">
<h1><img width="30" src="https://madewithml.com/static/images/rounded_logo.png">&nbsp;<a href="https://madewithml.com/">MLOPS</a></h1>

</div>

<br>
<hr>

## Overview

<br>

- **Data version control**: Google drive to storage
- **MLflow**: Experiment tracking.
- **Ray tune**: Hyperparameter tuning.
- **Git**:Code version management.
- **Docker**: Application packaging
- **Github actions**: CI/CD.

## Set up

### Cluster

We'll start by setting up our cluster with the environment and compute configurations.
Your personal laptop (Window) will act as the cluster, where one CPU will be the head node and some of the remaining CPU will be the worker nodes.

### Git setup

```bash
git clone https://github.com/QuocHieu59/Made-With-ML.git .
```

### Credentials

```bash
touch .env
```

```bash
# Inside .env
GITHUB_USERNAME="CHANGE_THIS_TO_YOUR_USERNAME"  # ← CHANGE THIS
```

### Virtual environment

```bash
python -m venv venv  # recommend using Python 3.10
venv\Scripts\activate
$env:PYTHONPATH = "$env:PYTHONPATH;$PWD"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
pre-commit install
pre-commit autoupdate
```

```
**Note**: Change the `--num-workers`, `--cpu-per-worker`, and `--gpu-per-worker` input argument values below based on your system's resources.
```

## Notebook

Start by exploring the notebooks/madewithml.ipynb to interactively walkthrough the core machine learning workloads.

<div align="center">
  <img src="https://madewithml.com/static/images/mlops/systems-design/workloads.png">
</div>
  ```bash
  # Start notebook
  jupyter lab notebooks/madewithml.ipynb
```

### Tuning

```bash
$env:EXPERIMENT_NAME="llm"
$env:DATASET_LOC="https://raw.githubusercontent.com/QuocHieu59/Made-With-ML/master/datasets/dataset.csv"
python madewithml/tune.py --experiment-name $env:EXPERIMENT_NAME --dataset-loc $env:DATASET_LOC --num-runs 2 --num-workers 1 --cpu-per-worker 2 --gpu-per-worker 0 --num-epochs 10 --batch-size 32 --results-fp results/tuning_results.json
```

### Experiment tracking

```bash
$env:MODEL_REGISTRY=$(python -c "from madewithml import config; print(config.MODEL_REGISTRY)")
mlflow server -h 127.0.0.1 -p 8080 --backend-store-uri $MODEL_REGISTRY
(mlflow server -h 127.0.0.1 -p 8080 --backend-store-uri file:///D:/Me-hi/20241/Made-With-ML/efs/shared_storage/madewithml/QuocHieu59/mlflow)
```

Click to <a href="http://localhost:8080/" target="_blank">http://localhost:8080/</a> to view your MLflow dashboard.

### Evaluation

```bash
$env:HOLDOUT_LOC="https://raw.githubusercontent.com/QuocHieu59/Made-With-ML/master/datasets/holdout.csv"
python madewithml/evaluate.py --dataset-loc $env:HOLDOUT_LOC --results-fp results/evaluation_results.json
```

### Inference

```bash
python madewithml/predict.py predict --title "Transfer learning with transformers"  --description "Using transformers for transfer learning on text classification tasks."
```

### Serving

```bash
# Set up
python madewithml/serve.py
```

Once the application is running, we can use it via cURL, Python, Postmans

```bash
Ctrl + C  # shutdown server
```

### Test case

```bash

# Data
pytest --dataset-loc=$env:DATASET_LOC tests/data --verbose --disable-warnings >test_results/pytest_results_data.txt

# Model
pytest tests/model --verbose --disable-warnings >test_results/pytest_results_model.txt

# Code
python -m pytest tests/code --verbose --disable-warnings >test_results/pytest_results_code.txt
```

### CI/CD

Using GitHub Actions!

Test code when push change to github: \.github\workflows\test.yml
