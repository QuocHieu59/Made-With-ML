import os
import subprocess
import sys

sys.path.append(".")

from madewithml.config import MODEL_REGISTRY  # NOQA: E402
from madewithml.serve import ModelDeployment  # NOQA: E402

# Copy from S3
github_username = os.environ.get("GITHUB_USERNAME")
subprocess.check_output(["aws", "s3", "cp", f"s3://madewithml/{github_username}/mlflow/", str(MODEL_REGISTRY), "--recursive"])
subprocess.check_output(["aws", "s3", "cp", f"s3://madewithml/{github_username}/results/", "./", "--recursive"])

# Entrypoint
entrypoint = ModelDeployment.bind(threshold=0.9)
