#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT License.
"""
Qlib provides two kinds of interfaces. 
(1) Users could define the Quant research workflow by a simple configuration.
(2) Qlib is designed in a modularized way and supports creating research workflow by code just like building blocks.

The interface of (1) is `qrun XXX.yaml`.  The interface of (2) is script like this, which nearly does the same thing as `qrun XXX.yaml`
"""
import qlib
from qlib.constant import REG_CN
from qlib.utils import init_instance_by_config, flatten_dict
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord, SigAnaRecord
from qlib.tests.data import GetData
from qlib.tests.config import CSI300_BENCH, CSI300_GBDT_TASK

from cfquant.instock.lib import utilsHelper

if __name__ == "__main__":

    root_uri = "F:/Project/Gits/ProjectData/qlibdata/"

    if utilsHelper.CheckIsHouse() == True:
        root_uri = "H:/Stock/ProjectData/qlibdata/"

    provider_uri = root_uri+"dump"

    # use default data
      # target_dir
    GetData().qlib_data(target_dir=provider_uri, region=REG_CN, exists_skip=True)
    qlib.init(provider_uri=provider_uri, region=REG_CN)

    market = "all"
    benchmark = "SH000300"

    ###################################
    # train model
    ###################################
    data_handler_config = {
        "start_time": "2008-01-01",
        "end_time": "2023-06-15",
        "fit_start_time": "2008-01-01",
        "fit_end_time": "2021-12-31",
        "instruments": market,
    }

    task = {
        "model": {
            "class": "GATs",
            "module_path": "qlib.contrib.model.pytorch_gats_ts",
            "kwargs": {
                "d_feat": 20,
                "hidden_size": 64,
                "num_layers": 2,
                "dropout": 0.7,
                "n_epochs": 200,
                "lr": 1e-4,
                "early_stop": 10,
                "metric": "loss",
                "loss": "mse",
                "base_model": "LSTM",
                "model_path": "benchmarks/LSTM/csi300_lstm_ts.pkl",
                "GPU": 0,
            },
        },
        "dataset": {
            "class": "DatasetH",
            "module_path": "qlib.data.dataset",
            "kwargs": {
                "handler": {
                    "class": "Alpha360",
                    "module_path": "qlib.contrib.data.handler",
                    "kwargs": data_handler_config,
                },
                "segments": {
                    "train": ("2008-01-01", "2021-12-31"),
                    "valid": ("2022-01-01", "2022-12-31"),
                    "test": ("2023-01-01", "2023-06-15"),
                },
            },
        },
    }

    # model initiaiton
    model = init_instance_by_config(task["model"])
    dataset = init_instance_by_config(task["dataset"])

    #model = init_instance_by_config(CSI300_GBDT_TASK["model"])
    #dataset = init_instance_by_config(CSI300_GBDT_TASK["dataset"])

    port_analysis_config = {
        "executor": {
            "class": "SimulatorExecutor",
            "module_path": "qlib.backtest.executor",
            "kwargs": {
                "time_per_step": "day",
                "generate_portfolio_metrics": True,
            },
        },
        "strategy": {
            "class": "TopkDropoutStrategy",
            "module_path": "qlib.contrib.strategy.signal_strategy",
            "kwargs": {
                "signal": (model, dataset),
                "topk": 50,
                "n_drop": 5,
            },
        },
        "backtest": {
            "start_time": "2023-01-01",
            "end_time": "2023-06-15",
            "account": 100000000,
            "benchmark": CSI300_BENCH,
            "exchange_kwargs": {
                "freq": "day",
                "limit_threshold": 0.095,
                "deal_price": "close",
                "open_cost": 0.0005,
                "close_cost": 0.0015,
                "min_cost": 5,
            },
        },
    }

    # NOTE: This line is optional
    # It demonstrates that the dataset can be used standalone.
    train = dataset.prepare("train")
    print(f"train:{len(train)}")
    train.to_csv(root_uri+f"h2o/train.csv", index=False)

    valid = dataset.prepare("valid")
    print(f"valid:{len(valid)}")
    valid.to_csv(root_uri+f"h2o/valid.csv", index=False)

    test = dataset.prepare("test")
    print(f"test:{len(test)}")
    test.to_csv(root_uri+f"h2o/test.csv", index=False)



