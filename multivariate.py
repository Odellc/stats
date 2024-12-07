#from pydoc import help  # can type in the python console `help(name of function)` to get the documentation
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import stats
import matplotlib as mp


DISPLAY_MAX_ROWS = 20  # number of max rows to print for a DataFrame
pd.set_option('display.max_rows', DISPLAY_MAX_ROWS)


# print(os.curdir)


data = pd.read_csv("C:/Users/codel/OneDrive/Documents/wine.data", header=None)
data.columns = ["V"+str(i) for i in range(1, len(data.columns)+1)]# rename column names to be similar to R naming convention
data.V1 = data.V1.astype(str)
X = data.loc[:, "V2":]  # independent variables data
y = data.V1  # dependednt variable data

print(data)
print(f"This is y: {y}")


columns = ['Alcohol', 'Malic acid', 'Ash',
            'Alcalinity of ash', 'Magnesium',
            'Total phenols', 'Flavanoids', 'Nonflavanoid phenols',
            'Proanthocyanins', 'Color intensity', 'Hue',
            'OD280/OD315 of diluted wines', 'Proline'
        ]


scatterplot_variables = data.loc[:, "V2":"V6"]

pd.plotting.scatter_matrix(data.loc[:, "V2":"V6"], diagonal="kde")
plt.tight_layout()
plt.show()


sns.lmplot(data, x="V4", y="V5", hue="V1", fit_reg=False)
plt.show()


ax = data[["V2","V3","V4","V5","V6"]].plot()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5));
plt.show()


#print the summary statistics

for x in [np.mean, np.std]:
    print(x)
    print(X.apply(x))


#Look at mean and standard deviation for a particular y group
class2data = data[y=="2"]

print(f'Mean of variable 2 group on y group 2: {class2data.loc[:, "V2":].apply(np.mean)}')

print(f'Standard Deviation of variable 2 group on y group 2: {class2data.loc[:, "V2":].apply(np.std)}')


def print_means_and_STD_by_group(variables, groupvariables):
    data_groupby = variables.groupby(groupvariables)
    print(f'Means: {data_groupby.apply(np.mean)}') 
    print(f'STD: {data_groupby.apply(np.std)}')
    print(f'Sample Size: {data_groupby.apply(len)}')


print_means_and_STD_by_group(X, y)

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

print(f'Function for calc within group variance {calcWithinGroupsVariance(X.V2, y)}')

def calcBetweenGroupsVariance(variable, groupvariable):
    # find out how many values the group variable can take
    levels = sorted(set((groupvariable)))
    numlevels = len(levels)
    # calculate the overall grand mean:
    grandmean = np.mean(variable)
    # get the mean and standard deviation for each group:
    numtotal = 0
    denomtotal = 0
    for leveli in levels:
        levelidata = variable[groupvariable==leveli]
        levelilength = len(levelidata)
        # get the mean and standard deviation for group i:
        meani = np.mean(levelidata)
        sdi = np.std(levelidata)
        numi = levelilength * ((meani - grandmean)**2)
        denomi = levelilength
        numtotal = numtotal + numi
        denomtotal = denomtotal + denomi
    # calculate the between-groups variance
    Vb = numtotal / (numlevels - 1)
    return(Vb)