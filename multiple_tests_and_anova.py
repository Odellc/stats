import requests
import re
from collections import namedtuple

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.weightstats import ttest_ind
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.oneway import anova_oneway
from statsmodels.formula.api import ols


#Get Data

data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
metadata_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.names"

# get metadata
metadata = requests.get(metadata_url)
metadata = metadata.content.decode("utf-8")
print(metadata)


variables = {}
lines = metadata.split('\n\n')[9].split('\n')
for line in lines:
    line = re.search(r"\d.\s([\s\w]+):\s+([()\s\w-]+)", line)
    variables[line.group(1).replace(' ', '_')] = line.group(2).replace(' ', '_')


print(f'Variables:{variables}')


names = list(variables.keys())

data = pd.read_csv(
    data_url,
    header=None,
    delim_whitespace=True,
    names=names,
)

print(data.head())

print(data.origin.value_counts())

# look at mean mpg for each origin
data[['origin','mpg']].groupby('origin').mean()

# get mpgs for each origin
mpg_1 = data[data.origin==1].sample(60, random_state=42).mpg
mpg_2 = data[data.origin==2].sample(60, random_state=42).mpg
mpg_3 = data[data.origin==3].sample(60, random_state=42).mpg


#Check Assumptions

sm.qqplot(mpg_1, line='s')
plt.title('QQ Plot for MPG from Origin 1')
plt.show()

sm.qqplot(mpg_2, line='s')
plt.title('QQ Plot for MPG from Origin 2')
plt.show()

sm.qqplot(mpg_3, line='s')
plt.title('QQ Plot for MPG from Origin 3')
plt.show()


#Check for equal variance

plt.boxplot([mpg_1, mpg_2, mpg_3])
plt.xlabel('origin')
plt.ylabel('mpg')
plt.title('MPG by Origin');

#hypothesis test

# store the values in a namedtuple
TestResult = namedtuple('TestResult', 'stat p_value df')


#perform individual tests

test_1v2 = TestResult(*ttest_ind(mpg_1, mpg_2))
test_1v3 = TestResult(*ttest_ind(mpg_1, mpg_3))
test_2v3 = TestResult(*ttest_ind(mpg_2, mpg_3))

pvalues = [result.p_value for result in [test_1v2, test_1v3, test_2v3]]
print(f"The p-values from the tests are {pvalues} (incorrect p-values)")

#correct p-values
reject, corrected_pvalues, *_ = multipletests(pvalues, alpha=0.01, method='bonferroni')
print(f"The bonferroni-corrected p-values are {corrected_pvalues}")

print("Test results:")
print(f"Reject difference in mean group 1, group 2: {reject[0]}")
print(f"Reject difference in mean group 1, group 3: {reject[1]}")
print(f"Reject difference in mean group 2, group 3: {reject[2]}")



for pvalue, bonf_pvalue in zip(pvalues, corrected_pvalues):
    print(f"The corrected value is {bonf_pvalue} and the individual pvalue multiplied by 3 is {pvalue*3}")



#ANOVA

anova = anova_oneway(data.mpg, data.origin, use_var='equal')
print(f'First ANOVA menthod: {anova}')



origin_lm = ols("mpg ~ C(origin)", data=data).fit()
anova = anova_lm(origin_lm)

print(f'Second ANOVA menthod: {anova}')

print(data[['model_year','mpg']].groupby('model_year').mean())


#Check for normality

model_years = data.model_year.unique()
mpgs_by_year = {}
for year in model_years:
    mpgs_by_year[year] = data[data.model_year==year].mpg.values

fig, axes = plt.subplots(ncols=4, nrows=4, sharex=True, figsize=(4*4, 4*3))
flat_axes = np.ravel(axes)
for year, ax in zip(list(mpgs_by_year.keys()), flat_axes):
    sm.qqplot(mpgs_by_year[year], line='s', ax=ax)
    ax.set_title(f'Year {year} QQ Plot')
for idx in range(len(mpgs_by_year.keys()), len(flat_axes)):
    flat_axes[idx].set_visible(False)
plt.tight_layout()


#check for equal variance

model_years = sorted(data.model_year.unique())
mpg_lists = []
for year in model_years:
    mpg_lists.append(data[data.model_year==year].mpg.values)
plt.boxplot(mpg_lists)

# note use_var='unequal' is the default of anova_oneway
anova = anova_oneway(data.mpg, data.model_year, use_var='unequal')
print(f'ANOVA results = {anova}')