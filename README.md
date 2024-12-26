<div align="center">
<h1><img width="30" src="https://madewithml.com/static/images/rounded_logo.png">&nbsp;<a href="https://madewithml.com/">Made With ML</a></h1>

</div>

<br>
<hr>

## Overview

<br>

- **Data version control**: Google drive to storage
- **MLflow**: Experiment tracking.
- **Ray tune**: Hyperparameter tuning.
- **Git**:Code version management.
- **Github actions**: CI/CD.

## Set up

### Cluster

We'll start by setting up our cluster with the environment and compute configurations.

<details>
  <summary>Local</summary><br>
  Your personal laptop (Window) will act as the cluster, where one CPU will be the head node and some of the remaining CPU will be the worker nodes.
</details>

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

<details>
  <summary>Local</summary><br>

```bash
python -m venv venv  # recommend using Python 3.10
venv\Scripts\activate
$env:PYTHONPATH = "$env:PYTHONPATH;$PWD"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
pre-commit install
pre-commit autoupdate
```

</details>
```
**Note**: Change the `--num-workers`, `--cpu-per-worker`, and `--gpu-per-worker` input argument values below based on your system's resources.
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

<details>
  <summary>Local</summary><br>

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

<details>
  <summary>Local</summary><br>

```bash
# Set up
python madewithml/serve.py
```

Once the application is running, we can use it via cURL, Python, Postmans

```bash
Ctrl + C  # shutdown server
```

</details>

### Test case

```bash
# Code
python -m pytest tests/code --verbose --disable-warnings >test_results/pytest_results_code.txt

# Data
pytest --dataset-loc=$env:DATASET_LOC tests/data --verbose --disable-warnings >test_results/pytest_results_data.txt

# Model
pytest tests/model --verbose --disable-warnings >test_results/pytest_results_model.txt

```

### CI/CD

Using GitHub Actions!

<div align="center">
  <img src="https://madewithml.com/static/images/mlops/cicd/cicd.png">
</div>

1. Create a new github branch to save our changes to and execute CI/CD workloads:

```bash
git remote set-url origin https://github.com/$GITHUB_USERNAME/Made-With-ML.git  # <-- CHANGE THIS to your username
git checkout -b dev
```

2. We'll start by adding the necessary credentials to the [`/settings/secrets/actions`](https://github.com/GokuMohandas/Made-With-ML/settings/secrets/actions) page of our GitHub repository.

```bash
export ANYSCALE_HOST=https://console.anyscale.com
export ANYSCALE_CLI_TOKEN=$YOUR_CLI_TOKEN  # retrieved from https://console.anyscale.com/o/madewithml/credentials
```

3. Now we can make changes to our code (not on `main` branch) and push them to GitHub. But in order to push our code to GitHub, we'll need to first authenticate with our credentials before pushing to our repository:

```bash
git config --global user.name $GITHUB_USERNAME  # <-- CHANGE THIS to your username
git config --global user.email you@example.com  # <-- CHANGE THIS to your email
git add .
git commit -m ""  # <-- CHANGE THIS to your message
git push origin dev
```

Now you will be prompted to enter your username and password (personal access token). Follow these steps to get personal access token: [New GitHub personal access token](https://github.com/settings/tokens/new) → Add a name → Toggle `repo` and `workflow` → Click `Generate token` (scroll down) → Copy the token and paste it when prompted for your password.

4. Now we can start a PR from this branch to our `main` branch and this will trigger the [workloads workflow](/.github/workflows/workloads.yaml). If the workflow (Anyscale Jobs) succeeds, this will produce comments with the training and evaluation results directly on the PR.

<div align="center">
  <img src="https://madewithml.com/static/images/mlops/cicd/comments.png">
</div>

5. If we like the results, we can merge the PR into the `main` branch. This will trigger the [serve workflow](/.github/workflows/serve.yaml) which will rollout our new service to production!
