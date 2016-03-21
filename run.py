# encoding: UTF-8

import logging
import yaml
from velib.data_prediction import DataPrediction

if __name__ == '__main__':
	
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        level='INFO'
    )

    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    logging.info(config)
    DataPrediction(config)
