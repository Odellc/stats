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

print(f"np library np.nanmean {mean_}")


#instead you can use np.nanmean()

mean_ = np.nanmean(x_with_nan)
print(f"np library np.nanmean {mean_}")

#For pandas you can use
mean_ = z.mean()
print(f"pandas mean {mean_}")

#pandas mean with nan is the same function
print(z_with_nan.mean())

'''
The weighted mean or weighted average
'''

w = [0.1, 0.2, 0.3, 0.25, 0.15]

wmean = sum(w[i] * x[i] for i in range(len(x))) / sum(w)

print(f"Weighted mean with range: {wmean}")

#or with zip
wmean = sum(x_ * w_ for (x_, w_) in zip(x,w)) / sum(w)

print(f"Weighted mean with zip: {wmean}")

#harmonic Mean manually
hmean = len(x) / sum(1 / item for item in x)
print(f"Harmonic mean by hand: {hmean}")

#haronic mean using stats module
hmean = statistics.harmonic_mean(x)
print(f"Harmonic mean using stats module: {hmean}")


#geometric mean
gmean = 1
for item in x:
    gmean *= item
    print(f"test: {gmean}")

gmean **= 1 / len(x)

print(f"Geometric mean = {gmean}")

#Note has to be python 3.8 or higher for this
print(f"or us the stats model for geometri mean {statistics.geometric_mean(x)}")

def calcWithinGroupsVariance(variable, groupvariable):
    # find out how many values the group variable can take
    levels = sorted(set(groupvariable))
    numlevels = len(levels)
    # get the mean and standard deviation for each group:
    numtotal = 0
    denomtotal = 0
    for leveli in levels:
        levelidata = variable[groupvariable==leveli]
        levelilength = len(levelidata)
        # get the standard deviation for group i:
        sdi = np.std(levelidata)
        numi = (levelilength)*sdi**2
        denomi = levelilength
        numtotal = numtotal + numi
        denomtotal = denomtotal + denomi
    # calculate the within-groups variance
    Vw = numtotal / (denomtotal - numlevels)
    return Vw

