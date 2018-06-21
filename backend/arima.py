from pandas import read_csv
from datetime import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from sklearn.metrics import mean_squared_error


def datetime_parser(x):
	return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S')

series = read_csv('reportsv2/7.csv', delimiter="|", usecols=["Report Date", "Total volume"],header=0, index_col=0 ,  parse_dates=[0], date_parser=datetime_parser)
dates = read_csv('reportsv2/7.csv', delimiter="|", usecols=["Report Date", "Total volume"],header=0,   parse_dates=[0], date_parser=datetime_parser)


#filter null values
series = series[series["Total volume"] > 0]
dates = dates[dates["Total volume"] > 0]["Report Date"].tolist()

# print(series)

X = series.values
whole_size =int(len(X)) 
size = int(whole_size * 0.66)

dates = dates[size:whole_size]
train, test = X[0:size], X[size:whole_size]
# print (train)
# print (dates)
#extract total volumes for data
history = [ x for x in train]

# history = [[x[1]] for x in train]
# print(series["Report Date"][0].strftime('%Y-%m-%dT%H:%M:%S'))

print("Report Date|predictions|exepected")
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print(dates[t].strftime('%Y-%m-%dT%H:%M:%S'), '|%f|%f' % (yhat, obs),sep='')
    # print('predicted=%f, expected=%f' % (yhat[0], obs[0]))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot

# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator())
# pyplot.plot(dates,test, predictions)
# plt.gcf().autofmt_xdate()
# pyplot.plot(predictions, color='red')
# pyplot.show()

# dates =  [x.strftime('%Y-%m-%d %H:%M:%S') for x in dates]
test =  [ x[0] for x in test]
predictions = [ x[0] for x in predictions]
# print(dates)
# print (test)
# print (predictions)

data = {
    # 'dates': dates,
    'test':test,
    'predictions':predictions
}
df = pd.DataFrame( data, columns=[  'test', 'predictions'])
# df.groupby("dates").mean().plot()
df.plot()
# df.plot(xticks=dates)
# plt.xticks(dates)
plt.show()

# fig, ax = plt.subplots()
# ax.plot(df.index, df.values)
# ax.set_xticks(df.index)
# ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
# ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m"))
# _=plt.xticks(rotation=90)  
# plt.plot(predictions, color='red')
# plt.show()