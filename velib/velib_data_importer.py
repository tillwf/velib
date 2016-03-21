# encoding: UTF-

from importer import *
from datetime import datetime

class VelibDataImporter(Importer):

    def __init__(self, config):
        Importer.__init__(self, config)
        self.files = glob.glob(self.config['velib_files_path'] + 'station*.gz')

    def init(self):
        self.init_data_frame()
        self.clean_temporal_data()

    def init_data_frame(self):
        """
        Init data frame with velib's data
        """
        self.data_frame = pd.DataFrame()

        for filename in self.files:
            logging.info('Importing %s' % filename)
            self.data_frame = pd.concat([self.data_frame, self.extract_df(filename)])

    def extract_df(self, filename):
        """
        Convert data from json file to pandas data frame
        """
        return pd.read_json(gzip.open(filename))

    def clean_temporal_data(self):
        self.data_frame['timestamp'] = self.data_frame['last_update'].apply(lambda x: float(x)/1000)
        self.data_frame['month'] = self.data_frame['timestamp'].apply(lambda x: datetime.fromtimestamp(x).month)
        self.data_frame['day'] = self.data_frame['timestamp'].apply(lambda x: datetime.fromtimestamp(x).day)
        self.data_frame['wday'] = self.data_frame['timestamp'].apply(lambda x: datetime.fromtimestamp(x).weekday())
        self.data_frame['hour'] = self.data_frame['timestamp'].apply(lambda x: datetime.fromtimestamp(x).hour)
        self.data_frame['minute'] = self.data_frame['timestamp'].apply(lambda x: datetime.fromtimestamp(x).minute)

