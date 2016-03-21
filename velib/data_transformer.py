# encoding: UTF-8

import logging
import pandas as pd
import numpy as np
import velib.utils as utils
from velib.velib_data_importer import VelibDataImporter
from velib.weather_data_importer import WeatherDataImporter
from velib.museum_data_crawler import MuseumDataCrawler
from velib.theatre_data_crawler import TheatreDataCrawler
from velib.market_data_crawler import MarketDataCrawler

class DataTransformer():

    def __init__(self, config, velib_data=None, filename="data/training.csv"):
        self.config = config
        self.init_logger()
        self.load_data(velib_data)
        self.merge_data()
        self.dump_csv(filename)

    def init_logger(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        if self.config.has_key('logging_level'):
            self.logger.setLevel(self.config['logging_level'])

    def min_dist(self,coordinate, coordinates):
        return min([utils.distance([coordinate, m_coor]) for m_coor in coordinates])

    ###########
    # LOADING #
    ###########

    def load_data(self, velib_data):
        self.load_external_data()
        self.load_velib_data(velib_data)

    def load_external_data(self):
        self.logger.info("Loading data")
        self.load_museum_data()
        self.load_theatre_data()
        self.load_market_data()
        self.load_weather_data()

    def load_velib_data(self, velib_data):
        self.logger.info("Loading velib data")
        if not velib_data:
            self.velib_data = VelibDataImporter(self.config)
            self.velib_data.init()
        else:
            self.velib_data = velib_data

    def load_museum_data(self):
        self.logger.info("Loading museum data")
        museum_data = MuseumDataCrawler(self.config)
        self.museum_coordinates = [row['fields'].get(
            museum_data.geo_attribute, [0,0]
        ) for i,row in museum_data.data_frame.iterrows()]

    def load_theatre_data(self):
        self.logger.info("Loading theatre data")
        theatre_data = TheatreDataCrawler(self.config)
        self.theatre_coordinates = [row['fields'].get(
            theatre_data.geo_attribute, [0,0]
        ) for i,row in theatre_data.data_frame.iterrows()]

    def load_market_data(self):
        self.logger.info("Loading market data")
        market_data = MarketDataCrawler(self.config)
        self.market_coordinates = [row['fields'].get(
            market_data.geo_attribute, [0,0]
        ) for i,row in market_data.data_frame.iterrows()]

    def load_weather_data(self):
        self.logger.info("Loading weather data")
        self.weather_data = WeatherDataImporter(self.config)
        self.weather_timestamps = np.array(self.weather_data.data_frame['timestamp'])
        self.weather_data.data_frame = self.weather_data.data_frame[[
            'conds',
            'icon',
            'rain',
            'snow',
            'thunder',
            'fog',
            'tempi',
            'tempm',
            'precipi',
            'precipm'
        ]]

    ###########
    # MERGING #
    ###########

    def merge_data(self):
        self.merge_museum_data()
        self.merge_theatre_data()
        self.merge_market_data()
        self.merge_weather_data()

    def merge_museum_data(self):
        self.logger.info("Merging museum data")
        museum_distances = self.velib_data.data_frame['position'].apply(
            lambda x: self.min_dist([x['lat'], x['lng']], self.museum_coordinates)
        )
        self.velib_data.data_frame['museum_distance'] = museum_distances

    def merge_theatre_data(self):
        self.logger.info("Merging theatre data")
        theatre_distances = self.velib_data.data_frame['position'].apply(
            lambda x: self.min_dist([x['lat'], x['lng']], self.theatre_coordinates)
            )
        self.velib_data.data_frame['theatre_distance'] = theatre_distances

    def merge_market_data(self):
        self.logger.info("Merging market data")
        market_distances = self.velib_data.data_frame['position'].apply(
            lambda x: self.min_dist([x['lat'], x['lng']], self.market_coordinates)
        )
        self.velib_data.data_frame['market_distance'] = market_distances

    def merge_weather_data(self):
        self.logger.info("Merging weather data")
        self.velib_data.data_frame['weather_index'] = self.velib_data.data_frame['timestamp'].apply(
            lambda x: np.abs((- self.weather_timestamps + (x))).argmin()
        )
        self.logger.info("Weather timestamp matching (long)")
        weather_data_interpolations = self.velib_data.data_frame['weather_index'].apply(
            lambda x: self.weather_data.data_frame.iloc[x]
        )
        self.velib_data.data_frame = pd.concat([self.velib_data.data_frame, weather_data_interpolations], axis=1)
        self.velib_data.data_frame = self.velib_data.data_frame.fillna(-9999.0)

    ###########
    # DUMPING #
    ###########

    def dump_csv(self, filename):
        self.velib_data.data_frame.to_csv(filename, encoding="utf-8", index=False)
