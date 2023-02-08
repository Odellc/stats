import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn import linear_model
matplotlib.style.use('ggplot')


#load the data
mtcars = pd.read_csv("../../Downloads/mtcars.csv")
print(mtcars)

mtcars.plot(kind="scatter", x="wt", y="mpg", figsize=(9,9),color="black" )
plt.show()


#Initialize model

regression_model = linear_model.LinearRegression()

#train the model using the mtcars data
regression_model.fit(X= pd.DataFrame(mtcars["wt"]),
y= mtcars["mpg"])

#Check trained model y-intercept
print(regression_model.intercept_)

#Check trained model coefficients
print(regression_model.coef_)


#Check the score
regression_model.score(pd.DataFrame(mtcars["wt"]),
y= mtcars["mpg"])

train_prediction = regression_model.predict(X = pd.DataFrame(mtcars['wt']))

#Acutal - prediction = residuals







