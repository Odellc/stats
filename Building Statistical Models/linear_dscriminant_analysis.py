import statsmodels.api as sm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

df_affairs = sm.datasets.fair.load().data

print(df_affairs.head())

total_count = df_affairs.shape[0]

positive_count = df_affairs.loc[df_affairs['affairs'] > 0].shape[0]

positive_pct = positive_count / total_count

negative_pct = 1- positive_pct

print("Class 1 Balance: {}%".format(round(positive_pct*100, 2)))
print("Class 2 Balance: {}%".format(round(negative_pct*100, 2)))

#if the balance is close to 90/10 it becomes a major issue
#  and upsampling or downsampling might be a possible option

#convert affairs into a binary classification problem
df_affairs['affairs'] = np.where(df_affairs['affairs']> 0, 1, 0)


#features to use
X=df_affairs[['rate_marriage','age','yrs_married','children','religious','educ','occupation','occupation_husb']]
y=df_affairs['affairs']

df_affairs_sd = pd.concat([X, y], axis=1)

# print(X)
# print(y)
# print(df_affairs_sd)

for col in df_affairs_sd.columns:
    if col not in ['affairs', 'occupation', 'occupation_husb']:
        print('Affairs = 0, Feature = {}, Standard Deviation = {}'.format(col, round(np.std(df_affairs_sd.loc[df_affairs['affairs']==0, col]),2)))
        print('Affairs = 1, Feature = {}, Standard Deviation = {}'.format(col, round(np.std(df_affairs_sd.loc[df_affairs['affairs']==1, col]),2)))

#drop husband occupation since it doesn't make a difference
pd.options.mode.chained_assignment = None

X['occupation'] = X['occupation'].map({1: 'Occupation_One',
                                       2: 'Occupation_Two',
                                       3: 'Occupation_Three',
                                       4: 'Occupation_Four',
                                       5: 'Occupation_Five',
                                       6: 'Occupation_Six'})

X = pd.get_dummies(X, columns=['occupation'])
X.drop('occupation_husb', axis=1, inplace=True)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.33, random_state=42)

X_train_sc = X_train.copy()
X_test_sc = X_test.copy()

ct = ColumnTransformer([
    ('', StandardScaler(), [
        'rate_marriage', 'age', 'yrs_married', 'children', 'religious', 'educ'
    ])
], remainder= 'passthrough'
)

X_train_sc = ct.fit_transform(X_train_sc)

ct = ColumnTransformer([
    ('', StandardScaler(), [
        'rate_marriage', 'age', 'yrs_married', 'children', 'religious', 'educ'
    ])
], remainder= 'passthrough'
)

X_test_sc = ct.fit_transform(X_test_sc)

print(X_train_sc)
print(X_test_sc)