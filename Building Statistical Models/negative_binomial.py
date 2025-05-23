
#Binomial Distribution, Bernoulli distribution, Negative Binomial Distribution. m
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import nbinom
import statsmodels.api as sm
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols as OLS
import statsmodels.api as sm
from statsmodels.genmod.families.family import NegativeBinomial
from sklearn.metrics import mean_squared_error as RMSE


n, p = 15, 0.5
mean, var, skew, kurt = nbinom.stats(n, p, moments='mvsk')
x = np.arange(nbinom.ppf(0.01, n, p),
              nbinom.ppf(0.99, n, p))


#Look to see if the variance is greater than the mean
print(x.var())

print(x.mean())

fig, ax = plt.subplots(1,1,figsize=(10,5))

sns.barplot(x=x.astype(int), y=nbinom.pmf(x, n, p), color='#17FF7D', alpha=0.5, ax=ax)
ax.set_title('Negative Binomial Distribution')
ax.set_xlabel('Count')
plt.setp(ax.get_yticklabels(), visible=False)
ax.tick_params(axis='y', which='both', length=0)
ax.set_ylabel('')
plt.show()


data = sm.datasets.fair.load().data
data = sm.add_constant(data, prepend=False)

print('Mean count of children per marriage: ', data['children'].mean())
print('Variance of the count of children per marriage: ', data['children'].var())


plt.hist(data['children'], bins=150)
plt.xlabel('Child Count')
plt.title('Child Count per Married Couple')
plt.savefig('./ChildrenDistribution.png', dpi=300, facecolor='w', bbox_inches = "tight")

'''
Here we use the log-likelihood method 'nb2', which is the variance derived from the mixture of Poisson distributions with Gamma mixing weights.
'''


y = round(data['children'])
X = data[['const','age','religious','yrs_married','educ','occupation','occupation_husb','affairs','rate_marriage']] 


pd.concat([X, y], axis=1).head().to_clipboard()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True)

print('''Here we have overdisperison of our target variable, which means we should use negative
       binomial regression instead of Poisson regression. Although it does not apply in this situation,
         it is useful to note that with negative binomial regression, target value order does 
      not matter as it does with Poisson regression.''')


print(np.unique(y))

np.array([0., 1., 2., 3., 4., 6.])


plt.hist(y, bins=50)
plt.xlabel('Child Count')
plt.title('Child Count per Married Couple')
plt.show()


df_train = pd.concat([X_train,y_train], axis=1)

poisson_training_results = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()

df_train['y_lambda'] = poisson_training_results.mu

df_train['y_auxiliary'] = df_train.apply(lambda x: ((x['children'] - x['y_lambda'])**2 - x['y_lambda']) / x['y_lambda'], axis=1)

aux_olsr_results = smf.ols('y_auxiliary ~ y_lambda - 1', df_train).fit()
print(aux_olsr_results.params)

print(f'numpy shape and average: {np.shape(poisson_training_results.mu)}')
print(f'y train shape = {np.shape(y_train)}')

poisson_training_results = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()

df_aux = pd.DataFrame({'children':y_train,
                       'y_lambda':poisson_training_results.mu})

df_train['y_lambda'] = poisson_training_results.mu

df_train['y_auxiliary'] = df_train.apply(lambda x: ((x['children'] - x['y_lambda'])**2 - x['y_lambda']) / x['y_lambda'], axis=1)

aux_olsr_results = smf.ols('y_auxiliary ~ y_lambda - 1', df_train).fit()
print(f'params = {aux_olsr_results.params}')

poisson_model = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()

df_aux = pd.DataFrame()
df_aux['y_mu_hat'] = poisson_model.mu
df_aux['children'] = y_train
df_aux['y_auxiliary'] = df_aux.apply(lambda x: ((x['children'] - x['y_mu_hat'])**2 - x['y_mu_hat']) / x['y_mu_hat'], axis=1)

ols_model = OLS('y_auxiliary ~ y_mu_hat - 1', df_aux).fit()
print(f'using params to check for over dispersian {ols_model.params}')

print(ols_model.summary)

negative_binomial_model = sm.GLM(y_train, X_train, family=NegativeBinomial(alpha=ols_model.params.values)).fit()
print(negative_binomial_model.summary())

print('Training Root Mean Squared Error: ', RMSE(y_train, negative_binomial_model.predict(X_train)) )
print('Testing Root Mean Squared Error: ', RMSE(y_test, negative_binomial_model.predict(X_test)))