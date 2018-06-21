from matplotlib import pyplot
from pandas import read_csv
from pandas import datetime
from pandas.tools.plotting import autocorrelation_plot

def datetime_parser(x):
	return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S')

# series = read_csv('reportsv2/2.csv', header=0, parse_dates=[2], usecols=["Report Date", , "Total volume"], squeeze=True, date_parser=datetime_parser)
series = read_csv('reportsv2/2.csv',delimiter="|", usecols=["Report Date", "Total volume"], index_col=0, parse_dates=[0], date_parser=datetime_parser)
print(series.head())
series.plot()
pyplot.show() 