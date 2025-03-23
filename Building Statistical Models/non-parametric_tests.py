# Permutation Test
import numpy as np
import scipy as sp
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os
import requests
from scipy import stats

# package for reading rda files
import pyreadr

import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import mannwhitneyu
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

from statsmodels.stats.gof import chisquare
from scipy.stats import chi2_contingency
from scipy.stats import chi2




# it is customary to use a random generator for
# reproducibility when randomness is required.
# See more here:
# https://numpy.org/doc/stable/reference/random/generator.html
random_gen = np.random.default_rng(42)

low_temp = np.array([0, 0, 0, 0, 0, 1, 1])
high_temp = np.array([1, 2, 3, 1])

#Show that data does not meet parametric assumptions


fig, axes = plt.subplots(2,2, figsize=(12,12))
sm.qqplot(low_temp, ax=axes[0,0], line='s')
axes[0,0].set_title("QQ Plot of Low Temp Points")
axes[0,1].hist(low_temp)
axes[0,1].set_title("Histogram of Low Temp Points")
sm.qqplot(high_temp, ax=axes[1,0], line='s')
axes[1,0].set_title("QQ Plot of High Temp Points")
axes[1,1].hist(high_temp)
axes[1,1].set_title("Histogram of High Temp Points")
plt.show()

#From the plots above, it appears to be unlikely that the data meets the assumptions of the t-test.
#Since this dataset is small, it is a good canditiate for the permutuation test.

# some permutations
permutations = []
for _ in range(5):
    all_samples = np.concatenate([low_temp, high_temp])
    permutations.append(random_gen.permutation(all_samples))
print(permutations)

'''
The function `permutation_test` requires that we provide the function for calculating the statistic.
This is the `statistic_function` which calculates the difference between the two means of the two groups.
'''
def statistic_function(set_one, set_two):
    return np.mean(set_one) - np.mean(set_two)
perm_result = sp.stats.permutation_test(
    (low_temp, high_temp),
    statistic_function, 
    random_state=random_gen,
)
perm_result.pvalue
observed_diff_mean =  low_temp.mean() - high_temp.mean()

print(f"The observed difference in mean of the two distributions is {observed_diff_mean:.1f}")


plt.figure(figsize=(7,5))
plt.hist(perm_result.null_distribution, bins=30);
plt.vlines(observed_diff_mean, 0, 100, colors='red');
plt.text(observed_diff_mean-0.1, 20,'Observed Difference',rotation=90);
plt.title("Distribution of Differences in Means from Permutation");
plt.show()

# Permutation Growth

'''As mentioned in the chapter, the permutations of a dataset grow quickly as the size of a dataset increases.
The following table shows how quickly the number of permutations increases as dataset size increases.
The column `sizes` represents number of samples in the dataset and
`permutations` is the number of permutations that can be arranged with the sample size.'''


sizes = np.arange(1, 13)
permutations = sp.special.factorial(sizes)
df = pd.DataFrame()
df['sizes'] = sizes
df['permutations'] = permutations
print(df)


#Rank - Sum test


# download and unpack the data
data_file = "iq.rda"
if not os.path.exists(data_file):
    r = requests.get("https://github.com/OpenIntroStat/openintro/raw/master/data/gpa_iq.rda")
    with open(data_file, 'wb') as f:
        f.write(r.content)
data = pyreadr.read_r('iq.rda')
data = data["gpa_iq"]


print(data.head())

print(data.size)


lower_bound, upper_bound = np.percentile(data.concept.values, [10, 90], method='closest_observation')

higher_score_iqs = data[data.concept >= upper_bound].iq
higher_score_iqs_mean = np.mean(higher_score_iqs)

lower_score_iqs = data[data.concept <= lower_bound].iq
lower_score_iqs_mean = np.mean(lower_score_iqs)

print(f"The lower 10% score is {lower_bound} and the upper 10% score is {upper_bound}")
print(f"The mean lower 10% score is {lower_score_iqs_mean} and the mean upper 10% score is {higher_score_iqs_mean:0.1f}")



plt.hist(lower_score_iqs, label='lower_iq')
plt.vlines(lower_score_iqs_mean, 0, 4, colors='red')
plt.text(lower_score_iqs_mean - 2, 2.5,'Lower IQ Mean',rotation=90)
plt.hist(higher_score_iqs, label='higher_iq')
plt.vlines(higher_score_iqs_mean, 0, 4, colors='red')
plt.text(higher_score_iqs_mean - 2, 2.5,'Higher IQ Mean',rotation=90)
plt.legend()
plt.title("Distribution of Scores from Lower and Higher IQ Students")
plt.show()


#Check normality assumptions
print('Check for normality')

fig, ax = plt.subplots(1,2, figsize=(10,5))
sm.qqplot(higher_score_iqs, line='s', ax=ax[0])
ax[1].hist(higher_score_iqs)
fig.suptitle("Scores from Students with Top 10% IQs")
plt.show()


fig, ax = plt.subplots(1,2, figsize=(10,5))
sm.qqplot(lower_score_iqs, line='s', ax=ax[0])
ax[1].hist(lower_score_iqs)
fig.suptitle("Scores from Students with Bottom 10% IQs")
plt.show()


