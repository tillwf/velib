# encoding: UTF-8

import logging
import matplotlib.pyplot as plt
import numpy as np
import operator
import os
import pandas as pd
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from velib.data_transformer import DataTransformer
from velib.velib_data_crawler import VelibDataCrawler


class DataPrediction():

    split_proportion = 0.3
    nb_run = 1

    def __init__(self, config):
    	self.config = config
        self.init_logger()
        if not os.path.isfile("data/training.csv"):
            DataTransformer(config)
        self.global_error_rate = np.zeros(100)
        self.global_feature_importance = {}
        self.load_training_set()
        for i in range(0,self.nb_run):
            self.logger.info('Run n.%i' % i)
            self.run()
        self.plot_resutls()

    def run(self):
        self.create_train_test_set()

        self.train_classes = self.get_classes(self.current_training_set)
        self.test_classes = self.get_classes(self.testing_set)

        self.remove_unecessary_fields(self.current_training_set)
        self.remove_unecessary_fields(self.testing_set)

        # self.plot_error_rate_evolution(50,100,10)
        
        self.get_feature_importance()
        self.do_predictions()

    def init_logger(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        if self.config.has_key('logging_level'):
            self.logger.setLevel(self.config['logging_level'])

    ###########
    # LOADING #
    ###########    

    def load_training_set(self):
        self.logger.info("The file training.csv exists")
        self.training_set = pd.read_csv("data/training.csv")
        self.training_set = self.prepare_set(self.training_set)

    def create_train_test_set(self):
        rows = random.sample(self.training_set.index, int(len(self.training_set) * self.split_proportion))
        self.testing_set = self.training_set.ix[rows]
        self.current_training_set = self.training_set.drop(rows)

    def load_testing_set_from_recent_data(self):
        velib_data = VelibDataCrawler(self.config)
        velib_data.get_data()
        velib_data.init()
        dt = DataTransformer(self.config, velib_data, "data/testing.csv")
        self.testing_set = dt.velib_data.data_frame
        self.test_classes = self.get_classes(self.testing_set)
        self.testing_set = self.prepare_set(self.testing_set)
        self.current_training_set = self.current_training_set[list(set(self.current_training_set.columns).intersection(set(self.testing_set.columns)))]

    #############
    # PREPARING #
    #############

    def prepare_set(self, dataset):
        dataset = pd.get_dummies(dataset, columns=['conds','icon'])
        dataset = dataset.fillna(-9999.0)
        return dataset

    def remove_unecessary_fields(self, dataset):
        dataset.pop("timestamp")
        dataset.pop("position")
        dataset.pop("address")
        dataset.pop("name")
        dataset.pop("contract_name")
        dataset.pop('available_bike_stands')
        dataset.pop('status')
        dataset.pop('available_bikes')
        dataset.pop('weather_index')
        dataset.pop('last_update')

    def get_classes(self, dataset):
    	return 0 + (dataset['available_bike_stands'] > 0) & (dataset['status'] != 'CLOSED')

    #########
    # STATS #
    #########
                    
    def get_feature_importance(self):
        if not hasattr(self, 'clf'):
            self.train_classifier(80)
        importances = self.clf.feature_importances_
        std = np.std([tree.feature_importances_ for tree in self.clf.estimators_], axis=0)
        indices = np.argsort(importances)[::-1]
        dictionary = dict(zip(self.current_training_set.columns[indices], self.clf.feature_importances_[indices]))
        for key, value in dictionary.iteritems():
            self.global_feature_importance[key] = self.global_feature_importance.get(key, 0) + value

    def do_predictions(self):
        predictions = self.clf.predict(self.testing_set)
        if type(predictions[0]) == list:
            predictions = [p[self.clf.classes_.argmax()] for p in predictions]
        error_rate = []
        for i in range(0, 100):
            prediction_masks = np.array(predictions) < float(i)/100
            error_rate.append(float(sum(prediction_masks == self.test_classes)) / len(prediction_masks))

        self.global_error_rate = self.global_error_rate + np.array(error_rate)

    def plot_resutls(self):
        sorted_dictionary = sorted(self.global_feature_importance.items(), key=operator.itemgetter(1))
        self.logger.info(sorted_dictionary)
        plt.plot(range(0,100), self.global_error_rate / self.nb_run, label="Error based on confidence level")
        plt.show()        

    def train_classifier(self, n_estimators):
        self.clf = RandomForestRegressor(n_estimators=n_estimators, n_jobs=4, oob_score=True)
        self.clf = self.clf.fit(self.current_training_set, self.train_classes)

        
    # methods to compute error rate based on n_estimators
    def get_classifier_oob(self, n_estimators, n_jobs=4):
        self.logger.info("Getting oob for n_estimators = %s" % n_estimators)
        self.train_classifier(n_estimators)
        return 1 - self.clf.oob_score_

    def plot_error_rate_evolution(self, min_n_estimators, max_n_estimators, step):
        error_rate = []
        for i in range(min_n_estimators, max_n_estimators, step):
            error_rate.append((i, self.get_classifier_oob(i)))
        self.logger.info(error_rate)
        xs, ys = zip(*error_rate)
        plt.plot(xs, ys, label="YO")
        plt.show()
