import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn import datasets
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif


data = datasets.load_diabetes()

print(data['DESCR'])

y = data['target']
X = pd.DataFrame(
    data['data'], 
    columns=['age','sex','bmi','bp','s1','s2','s3','s4','s5','s6']
)
# this just converts sex back to a categorical variable
X.sex = X.sex.apply(lambda x: 1 if x > 0 else 0)
X = sm.add_constant(X)


max_vif = vif.max()
max_vif_idx = np.where(vif == max_vif)[0][0]
print(f"The max vif of {max_vif} is located at index {max_vif_idx}")