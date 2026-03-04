import scipy
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
import statistics


#CDF = cumulative distribution function
print(f"Cumulative distrbution function: {round(scipy.stats.norm.cdf(1), 4)}")
#CDF = cumulative distribution function
print(f"Cumulative distrbution function: {round(scipy.stats.norm.cdf(1), 4)}")

iq = np.array([90, 78, 110, 110, 99, 115, 130, 100, 95, 93])

z_score = stats.zscore(iq)

#create dataframe

data_zscores = {
    "IQ score" : iq,
    "z_score" : z_score
}

IQ_zscore = pd.DataFrame(data_zscores)
print(IQ_zscore)


#calculate a z-score at x=95 and x=104
score_dict = {
    "_95" : 95,
    "_104" : 104
}

prob_dict = {}

for i, v in score_dict.items():
    mu = 98
    score = round((v-mu)/12, 2)
    print(f"score {score}")

    prob_dict.update({ i:stats.norm.cdf(score)})

prob = abs(prob_dict["_95"] - prob_dict["_104"])

#print the probability
print(f"The probability that the taken score between 95 and 104 is {round(prob*100,2)}%!")


# standard error
n= 4
sigma = 12
se = sigma/math.sqrt(n)
#calculate z scores at x=95 and 104
zscore_95 = round((95-98)/se,2)
zscore_104 = round((104-98)/se,2)
#calculate cdf and probability
cdf_95 = stats.norm.cdf(zscore_95)
cdf_104 = stats.norm.cdf(zscore_104)
prob = abs(cdf_95-cdf_104)
#print the probability
print(f"The probability that the taken score between 95 and 104 is {round(prob*100,2)}%!")

#This section is the probably of greater than the value to infinity
# where the cdf is from negative infinity to the numner

print(scipy.stats.norm.sf(abs(1)))
#find p-value
round(scipy.stats.norm.sf(abs(-2.67)),4)

#for a two tailed test
#find p-value for two-tailed test
scipy.stats.norm.sf(abs(2.67))*2

#critical region
alpha = 0.05
print(scipy.stats.norm.ppf(alpha))

import scipy.stats
alpha = 0.05 # level of significance
#find Z critical value for left-tailed test
print(f" The critical value is {scipy.stats.norm.ppf(alpha)}")
#find Z critical value for right-tailed test
print(f" The critical value is {scipy.stats.norm.ppf(1-alpha)}")
##find Z critical value for two-tailed test
print(f" The critical values are {-scipy.stats.norm.ppf(1-alpha/2)} and {scipy.stats.norm.ppf(1-alpha/2)}")


IQscores = [95,110, 105, 120, 125, 110, 98, 90, 99, 100,
            110, 112, 106, 92, 108, 97, 95, 99, 100, 100,
            103, 125, 122, 110, 112, 102, 92, 97, 89, 102]
IQmean = np.array(IQscores).mean()

print(IQmean)

n=30 #number of students
sigma =12 #population standard deviation
IQmean# IQ mean of 30 students after the training
mu = 98 # population mean
z = (IQmean-mu)/(sigma/math.sqrt(n))


#statsmodels.stats.weightstats.ztest(x1, x2=None, value=0, alternative='two-sided')

from statsmodels.stats.weightstats import ztest as ztest
#IQ scores after training sections
IQscores = [95,110, 105, 120, 125, 110, 98, 90, 99, 100, 
            110, 112, 106, 92, 108, 97, 95, 99, 100, 100,
            103, 125, 122, 110, 112, 102, 92, 97, 89, 102]
#perform one sample z-test
z_statistic, p_value = ztest(IQscores, value=98, alternative = 'larger')
print(f'''The test statistic is {z_statistic} and the
    corresponding p-value is {p_value}.''')


from statsmodels.stats.weightstats import ztest
#IQ score
A= [95,110, 105, 120, 125, 110, 98, 90, 99, 100, 
    110, 112, 106, 92, 108, 97, 95, 99, 100, 100, 
    103, 125, 122, 110, 112, 102, 92, 97, 89,102] #school A
B = [98, 90, 100, 93, 91, 79, 90, 100, 121, 89, 
     101, 98, 75, 90, 95, 99, 100, 120, 121, 95, 
     96, 89, 115, 99, 95, 121, 122, 98, 97, 97] # school B
#perform two- sample z-test
z_statistic, p_value = ztest(A, B, value=0, alternative = 'two-sided')
print(f"The test statistic is {z_statistic} and the corresponding p-value is {p_value}.")


#proportions testing
#statsmodels.stats.proportion.proportions_ztest(count, nobs, value=None, alternative='two-sided')


#import proportions_ztest function
from statsmodels.stats.proportion import proportions_ztest
count = 0.8*500
nobs = 500
value = 0.84
#perform one proportion two-tailed z-test
z_statistic, p_value = proportions_ztest(count, nobs, value, alternative = 'two-sided')
print(f'''The test statistic is {z_statistic} and the
    corresponding p-value is {p_value}.''')

p_1bar = 0.8
p_2bar = 0.7
n1 = 100.0
n2 = 100.0
p= (p_1bar*n1 + p_2bar*n2)/(n1+n2) # the total pooled proportion
z = (p_1bar-p_2bar)/math.sqrt(p*(1-p)*(1/n1+1/n2))
pval = scipy.stats.norm.sf(abs(z))*2
print(f"The test statistic is {z} and the p-value for two tailed test is {pval}.")

import statsmodels.api as sm
import math
df_prof = sm.datasets.get_rdataset("Salaries", "carData").data
df_prof_A = df_prof.loc[df_prof['discipline'] == 'A']
df_prof_B = df_prof.loc[df_prof['discipline'] == 'B']
def pooled_standard_deviation(dataset1, dataset2, column) -> float:
    pooledSD = math.sqrt(((len(dataset1) - 1)*(dataset1[column].std()**2)+(len(dataset2) - 1)*(dataset2[column].std()**2))/(len(dataset1) + len(dataset2) - 2))
    return pooledSD;

stdDeviation = pooled_standard_deviation( dataset1 = df_prof_A, dataset2=df_prof_B,column='salary')

from statsmodels.stats.power import NormalIndPower

effect = abs(df_prof_B['salary'].mean() - df_prof_A['salary'].mean() ) / stdDeviation
# The difference between two means divided by std if pooled 2-sample
alpha = 0.05
power = 0.8
ratio=1.19 # # of obs in sample 2 relative to sample 1
analysis = NormalIndPower()
result = analysis.solve_power(effect, power=power, nobs1=None, ratio=ratio, alpha=alpha, alternative='two-sided')
print('Sample Size Required in Sample 1: {:.3f}'.format( result*ratio)) # nobs1 is the sample size.
print('''Sample Size Required in Sample 2: {:.3f}'''.format(result)) # nobs2 is the sample size.

