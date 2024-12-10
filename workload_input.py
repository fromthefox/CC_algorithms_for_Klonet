import configparser
import json

def config_ini(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def model_ini(model, dataset, weight_dtype):
    model_size_dict = {
        "llama-3-8B": 16.07
    }
    model_param_dict = {
        "llama-3-8B": 8029995008
    }
    dataset_dict = {
        "WuDao": 181
    }
    dtype = {
        "fp32": 4,
        "fp16": 2,
        "fp8": 1,
        "int4": 0.5
    }
    init_dict = {
        "model_size": model_size_dict[model],
        "model_params": model_param_dict[model],
        "dataset_size": dataset_dict[dataset],
        "dtype_size": dtype[weight_dtype]
    }
    return init_dict