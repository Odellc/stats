import matplotlib.pyplot as plt
from scipy.stats import skewnorm
from scipy.stats import mode
import numpy as np
from scipy import stats
from scipy.stats import skewnorm, norm
from scipy.stats import skew as skew_calc
from scipy.stats import norm
from scipy.stats import gennorm
from scipy.stats import kurtosis


label = ['model A', 'model B']
counts = [3, 5]
edu_label = ['BS', 'MS', 'PhD']
edu_counts = [10, 5, 2]

fig, ax = plt.subplots(1,2, figsize=(12,5))

ax[0].bar(label, counts)
ax[0].set_title('Counts of Machine Models')
ax[0].set_ylabel('Count')
ax[0].set_xlabel('Machine Models')

ax[1].bar(edu_label, edu_counts)
ax[1].set_title('Counts of Education Levels')
ax[1].set_ylabel('Count')
ax[1].set_xlabel('Education Level')


plt.show()


a = 4
x = skewnorm.rvs(a, size=3000) + 0.5
x = x[x > 0]
dfw_highs = [
    85, 87, 75, 88, 80, 86, 90, 94, 93, 92, 90, 92, 94,
    93, 97, 90, 95, 96, 96, 95, 92, 70, 79, 73, 88, 92,
    94, 93, 95, 76, 78, 86, 81, 95, 77, 71, 69, 88, 86,
    89, 84, 82, 77, 84, 81, 79, 75, 75, 91, 86, 86, 84,
    82, 68, 75, 78, 82, 83, 85]
fig, ax = plt.subplots(1,2, figsize=(12, 5))

ax[0].hist(x, bins=30)
ax[0].set_xlabel('Wait Time (hr)')
ax[0].set_ylabel('Frequency')
ax[0].set_title('Wait Times');

ax[1].hist(dfw_highs, bins=7)
ax[1].set_title('High Temperatures for DFW (4/2022-5/2022)')
ax[1].set_ylabel('Frequency')
ax[1].set_xlabel('Temperature (F)')

plt.show()

plt.hist(x, bins=30)
plt.gca().set(title='Wait Times', xlabel='Wait Time (hr)', ylabel='Frequency')
plt.show()

#mode
# m = mode([1,2,3,4,4,4,5,5])
# print(f"The mode is {m.mode[0]} with a count of {m.count[0]} instances"
# )
# The mode is 4 with a count of 3 instances


values = [85, 99, 70, 71, 86, 88, 94, 105]
median = np.median(values)
print(f"The median value is {median:.2f}")
# The median value is 87.00


values = [85, 99, 70, 71, 86, 88, 94]
mean = np.mean(values)
print(f"The mean value is {mean:.1f}")
# The mean value is 84.7


values = [85, 99, 70, 71, 86, 88, 94, 105]
max_value = np.max(values)
min_value = np.min(values)
range_ = max_value - min_value
print(f"The data have a range of {range_}"
      f" with max of {max_value}"
      f" and min of {min_value}")
# The data have a range of 35 with max of 105 and min of 70



values = [85, 99, 70, 71, 86, 88, 94]
quartiles = np.quantile(values, [0.25, 0.5, 0.75],
                        method="closest_observation")
print(f"The quartiles are Q1: {quartiles[0]}, Q2: {quartiles[1]}, Q3: {quartiles[2]}")
iqr = stats.iqr(values,interpolation='closest_observation')
print(f"The interquartile range is {iqr}")
# The quartiles are Q1: 71, Q2: 85, Q3: 88
# The interquartile range is 17


values = stats.norm.rvs(10, size=3000)
q1, q3 = np.quantile(values, [.25, .75], method='closest_observation')
iqr = stats.iqr(values,interpolation='closest_observation')
lower_fence = q1 - iqr * 1.5
upper_fence = q3 + iqr * 1.5
# may vary due to randomness in data generation
print(f"The lower fence is {lower_fence:.2f} and the upper fence is {upper_fence:.2f}")
# The lower fence is 7.36 and the upper fence is 12.67


values = [85, 99, 70, 71, 86, 88, 94]
variance = np.var(values)
standard_dev = np.std(values)
print(f"The variance is {variance:.2f} and the standard deviation is {standard_dev:.2f}")
# The variance is 101.06 and the standard deviation is 10.05



