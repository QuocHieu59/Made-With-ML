import argparse
import os
from http import HTTPStatus
from typing import Dict

import ray
from fastapi import FastAPI
from ray import serve
from starlette.requests import Request
from fastapi.encoders import jsonable_encoder

from madewithml import evaluate, predict
from madewithml.config import MLFLOW_TRACKING_URI, mlflow

# Define application
app = FastAPI(
    title="Made With ML",
    description="Classify machine learning projects.",
    version="0.1",
)


@serve.deployment(num_replicas="1", ray_actor_options={"num_cpus": 6, "num_gpus": 0})
@serve.ingress(app)
class ModelDeployment:
    def __init__(self, threshold: int = 0.9):
        """Initialize the model."""
        self.threshold = threshold
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)  # so workers have access to model registry
        best_checkpoint = predict.get_best_checkpoint()
        self.predictor = predict.TorchPredictor.from_checkpoint(best_checkpoint)

    @app.get("/")
    def _index(self) -> Dict:
        """Health check."""
        response = {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": {},
        }
        return response

    # @app.get("/run_id/")
    # def _run_id(self) -> Dict:
    #     """Get the run ID."""
    #     return {"run_id": self.run_id}

    @app.post("/evaluate/")
    async def _evaluate(self, request: Request) -> Dict:
        data = await request.json()
        results = evaluate.evaluate(dataset_loc=data.get("dataset"))
        return {"results": results}

    @app.post("/predict/")
    async def _predict(self, request: Request):
        data = await request.json()
        sample_ds = ray.data.from_items([{"title": data.get("title", ""), "description": data.get("description", ""), "tag": ""}])
        results = predict.predict_proba(ds=sample_ds, predictor=self.predictor)
        print(results)
        # Apply custom logic
        for result in results:
            prob = result["probabilities"]
    # Chuyển đổi probabilities thành float nếu chúng là kiểu dữ liệu không phải float
            result["probabilities"] = {key: float(value) for key, value in prob.items()}
        encoded_results = jsonable_encoder(results)
        print(encoded_results)
        return {"results": encoded_results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("--run_id", help="run ID to use for serving.")
    parser.add_argument("--threshold", type=float, default=0.9, help="threshold for `other` class.")
    args = parser.parse_args()
    ray.init(runtime_env={"env_vars": {"GITHUB_USERNAME": os.environ["GITHUB_USERNAME"]}})
    serve.run(ModelDeployment.bind(threshold=args.threshold))
    import time
    try:
        while True:
            time.sleep(3600)  # Chờ trong 1 giờ, vòng lặp này sẽ giữ server chạy liên tục
    except KeyboardInterrupt:
        print("Shutting down server...")
