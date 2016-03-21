import glob
import gzip
import pandas as pd

def extract_df(filename):
	return pd.read_json(gzip.open(filename))

file_list = glob.glob('../challenge_data/*.gz')

data_frame = pd.DataFrame()

for filename in file_list:
	print 'Importing %s' % filename
	data_frame = pd.concat([data_frame, extract_df(filename)])
data_frame = data_frame.set_index(['name', 'last_update'])

