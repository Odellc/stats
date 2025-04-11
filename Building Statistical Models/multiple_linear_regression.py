import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn import datasets
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error as mape
from sklearn.metrics import make_scorer
from sklearn.feature_selection import RFECV
import seaborn as sns


data = datasets.load_diabetes()

print(data['DESCR'])

y = data['target']
X = pd.DataFrame(
    data['data'], 
    columns=['age','sex','bmi','bp','s1','s2','s3','s4','s5','s6']
)

all_data = X[::]
all_data['target'] = y

#this just converts sex back to a categorical variable
X.sex = X.sex.apply(lambda x: 1 if x > 0 else 0)
X = sm.add_constant(X)


#Variance inflation Factor
vif_data = pd.DataFrame()
vif_data["VIF"] = [vif(X.values, i) for i in range(X.shape[1])]
print(vif_data)

X_2 = X.drop(columns=['s1'], inplace=False)

vif_data_2 = pd.DataFrame()
vif_data_2["VIF"] = [vif(X_2.values, i) for i in range(X_2.shape[1])]
print(vif_data_2)
# max_vif = vif.max()``
# max_vif_idx = np.where(vif == max_vif)[0][0]
# print(f"The max vif of {max_vif} is located at index {max_vif_idx}")


model = sm.OLS(y, X)

fit = model.fit()

print(fit.summary())


# Evaluate Model Fit

fig, ax = plt.subplots(5, 2, figsize=(10, 20))

for idx, col in enumerate(X.columns[1:]):
    # if idx == 8:
    #     break
    ax[idx//2, idx%2].scatter(X[col], y)
    ax[idx//2, idx%2].set_xlabel(col)
    ax[idx//2, idx%2].set_ylabel('Response')

    print("idx = {} with idx//2 = {} and idx%2 = {}".format(idx, idx//2, idx%2))

plt.show()

# Feature selection

fig, ax = plt.subplots(1, figsize=(9,9))
mask = np.triu(np.ones_like(all_data.corr(), dtype=np.bool))
heatmap = sns.heatmap(
    all_data.corr(), 
    vmin=-1, 
    vmax=1, 
    annot=True, 
    cmap='coolwarm', 
    mask=mask, 
    ax=ax
)

plt.show()


heatmap = sns.heatmap(
    all_data.corr()[['target']].sort_values(by='target', ascending=False).drop('target'),
    vmin=-1,
    vmax=1,
    annot=True,
    cmap='coolwarm')
heatmap.set_title(
    'Features Correlated with Response',
    fontdict={'fontsize':18},
    pad=16
);
fig = heatmap.get_figure()

plt.show()

print(all_data.corr())
print(all_data.corr()[['target']])