import shutil
import requests
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.stats import poisson
import matplotlib.pyplot as plt
import statsmodels.api as sm 
from sklearn.metrics import (
    mean_absolute_percentage_error,
    mean_absolute_error
)

random_gen = np.random.default_rng(2022)


means = [12, 5, 2]

fig, ax = plt.subplots(3,1, figsize=(7, 15))

for i, mean in enumerate(means):
    # generate sample data
    r = poisson.rvs(mean, size=1000, random_state=random_gen)
    # plot the data
    labels, counts = np.unique(r, return_counts=True)
    ax[i].bar(np.arange(counts.size), counts, tick_label=labels)
    ax[i].set_ylabel('Counts')
    ax[i].set_xlabel(f'Poisson distribution with mean of {mean}')

plt.show()


# download the data
r = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip')
print(f"URL request status code: {r.status_code}")
with open('./Bike-Sharing-Dataset.zip', 'wb') as f:
    f.write(r.content)
shutil.unpack_archive('Bike-Sharing-Dataset.zip', 'Bike-Sharing-Dataset')


df = pd.read_csv('./Bike-Sharing-Dataset/day.csv')

# filter data down to one ISO year
df['isoweek'] = df.dteday.apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date().isocalendar()[1])
df['isoyear'] = df.dteday.apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date().isocalendar()[0])
df = df[(df.isoyear==2011)]

df.head()

df.tail()

# df.groupby('isoweek').mean()


week_index = df.groupby('isoweek').sum()['casual'].index
mean_weekly_cnts = df.groupby('isoweek').mean()['casual']
plt.bar(week_index, mean_weekly_cnts);
plt.xlabel('week')
plt.ylabel('count')
plt.title('mean weekly causal rental count')


# select variables
X = df.groupby('isoweek').mean()[['atemp', 'season', 'weathersit','hum','windspeed', 'holiday']]
# transform holiday variable as an indicator that a holiday occurs within that week
X['holiday'] = X['holiday'].apply(lambda x: 1 if x > 0.1 else 0)
# add a constant for the model
X = sm.add_constant(X)
# get the response variable
y = df.groupby('isoweek').mean()['casual']


fit_model = sm.Poisson(y, X).fit()
print(fit_model.summary())

preds = fit_model.predict(X)

print(f"The MAPE is {mean_absolute_percentage_error(y, preds) * 100:0.0f}% and the mean absolute error is {mean_absolute_error(y, preds):0.0f}")


plt.bar(np.arange(preds.size) + 1, preds)

week_index = df.groupby('isoweek').mean()['casual'].index
mean_weekly_cnts = df.groupby('isoweek').mean()['casual']
plt.plot(week_index, mean_weekly_cnts, label = 'actual');
plt.plot(np.arange(preds.size) + 1, preds, label='prediction')
plt.legend()

