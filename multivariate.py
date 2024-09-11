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


print(os.curdir)


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


