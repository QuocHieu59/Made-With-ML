import json

import pytest
import utils

from madewithml import tune


@pytest.mark.training
def test_tune_models(dataset_loc):
    num_runs = 2
    experiment_name = utils.generate_experiment_name(prefix="test_tune")
    results = tune.tune_models(
        experiment_name=experiment_name,
        dataset_loc=dataset_loc,
        num_workers=1,
        cpu_per_worker=2,
        gpu_per_worker=0,
        num_runs=num_runs,
        num_epochs=2,
        num_samples=512,
        batch_size=8,
        results_fp=None,
    )
    utils.delete_experiment(experiment_name=experiment_name)
    assert len(results.get_dataframe()) == num_runs
