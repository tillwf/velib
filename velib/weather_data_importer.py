# encoding: UTF-8
from importer import *
import json
import time


class WeatherDataImporter(Importer):
    """
    {
      "heatindexm": "-9999",
      "windchillm": "-999",
      "wdire": "West",
      "heatindexi": "-9999",
      "windchilli": "-999",
      "hail": "0",
      "wdird": "280",
      "wgusti": "-9999.0",
      "thunder": "0",
      "pressurei": "29.89",
      "snow": "0",
      "pressurem": "1012",
      "fog": "0",
      "vism": "-9999.0",
      "wgustm": "-9999.0",
      "conds": "Clear",
      "tornado": "0",
      "hum": "83",
      "tempi": "68.0",
      "tempm": "20.0",
      "dewptm": "17.0",
      "rain": "0",
      "dewpti": "62.6",
      "date": {
        "mday": "31",
        "hour": "02",
        "min": "00",
        "mon": "08",
        "pretty": "2:00 AM CEST on August 31, 2015",
        "year": "2015",
        "tzname": "Europe/Paris"
      },
      "visi": "-9999.0",
      "icon": "clear",
      "utcdate": {
        "mday": "31",
        "hour": "00",
        "min": "00",
        "mon": "08",
        "pretty": "12:00 AM GMT on August 31, 2015",
        "year": "2015",
        "tzname": "UTC"
      },
      "precipi": "-9999.00",
      "metar": "METAR LFPO 310000Z 28002KT CAVOK 20/17 Q1012 NOSIG",
      "precipm": "-9999.00",
      "wspdi": "2.3",
      "wspdm": "3.7"}
    """

    def __init__(self, config):
        Importer.__init__(self, config)
        self.files = glob.glob(self.config['weather_files_path'] + 'paris_weather*.gz')
        self.init_data_frame()

    def init_data_frame(self):
        """
        Init data frame with velib's data
        """
        self.data_frame = pd.DataFrame()

        for filename in self.files:
            logging.info('Importing %s' % filename)
            self.data_frame = pd.concat(
              [self.data_frame, self.extract_df(filename)]
            )
        self.data_frame = self.data_frame.T
        self.data_frame['timestamp'] = self.data_frame.apply(
          lambda x: self.construct_timestamp(x), axis=1
        )

    def extract_df(self, filename):
        """
        Convert data from json file to pandas data frame
        """
        data = pd.read_json(gzip.open(filename))['data']
        data_frame = pd.Series()
        for line in data:
            data_frame = pd.concat(
              [data_frame, pd.Series(line)]
            , axis=1)
        return data_frame

    def construct_timestamp(self, data):
      return int(time.mktime(datetime(
        int(data['date']['year']),
        int(data['date']['mon']),
        int(data['date']['mday']),
        int(data['date']['hour']),
        int(data['date']['min'])
      ).timetuple()))
