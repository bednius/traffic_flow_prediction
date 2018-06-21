from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot

def datetime_parser(x):
	return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S')

series = read_csv('predictions/5_1.csv', header=0, parse_dates=[0], index_col=0, squeeze=True ,delimiter="|")
# series = read_csv('reportsv2/5.csv', delimiter="|", usecols=["Report Date", "Total volume"],header=0,index_col=0 ,  parse_dates=[0], date_parser=datetime_parser)


print(series.head())
series.plot()
pyplot.title("7th sensor")
pyplot.show()
# print( rows["predicted"] ,rows["expected"])
