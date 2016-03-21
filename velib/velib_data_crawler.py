# encoding: UTF-8
from crawler import Crawler
from datetime import datetime
import pandas as pd
import time

class VelibDataCrawler(Crawler):
    """
    {
      "status": "OPEN",
      "contract_name": "Paris",
      "name": "01010 - PONT NEUF",
      "bonus": false,
      "bike_stands": 25,
      "number": 1010,
      "last_update": 1442355200000,
      "available_bike_stands": 18,
      "banking": true,
      "available_bikes": 7,
      "address": "10 RUE BOUCHER - 75001 PARIS",
      "position": {
        "lat": 48.85946238924527,
        "lng": 2.344366128446111
      }
    }
    """

    params = {
    	"dataset": "stations-velib-disponibilites-en-temps-reel",
    	"facet":"status",
    	"facet":"contract_name",
    	"facet":"name",
    	"facet":"bonus",
    	"facet":"bike_stands",
    	"facet":"number",
    	"facet":"last_update",
    	"facet":"available_bike_stands",
    	"facet":"banking",
    	"facet":"available_bikes",
    	"facet":"address",
    	"facet":"position",
      "rows": 10000
    }

    def __init__(self, config):
        Crawler.__init__(self, config)

    def init(self):
      self.init_data_frame()
      self.clean_temporal_data()
      self.clean_position_data()
      self.clean_boolean_data()
      
    def init_data_frame(self):
        self.data_frame = self.data_frame['fields'].apply(lambda x: pd.Series(x))

    def clean_temporal_data(self):
        self.data_frame['timestamp'] = self.data_frame['last_update'].apply(lambda x: time.strptime(x, "%Y-%m-%dT%H:%M:%S+00:00"))
        self.data_frame['month'] = self.data_frame['timestamp'].apply(lambda x: x.tm_mon)
        self.data_frame['day'] = self.data_frame['timestamp'].apply(lambda x: x.tm_mday)
        self.data_frame['wday'] = self.data_frame['timestamp'].apply(lambda x: x.tm_wday)
        self.data_frame['hour'] = self.data_frame['timestamp'].apply(lambda x: x.tm_hour)
        self.data_frame['minute'] = self.data_frame['timestamp'].apply(lambda x: x.tm_hour)
        self.data_frame['timestamp'] = self.data_frame['timestamp'].apply(lambda x: time.mktime(x)  )

    def clean_position_data(self):
        self.data_frame['position'] = self.data_frame['position'].apply(lambda x: {'lat': x[0], 'lng': x[1]})

    def clean_boolean_data(self):
        self.data_frame['banking'] = self.data_frame['banking'].astype(bool)
        self.data_frame['bonus'] = self.data_frame['bonus'].astype(bool)