# generate data
skew_left = -skewnorm.rvs(10, size=3000) + 4
skew_right = skewnorm.rvs(10, size=3000) + 3
symmetric = norm.rvs(10, size=3000)
# calculate skewness
skew_left_value = skew_calc(skew_left)
skew_right_value = skew_calc(skew_right)
symmetric_value = skew_calc(symmetric)
# Output may vary some due to randomness of generated data
print(f"The skewness value of this left skewed distribution is {skew_left_value:.3f}")
print(f"The skewness value of this right skewed distribution is {skew_right_value:.3f}")
print(f"The skewness value of this symmetric distribution is {symmetric_value:.3f}")


# generate data
light_tailed = gennorm.rvs(5, size=3000)
symmetric = norm.rvs(10, size=3000)
heavy_tailed = gennorm.rvs(1, size=3000)
# calculate skewness
light_tailed_value = kurtosis(light_tailed)
heavy_tailed_value = kurtosis(heavy_tailed)
symmetric_value = kurtosis(symmetric)
# Output may vary some due to randomness of generated data
print(f"The kurtosis value of this light-tailed distribution is {light_tailed_value:.3f}")
print(f"The kurtosis value of this heavy_tailed distribution is {heavy_tailed_value:.3f}")
print(f"The kurtosis value of this normal distribution is {symmetric_value:.3f}")

import matplotlib.pyplot as plt, statsmodels.api as sm, pandas as pd, numpy as np, scipy.stats
df_duncan = sm.datasets.get_rdataset("Duncan","carData").data
df_duncan.loc[df_duncan['type'] == 'prof', 'type'] = 'professional'
df_duncan.loc[df_duncan['type'] == 'wc', 'type'] = 'white-collar'
df_duncan.loc[df_duncan['type'] == 'bc','type'] = 'blue-collar'
df_professional = df_duncan.loc[(df_duncan['type'] == 'professional')]
df_blue_collar = df_duncan.loc[(df_duncan['type'] == 'blue-collar')]


def plot_distributions(n_replicas, professional_sample, blue_collar_sample, professional_label, blue_collar_label, p=5):
    fig, ax = plt.subplots(2, 1, figsize=(10,8))
    ax[0].hist(professional_sample, alpha=.3, bins=20)
    ax[0].axvline(professional_sample.mean(),
                  color='black', linewidth=5)
    # sampling distribution mean
    ax[0].axvline(np.percentile(professional_sample, p/2.), color='red', linewidth=3, alpha=0.99)
    # 95% CI Lower limit (if bootstrapping)
    ax[0].axvline(np.percentile(professional_sample, 100-p/2.), color='red', linewidth=3, alpha=0.99)
    # 95% CI Upper Limit  (if bootstrapping)
    ax[0].title.set_text(str(professional_label) + "\nn = {} Resamples".format(n_replicas))
    ax[1].hist(blue_collar_sample, alpha=.3, bins=20)
    ax[1].axvline(blue_collar_sample.mean(), color='black', linewidth=5) # sampling distribution mean
    ax[1].axvline(np.percentile(blue_collar_sample, p/2.), color='red', linewidth=3, alpha=0.99)
    # 95% CI Lower limit (if bootstrapping)
    ax[1].axvline(np.percentile(blue_collar_sample, 100-p/2.), color='red', linewidth=3, alpha=0.99)
    # 95% CI Upper Limit (if bootstrapping)
    ax[1].title.set_text(str(blue_collar_label) + "\nn = {} Resamples".format(n_replicas))
    if n_replicas > 1:
        print("Lower confidence interval limit: ", np.percentile(round(professional_sample,4), p/2.))
        print("Upper confidence interval limit: ", np.percentile(round(professional_sample,4), 100-p/2.))
        print("Mean: ", round(professional_sample, 4).mean())
        print("Standard Error: ", round(professional_sample.std() / np.sqrt(n_replicas), 4) )
        print("Lower confidence interval limit: ", np.percentile(round(blue_collar_sample,4), p/2.))
        print("Upper confidence interval limit: ", np.percentile(round(blue_collar_sample,4), 100-p/2.))
        print("Mean: ", round(blue_collar_sample,4).mean())
        print("Standard Error: ", round(blue_collar_sample.std() / np.sqrt(n_replicas), 4) )
    else:
        print("At least two samples required to create the following statistics:\nConfidence Intervals\nMean\nStandard Error")
    
    plt.show()

