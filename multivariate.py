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
import sys


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


print(f'Function for calc between group variance {calcBetweenGroupsVariance(X.V2, y)}')
      
print(f'Seperation achieved by V2: {calcBetweenGroupsVariance(X.V2, y) / calcWithinGroupsVariance(X.V2, y)}')


def calcSeparations(variables, groupvariable):
    # calculate the separation for each variable
    for variablename in variables:
        variablei = variables[variablename]
        Vw = calcWithinGroupsVariance(variablei, groupvariable)
        Vb = calcBetweenGroupsVariance(variablei, groupvariable)
        sep = Vb/Vw
        print("variable", variablename, "Vw=", Vw, "Vb=", Vb, "separation=", sep)

calcSeparations(X, y)


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

print(calcWithinGroupsCovariance(X.V8, X.V11, y))

corr = stats.pearsonr(X.V2, X.V3)
print("p-value:\t", corr[1])
print("cor:\t\t", corr[0])


corrmat = X.corr()
corrmat

sns.heatmap(corrmat, vmax=1., square=False).xaxis.tick_top()
plt.show()

def hinton(matrix, max_weight=None, ax=None):
    """Draw Hinton diagram for visualizing a weight matrix."""
    ax = ax if ax is not None else plt.gca()

    if not max_weight:
        max_weight = 2**np.ceil(np.log(np.abs(matrix).max())/np.log(2))

    ax.patch.set_facecolor('lightgray')
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for (x, y), w in np.ndenumerate(matrix):
        color = 'red' if w > 0 else 'blue'
        size = np.sqrt(np.abs(w))
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    nticks = matrix.shape[0]
    ax.xaxis.tick_top()
    ax.set_xticks(range(nticks))
    ax.set_xticklabels(list(matrix.columns), rotation=90)
    ax.set_yticks(range(nticks))
    ax.set_yticklabels(matrix.columns)
    ax.grid(False)

    ax.autoscale_view()
    ax.invert_yaxis()
    plt.show()

hinton(corrmat)


def test(matrix):
    print(f'matrix is {matrix}')
    print("-----------------------------------")
    count = 0
    for (x,y), w in np.ndenumerate(matrix):
        print(f"x is {x}, y is {y}")
        print(f"w is {w}")
        count += 1
        if count >3:
            sys.exit()


def mosthighlycorrelated(mydataframe, numtoreport):
    '''
    The arguments of the function are the variables that you want 
    to calculate the correlations for, and the number of top 
    correlation coefficients to print out 
    (for example, you can tell it to print out the largest 10 
    correlation coefficients, or the largest 20).
    '''
    #find the correlations
    cormatrix = mydataframe.corr()
    #set the correlations on the diagonal to zero
    #to stop them from being reported as the highest ones
    cormatrix *= np.tri(*cormatrix.values.shape, k=-1).T
    # find the top n correlations
    cormatrix = cormatrix.stack()
    cormatrix = cormatrix.reindex(cormatrix.abs().sort_values(ascending=False).index).reset_index()
    # assign human-friendly names
    cormatrix.columns = ["FirstVariable", "SecondVariable", "Correlation"]
    return cormatrix.head(numtoreport)

print(f'most highly correlationd= {mosthighlycorrelated(X, 10)}')


#Standardize and scale the data
#setup for a mean of 0 and variance of 1

standardisedX = scale(X)

standardisedX = pd.DataFrame(standardisedX, index=X.index, columns=X.columns)

standardisedX.apply(np.mean)
print(f"standardized outputs: {standardisedX}")


pca = PCA().fit(standardisedX)

def pca_summary(pca, standardised_data, out=True):
    names = ["PC"+str(i) for i in range(1, len(pca.explained_variance_ratio_)+1)]
    a = list(np.std(pca.transform(standardised_data), axis=0))
    b = list(pca.explained_variance_ratio_)
    c = [np.sum(pca.explained_variance_ratio_[:i]) for i in range(1, len(pca.explained_variance_ratio_)+1)]
    columns = pd.MultiIndex.from_tuples([("sdev", "Standard deviation"), ("varprop", "Proportion of Variance"), ("cumprop", "Cumulative Proportion")])
    summary = pd.DataFrame(zip(a, b, c), index=names, columns=columns)
    if out:
        print("Importance of components:")
        print(summary)
    return summary

pca_summary(pca, standardisedX)

