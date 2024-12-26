import sys
from pathlib import Path
import os

import mlflow

# Directories
ROOT_DIR = Path(__file__).parent.parent.absolute()

LOGS_DIR = Path(ROOT_DIR, "logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
EFS_DIR = Path(f"/efs/shared_storage/madewithml/{os.environ.get('GITHUB_USERNAME', '')}")
EFS_DIR = ROOT_DIR / EFS_DIR.relative_to(EFS_DIR.anchor)

try:
    Path(EFS_DIR).mkdir(parents=True, exist_ok=True)
except OSError:
    EFS_DIR = Path(ROOT_DIR, "efs")
    Path(EFS_DIR).mkdir(parents=True, exist_ok=True)
print(EFS_DIR)
print(ROOT_DIR)
file_path = EFS_DIR / "best_trial_path.txt"
with open(file_path , "r") as file:
    saved_path = file.read()
print(saved_path)