n_replicas=0
plot_distributions(n_replicas=n_replicas, professional_sample=df_professional['income'],
                    blue_collar_sample=df_blue_collar['income'],
                    professional_label="Professional",
                    blue_collar_label="Blue Collar")


n_replicas=1000
professional_boostrap_means = pd.Series([df_professional.sample(frac=0.5, replace=True)['income'].mean() for i in range(n_replicas)])
blue_collar_boostrap_means = pd.Series([df_blue_collar.sample(frac=0.5, replace=True)['income'].mean() for i in range(n_replicas)])

plot_distributions(n_replicas=n_replicas, professional_sample=professional_boostrap_means,
                    blue_collar_sample=blue_collar_boostrap_means,
                    professional_label="Professional",
                    blue_collar_label="Blue Collar")


#SEM is the standard error of the mean
print(f'''Below is the SEM: Standard Error of the Mean: 
SEM for Professional: {scipy.stats.sem(professional_boostrap_means):.3f}
SEM for Blue Collar: {scipy.stats.sem(blue_collar_boostrap_means):.3f}
''')


#Correlation Coefficent Pearsons
df_prof_corr = df_professional.sample(n=10)
df_blue_corr = df_blue_collar.sample(n=10)

corr, _ = scipy.stats.pearsonr(df_prof_corr['income'], df_blue_corr['income'])

print(f"what comes out of scipy.stats.pearsonr: {scipy.stats.pearsonr(df_prof_corr['income'], df_blue_corr['income'])}")

print(f"Correlation for n=10 samples between pressional and blue collar income: {corr}")

#get correlation for high number of replications
professional_boostrap_means = pd.Series([df_prof_corr.sample(frac=0.5, replace =False).income.mean() for i in range(n_replicas)])
blue_collar_boostrap_means = pd.Series([df_blue_corr.sample(frac=0.5, replace =False).income.mean() for i in range(n_replicas)])

corr, _ = scipy.stats.pearsonr(professional_boostrap_means, blue_collar_boostrap_means)

print(f"Correlation for n={n_replicas} samples between pressional and blue collar income: {corr}")


#PERMUTATIONS
from itertools import permutations, combinations
# list of 10 people in the party
people = ['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10']
# all the ways that the 3 prizes are distributed
perm = permutations(people, 3)
list_perm = list(perm)
print(f"Permutations: There are {len(list_perm)} ways to distribute the prizes!")

print(f"Permutations: The 10 first ways to distribute the prizes: {list_perm[:10]} ")

comb = combinations(people, 3)
list_comb = list(comb)
print(f"Combinations: There are {len(list_comb)} ways to distribute the prizes!")

print(f"Combinations: The 10 first ways to distribute the prizes: {list_comb[:10]} ")



#testing purmutations

#create permutations testing function
def permutation_testing(A,B, n_iter=1000):
    differences = []
    P = np.array(A+B)
    original_mean = np.array(A).mean() - np.array(B).mean()

    for i in range(n_iter):
        np.random.shuffle(P) # Create a random permutation of P
        A_new = P[:len(A)] #have the same size as the original A
        B_new = P[-len(B):] # having the original length of B
        differences.append(A_new.mean() - B_new.mean())

    #calculate P value
    
    p_value = round(
        1-(float(
            len(
                np.where(
                    differences <= original_mean
                )[0]
            )
        )/float(
            n_iter
        ))
        ,2
    )
    return p_value

A = [3,5,4]
B = [43,41,56,78,54]
print(permutation_testing(A,B,n_iter=10000))

#Transformations
np.random.seed(42) # for reproducible purpose
# create a random data
df = np.random.beta(a=1, b=10, size = 10000)
df_log = np.log(df) #log transformation
df_sqrt = np.sqrt(df) # Square Root transformation
df_cbrt = np.cbrt(df) # Cube Root transformation
plt.figure(figsize = (10,10))
plt.subplot(2,2,1)
plt.hist(df)
plt.title("Original Data")
plt.subplot(2,2,2)
plt.hist(df_log)
plt.title("Log Transformation")
plt.subplot(2,2,3)
plt.hist(df_sqrt)
plt.title("Square Root Transformation")
plt.subplot(2,2,4)
plt.hist(df_cbrt)
plt.title("Cube Root Transformation")


plt.show()