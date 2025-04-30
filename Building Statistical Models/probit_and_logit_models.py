import pandas as pd 
import statsmodels.formula.api as smf 
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay

# create gpa train data 
train = pd.DataFrame({'Admitted': [1, 1, 1,1, 1, 0, 1, 1, 0, 1,1,1, 1,1,0, 1, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 1,1,1,1, 0], 
                    'GPA': [2.8, 3.3, 3.7, 3.7, 3.7, 3.3, 3.7, 3, 1.7, 3.6, 3.3, 4, 3.2, 3.4, 2.8, 4, 1.5, 2.7, 2.3, 2.3, 2.7, 2.2, 3.3,3.3, 4, 2.3, 3.6, 3.4, 4, 3.7, 2.3], 
                    'Exp': [8, 6, 5, 5, 6, 3, 4, 2, 1, 5, 5, 3, 6,5, 4, 4, 4, 1, 1, 2, 2, 2, 1, 4, 4, 4, 5, 2, 4, 6, 3]}) 
train.head() 

# create a testing dataset for this model. 
test = pd.DataFrame({'Admitted': [1, 0, 1, 0, 1], 
                    'GPA': [2.9, 2.4, 3.8, 3, 3.3], 
                    'Exp': [9, 1, 6, 1,4 ]}) 
test.head() 

# We will use Logit from statsmodels.  


#fit logistic regression 
model = smf.logit('Admitted ~ GPA + Exp', data=train)

model = model.fit()

print(model.summary())

#confusion matrix and accuracy scores

# X_test and y_test
X_test = test[['GPA', 'Exp']]
y_test = test['Admitted']

#
y_hat = model.predict(X_test)
pred = list(map(round, y_hat))

#confusion matrix
cm = confusion_matrix(y_test, pred)
display = ConfusionMatrixDisplay(cm).plot()
plt.show()

#Accuracy
print('Test accuracy =', accuracy_score(y_test, pred))