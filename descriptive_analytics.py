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

print(calcWithinGroupsVariance(variable, groupvariable))


def calcWithinGroupsCovariance(variable1, variable2, groupvariable):
    levels = sorted(set(groupvariable))
    numlevels = len(levels)
    Covw = 0.0
    # get the covariance of variable 1 and variable 2 for each group:
    for leveli in levels:
        levelidata1 = variable1[groupvariable==leveli]
        levelidata2 = variable2[groupvariable==leveli]
        mean1 = np.mean(levelidata1)
        mean2 = np.mean(levelidata2)
        levelilength = len(levelidata1)
        # get the covariance for this group:
        term1 = 0.0
        for levelidata1j, levelidata2j in zip(levelidata1, levelidata2):
            term1 += (levelidata1j - mean1)*(levelidata2j - mean2)
        Cov_groupi = term1 # covariance for this group
        Covw += Cov_groupi
    totallength = len(variable1)
    Covw /= totallength - numlevels
    return Covw

print(calcWithinGroupsCovariance(x.V8, x.V11, y))

corr = stats.pearsonr(x.V2, x.V3)
print("p-value:\t", corr[1])
print("cor:\t\t", corr[0])


corrmat = X.corr()
corrmat

sns.heatmap(corrmat, vmax=1., square=False).xaxis.tick_top()