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



#Principal Component Analysis

# Import libraries 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.preprocessing import scale 
from sklearn.linear_model import LinearRegression 
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error, root_mean_squared_error
from sklearn.decomposition import PCA 


#location of dataset  
url = "./Hitters.csv" 
#read in data 
data = pd.read_csv(url).dropna() # to simply the analysis, we drop all missing values 
print(data.head())


# create dummies variables 
dummies_variables = pd.get_dummies(data[['League', 'Division', 'NewLeague']])  
# create features and target 
target = data['Salary'] 
processed_data = data.drop(['Salary', 'League', 'Division', 'NewLeague'], axis=1).astype('float64') 

print(processed_data.head())

X = pd.concat([processed_data, dummies_variables[['League_N', 'Division_W', 'NewLeague_N']]], axis=1) 
print(X.head())
#scaled data - preprocessing 
X_scaled = scale(X) 
# train test split 
X_train, X_test, y_train, y_test = train_test_split(X_scaled, target, test_size=0.2, random_state=42) 

# First generate all the principal components 
pca = PCA() 
X_pc_train = pca.fit_transform(X_train) 
print(f"shape of principal component trained x: {X_pc_train.shape} ")

# Determining the best number of PCs to be used 
# The next step is to perform a 10-fold cross validation multiple linear regression 
# and choose the best number of PC to use by using RMSE (root mean squared error). 
 
# Define cross-validation folds 
cv = KFold(n_splits=10, shuffle=True, random_state=42) 
model = LinearRegression() 
rmse_score = [] 
# Calculate MSE score - based on 19 PCs 
for i in range(1, X_pc_train.shape[1]+1): 
    rmse = -cross_val_score(model, X_pc_train[:,:i], y_train, cv=cv, scoring='neg_root_mean_squared_error').mean() 
    rmse_score.append(rmse) 
# Plot results     
plt.plot(rmse_score, '-o') 
plt.xlabel('Number of principal components in regression') 
plt.ylabel('RMSE') 
plt.title('Salary') 
plt.xlim(xmin=-1) 
plt.xticks(np.arange(X_pc_train.shape[1]), np.arange(1, X_pc_train.shape[1]+1)) 
plt.show() 

#the best number of PC is 6 corresponding the lowest cross validation RMSE.  


# Train regression model on training data  
model = LinearRegression() 
model.fit(X_pc_train[:,:6], y_train) 
 
pcr_score_train = -cross_val_score(model, X_pc_train[:,:6], y_train, cv=cv,scoring='neg_root_mean_squared_error').mean() 
 
# Prediction with test data 
X_pc_test = pca.fit_transform(X_test)[:,:6] 
pred = model.predict(X_pc_test) 
pcr_score_test = mean_squared_error(y_test, pred) 
# pcr_score_test_with_false = mean_squared_error(y_test, pred, squared=False) #having squared in parameter is being depricated and is not just called root mean squared error
pcr_score_root_test = root_mean_squared_error(y_test, pred)
# print(f'pcr score test = {pcr_score_test} and pcr score test with false = {pcr_score_test_with_false} and pcr_score root = {pcr_score_root_test}')
print(f'pcr score test mean squared error is = {pcr_score_test} and pcr_score root mean squared error = {pcr_score_root_test}')
