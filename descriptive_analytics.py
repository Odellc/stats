import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd


x = [8.0, 1, 2.5, 4, 28.0]
x_with_nan = [8.0, 1, 2.5, math.nan, 4, 28.0]
print(f'just x = {x}')
print(f'x with nan = {x_with_nan}')


y, y_with_nan = np.array(x), np.array(x_with_nan)
z, z_with_nan = pd.Series(x), pd.Series(x_with_nan)

print(f'just y = {y}')
print(f'y with nan = {y_with_nan}')

print(f'just z = {z}')
print(f'z with nan = {z_with_nan}')



#Simple Mean
mean_ = sum(x)/len(x)

print(f"calculated mean {mean_}")

#or built in version
mean_ = statistics.mean(x)
print(f"statistics library mean {mean_}")

#if you have a nan though it will return nan instead.
#example
 #or built in version
mean_ = statistics.mean(x_with_nan)
print(f"statistics library mean {mean_}")


#instead you can use np.nanmean()

mean_ = np.nanmean(x_with_nan)
print(f"np library np.nanmean {mean_}")

#For pandas you can use
mean_ = z.mean()
print(f"pandas mean {mean_}")

#pandas mean with nan is the same function
print(z_with_nan.mean())