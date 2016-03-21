# encoding: UTF-8

import logging
import pandas as pd
import requests

class Crawler():

    base_url = "http://opendata.paris.fr/api/records/1.0/search"
    params={}

    def __init__(self, config):
        self.config = config
        self.init_logger()
        self.get_data()

    def init_logger(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        if self.config.has_key('logging_level'):
            self.logger.setLevel(self.config['logging_level'])

    def get_data(self):
        records = requests.get(self.base_url, params=self.params).json()
        self.data_frame = pd.DataFrame(records['records'])