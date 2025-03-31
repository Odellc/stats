
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess


#if we wanted to get the Beta zero and beta 1 by hand
def least_squares_method(x,y):
    x_mean=x.mean()
    y_mean=y.mean()
    beta1 = ((x-x_mean)*(y-y_mean)).sum(axis=0)/ ((x-x.mean())**2).sum(axis=0)
    beta0 = y_mean-(beta1*x_mean)
    return beta0, beta1


df = sm.datasets.macrodata.load().data

df = sm.add_constant(df, prepend=False)
df_mod = df[['realinv','realdpi','const']]

print('Data:')
print(df_mod)

ols_model = sm.OLS(df_mod['realdpi'], df_mod[['const', 'realinv']])

compiled_model = ols_model.fit()

print('Ordinary Least Squares model summary:')
print(compiled_model.summary())


beta0, beta1 = least_squares_method(df['realinv'], df['realdpi'])
print(f'Least Squares calculation by hand: beta0 = {beta0}, beta1 = {beta1}')


model_residuals = compiled_model.resid
fitted_value = compiled_model.fittedvalues
standardized_residuals = compiled_model.resid_pearson # Residuals, normalized to have unit variance.
sqrt_standardized_residuals = np.sqrt(np.abs(compiled_model.get_influence().resid_studentized_internal))

influence = compiled_model.get_influence()
leverage = influence.hat_matrix_diag
cooks_distance = compiled_model.get_influence().cooks_distance[0]

fig, ax = plt.subplots(2, 2, figsize=(10,8))
# Residuals vs. Fitted
ax[0, 0].set_xlabel('Fitted Values')
ax[0, 0].set_ylabel('Residuals')
ax[0, 0].set_title('Residuals vs. Fitted')
locally_weighted_line1 = lowess(model_residuals, fitted_value)
sns.scatterplot(x=fitted_value, y=model_residuals, ax=ax[0, 0])
ax[0, 0].axhline(y=0, color='grey', linestyle='--')
ax[0,0].plot(locally_weighted_line1[:,0], locally_weighted_line1[:,1], color = 'red')
# Normal Q-Q
ax[0, 1].set_title('Normal Q-Q')
sm.qqplot(model_residuals, fit=True, line='45',ax=ax[0, 1], c='blue')
# Scale-Location
ax[1, 0].set_xlabel('Fitted Values')
ax[1, 0].set_ylabel('Square Root of Standardized Residuals')
ax[1, 0].set_title('Scale-Location')
locally_weighted_line2 = lowess(sqrt_standardized_residuals, fitted_value)
sns.scatterplot(x=fitted_value, y=sqrt_standardized_residuals, ax=ax[1, 0])
ax[1,0].plot(locally_weighted_line2[:,0], locally_weighted_line2[:,1], color = 'red')
# Residual vs. Leverage Influence
ax[1, 1].set_xlabel('Leverage')
ax[1, 1].set_ylabel('Standardized Residuals')
ax[1, 1].set_title('Residuals vs. Leverage Influence')
locally_weighted_line3 = lowess(standardized_residuals, leverage)
sns.scatterplot(x=leverage, y=standardized_residuals, ax=ax[1, 1])
ax[1, 1].plot(locally_weighted_line3[:,0], locally_weighted_line3[:,1], color = 'red')
ax[1, 1].axhline(y=0, color='grey', linestyle='--')
ax[1, 1].axhline(3, color='orange', linestyle='--', label='Outlier Demarkation')
ax[1, 1].axhline(-3, color='orange', linestyle='--')
ax[1, 1].legend(loc='upper right')


leverages = []

for i in range(len(cooks_distance)):
    if cooks_distance[i] > 0.5:
        leverages.append(leverage[i])
        ax[1, 1].annotate(str(i) + " Cook's D > 0.5",xy=(leverage[i], standardized_residuals[i]))

if leverages:
    ax[1, 1].axvline(min(leverages), color='red', linestyle='--', label="Cook's Distance")
for i in range(len(standardized_residuals)):
    if standardized_residuals[i] > 3 or standardized_residuals[i] < -3:
        ax[1, 1].annotate(i,xy=(leverage[i], standardized_residuals[i]))

fig.tight_layout()



from statsmodels.graphics.tsaplots import plot_pacf
plot_pacf(compiled_model.resid, alpha=0.05, lags=50)

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
fig, ax = plt.subplots(2,3, figsize=(15,10))
plot_acf(df_mod['realdpi'], alpha=0.05, lags=50, ax=ax[0,0])
ax[0,0].set_title('Original ACF')
plot_pacf(df_mod['realdpi'], alpha=0.05, lags=50, ax=ax[0,1])
ax[0,1].set_title('Original PACF')
ax[0,2].set_title('Original Data')
ax[0,2].plot(df_mod['realdpi'])
plot_acf(np.diff(df_mod['realdpi'], n=1), alpha=0.05, lags=50, ax=ax[1,0])
ax[1,0].set_title('Once-Differenced ACF')
plot_pacf(np.diff(df_mod['realdpi'], n=1), alpha=0.05, lags=50, ax=ax[1,1])
ax[1,1].set_title('Once-Differenced PACF')
ax[1,2].set_title('Once-Differenced Data')
ax[1,2].plot(np.diff(df_mod['realdpi'], n=1))


ols_model_1diff = sm.OLS(np.diff(df_mod['realdpi'], n=1), pd.concat([df_mod['const'].iloc[:-1], pd.Series(np.diff(df_mod['realinv'], n=1))], axis=1))
compiled_model_1diff = ols_model_1diff.fit()

from sklearn.model_selection import train_test_split
train, test = train_test_split(df_mod, train_size=0.75, shuffle=True)

ols_model_train = sm.OLS(train['realdpi'], train[['const','realinv']])
compiled_model_train = ols_model_train.fit()
print(compiled_model_train.summary())

ols_model_test = sm.OLS(test['realdpi'], test[['const','realinv']])
compiled_model_test = ols_model_test.fit()
print(compiled_model_test.summary())

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(train['realdpi'], compiled_model_train.predict(train[['const','realinv']]))
print(f'mean absolute error: {mae}')

import numpy as np
errors = []
for i in range(len(train)):
    errors.append(abs(train['realdpi'].iloc[i] - train['realdpi'].mean()))
np.mean(errors)

mae_test = mean_absolute_error(test['realdpi'], compiled_model_train.predict(test[['const','realinv']]))
mae_test
#408.0253171549187

errors = []
for i in range(len(test)):
    errors.append(abs(test['realdpi'].iloc[i] - test['realdpi'].mean())), 
np.mean(errors)
#1945.5873125720873