#Check for equal variance
print('Check for equal variance')

plt.hist(lower_score_iqs, label='lower_iq')
plt.hist(higher_score_iqs, label='higher_iq')
plt.legend()
plt.title("Distribution of Scores from Lower and Higher IQ Students")

print('higher score iqs:')
print(higher_score_iqs)
print('lower score iqs:')
print(lower_score_iqs)


print('Mann whitney test p_value:')
print(mannwhitneyu(higher_score_iqs, lower_score_iqs).pvalue)



#Signed Rank Test
print('Signed Rank Test')

# label L group with 0 and H group with 1
group_labels = np.concatenate([np.zeros_like(lower_score_iqs), np.ones_like(higher_score_iqs)])
# combine all samples
all_samples = np.concatenate([lower_score_iqs, higher_score_iqs])


# create dataframe from samples and group labels
df = pd.DataFrame(
    {
        'samples' : all_samples,
        'group' : group_labels,
    }
)
# sort records by sample value
df = df.sort_values('samples').reset_index(drop=True)
# rank values from 1
df['raw_rank'] = df.index.values + 1
# correct ranks where ties occur
df['rank_'] = df.samples.apply(lambda x: df[df.samples==x].raw_rank.mean() if df.samples.value_counts().loc[x] > 1 else df[df.samples==x].raw_rank.iloc[0])


print(df.head())

# get the test statistic
T = df[df.group==0].rank_.sum()
print(T)

# get term Mean(T)
mean_T = df.rank_.mean() * df[df.group==0].rank_.size
mean_T

# get term STDEV(T)
def pooled_size(n1, n2):
    return np.sqrt(n1 * n2 / (n1 + n2))

ps = pooled_size(df[df.group==0].rank_.size, df[df.group==1].rank_.size)

sd_T = df.rank_.std() * ps

# get approx Z
Z = (T - mean_T)/sd_T
print(f'Z statistic: {Z}')

# get p-value
print(f'pvalue = {norm.cdf(Z) * 2}')

before_treatment   = np.array([37, 14, 22, 12, 24, 35, 35, 51,39]) 
after_treatment = np.array([38,17, 19, 7, 15, 25, 24, 38,19]) 
 
# Signed Rank Test 
print(f'signed rank test example output for wilcoxon model: {stats.wilcoxon(before_treatment, after_treatment, alternative = 'greater')}') 


group1 = [8, 13, 13, 15, 12, 10, 6, 15, 13, 9] 
group2 = [16, 17, 14, 14, 15, 12, 9, 12, 11, 9] 
group3 = [7, 8, 9, 9, 4, 15, 13, 9, 11, 9] 
#Kruskal-Wallis Test  
print(f'Example output for Kruskal-Wallis test: {stats.kruskal(group1, group2, group3)}')


#Chi Squared Distribution
print('Chi Squared Distribution')



x = np.random.chisquare(7, size=1000000)
ax = sns.kdeplot(x=x, fill=True, color='#17FF7D')
ax.set(ylabel=None)
ax.set_title('Chi-Square Distribution')
ax.set_xlabel('x')
plt.show()

x = np.random.chisquare(1, size=1000000)
ax = sns.kdeplot(x=x, fill=True, color='#17FF7D')
ax.set(ylabel=None)
ax.set_title('Chi-Square Distribution')
ax.set_xlabel('x')
plt.show()

chi_square_stat, p_value = chisquare(f_obs=[45, 30, 15], f_exp=[30, 30, 30])
chi_square_critical_value = chi2.ppf(1-.05, df=2)
print(f'Chi-Square Test Statistic: {chi_square_stat}')
print(f'Chi-Square Critical Value: {chi_square_critical_value}')
print(f'P-Value: {p_value}')


chi_square_stat, p_value = chisquare(f_obs=[45, 30], f_exp=[37.5, 37.5])
chi_square_critical_value = chi2.ppf(1-.05, df=2)
print(f'Chi-Square Test Statistic: {chi_square_stat}')
print(f'Chi-Square Critical Value: {chi_square_critical_value}')
print(f'P-Value: {p_value}')


#Chi-Square Test of Independence

observed_frequencies = np.array([[1429, 1235], [1216934, 22663]])
chi_Square_test_statistic, p_value, degrees_of_freedom, expected_frequencies = chi2_contingency(observed_frequencies)
chi_square_critical_value = chi2.ppf(1-.05, df=degrees_of_freedom)

print(f'Chi-Square Test Statistic: {chi_Square_test_statistic}')
print(f'Chi-Square Critical Value: {chi_square_critical_value}')
print(f'P-Value: {p_value}')

#Spearman's Rank Correlation Coefficient



df_scores = pd.DataFrame({'Judge A':[1, 3, 5, 7, 8, 3, 9],
                          'Judge B':[2, 5, 3, 9, 6, 1, 7]})

correlation, p_value = spearmanr(df_scores['Judge A'], df_scores['Judge B'])

print(f'Spearman Correlation Coefficient: {correlation}')
print(f'P-Value: {p_value}')

print('DataFrame Scores')
print(df_scores)
