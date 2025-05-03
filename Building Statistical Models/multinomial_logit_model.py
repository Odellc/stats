# import packages 

import numpy as np 
import pandas as pd 
from sklearn import datasets 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import confusion_matrix, accuracy_score,  ConfusionMatrixDisplay 
import statsmodels.discrete.discrete_model as sm 
import matplotlib.pyplot as plt

# import Iris data 

iris = datasets.load_iris() 
print(iris.feature_names) 
print(iris.target_names) 

#create dataframe 

df = pd.DataFrame(iris.data, columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']) 
df['target'] = iris.target 
print(df.head())

#check for missing values
print(df.isna().sum())

#create train and test data

X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

#fit the model using sklearn
model_sk = LogisticRegression(solver= 'newton-cg', multi_class= 'multinomial')
model_sk.fit(X_train, y_train)

#using the trained model to predit y to compare to the y test
y_hat_sk = model_sk.predict(X_test)

#use map to apply round across all the predictions
pred_sk = list(map(round, y_hat_sk))

#confusion matrix
cm_sk = confusion_matrix(y_test, pred_sk)

display = ConfusionMatrixDisplay(cm_sk).plot()

plt.show()

#get accuracy
print(f'Test accuracy = {round(accuracy_score(y_test, pred_sk), 6)}')




#fit a model using the statsmodel
#in the fit the method bfgs stands for Broyden-Fletcher-Goldfarb_shanno
model_stat = sm.MNLogit(y_train, X_train).fit(method='bfgs')

'''
Other potential model fits solvers available are:
'newton’ for Newton-Raphson, ‘nm’ for Nelder-Mead
‘bfgs’ for Broyden-Fletcher-Goldfarb-Shanno (BFGS)
‘lbfgs’ for limited-memory BFGS with optional box constraints
‘powell’ for modified Powell’s method
‘cg’ for conjugate gradient
‘ncg’ for Newton-conjugate gradient
‘basinhopping’ for global basin-hopping solver
‘minimize’ for generic wrapper of scipy minimize (BFGS by default)

'''
model_stat.summary()

#predict the y to compare to y test based on the trained model
y_hat_stat = model_stat.predict(X_test)

pred_stat = np.asarray(y_hat_stat).argmax(1)


# confusion matrix 
cm_stat = confusion_matrix(y_test, pred_stat)  
display = ConfusionMatrixDisplay(cm_stat).plot() 
plt.show()

# Accuracy 
print(f'Test accuracy = {round(accuracy_score(y_test, pred_stat), 6)}') 
