from sklearn.metrics import mean_squared_error as MSE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import pandas as pd
from sklearn.datasets import fetch_california_housing


california_housing = fetch_california_housing()
df_california = pd.DataFrame(california_housing.data, columns = california_housing.feature_names)
df_california['PRICE'] = california_housing.target
df_california = sm.add_constant(df_california, prepend=False)


df_california.head().to_clipboard()

X = df_california.drop('PRICE', axis=1)
y = df_california['PRICE']

print(X.head())

sc = StandardScaler()
X_scaled = sc.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, shuffle=True)


#Ridge Regression
ols_model = sm.OLS(y_train, X_train)
compiled_model = ols_model.fit()
compiled_model_ridge = ols_model.fit_regularized(method='elastic_net', L1_wt=0, alpha=0.1,refit=True)

print('OLS Error: ', MSE(y_train, compiled_model.predict(X_train)) )
print('Ridge Regression Error: ', MSE(y_train, compiled_model_ridge.predict(X_train)))

print('OLS Error: ', MSE(y_test, compiled_model.predict(X_test)) )
print('Ridge Regression Error: ', MSE(y_test, compiled_model_ridge.predict(X_test)))

df_compare = pd.DataFrame({'Before Ridge Regression':compiled_model.params,
                           'After Ridge Regression':compiled_model_ridge.params})
df_compare.index=list(X.columns)

print(f'Table Ridge Regression: {df_compare.T}')



#Lasso

ols_model = sm.OLS(y_train, X_train)
compiled_model = ols_model.fit()
compiled_model_lasso = ols_model.fit_regularized(method='elastic_net', L1_wt=1, alpha=0.1,refit=True)

print('OLS Error: ', MSE(y_train, compiled_model.predict(X_train)) )
print('LASSO Regression Error: ', MSE(y_train, compiled_model_lasso.predict(X_train)))


print('OLS Error: ', MSE(y_test, compiled_model.predict(X_test)) )
print('LASSO Regression Error: ', MSE(y_test, compiled_model_lasso.predict(X_test)))

df_compare = pd.DataFrame({'Before LASSO Regression':compiled_model.params,
                           'After LASSO Regression':compiled_model_ridge.params})
df_compare.index=list(X.columns)

print(f'Table Lasso: {df_compare.T}')


#Elastic

ols_model = sm.OLS(y_train, X_train)
compiled_model = ols_model.fit()
compiled_model_elastic = ols_model.fit_regularized(method='elastic_net', L1_wt=0.5, alpha=8,refit=True)


print('OLS Error: ', MSE(y_train, compiled_model.predict(X_train)) )
print('Elastic Net Regression Error: ', MSE(y_train, compiled_model_elastic.predict(X_train)))


print('OLS Error: ', MSE(y_test, compiled_model.predict(X_test)) )
print('Elastic Net Regression Error: ', MSE(y_test, compiled_model_elastic.predict(X_test)))

df_compare = pd.DataFrame({'Before Elastic Net Regression':compiled_model.params,
                           'After Elastic Net Regression':compiled_model_ridge.params})
df_compare.index=list(X.columns)

print(f'Table Elastic Net: {df_compare.T}')