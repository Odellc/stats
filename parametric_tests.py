import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import levene
import numpy as np
import pandas as pd
import pylab
import statistics
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.weightstats import ttest_ind as ttest 


mu, sigma = 0, 1

normally_distributed = np.random.normal(mu, sigma, 1000)

print(f'''
      {stats.kstest(normally_distributed, stats.norm.cdf)}
        Kolmogrogov-smirnov test for normality''')

print(f'''exponential distributed data for ks-test 
      {stats.kstest(np.exp(normally_distributed), stats.norm.cdf)}''')


mu, sigma = 100, 2
normally_distributed = np.random.normal(mu, sigma, 1000)
normally_distributed_scaled = (normally_distributed - normally_distributed.mean()) / normally_distributed.std()

print(f'''standardized distributed data for ks-test 
      {stats.kstest(normally_distributed_scaled, stats.norm.cdf)}''')



#caustion of which standard deviation to use
iq = np.array([90, 78, 110, 110, 99, 115, 130, 100, 95, 93])

print(np.std(iq, ddof=1)) #sample
print(np.std(iq)) #population
print(statistics.stdev([90, 78, 110, 110, 99, 115, 130, 100, 95, 93])) #sample
print(statistics.pstdev([90, 78, 110, 110, 99, 115, 130, 100, 95, 93])) #population
print(stats.tstd(iq, ddof=1)) #sample
print(stats.tstd(iq, ddof=0)) #population
print(stats.tstd(iq)) #sample

#Anderson test for normality

def anderson_test(data):
    data = np.array(data)
    test_statistic, critical_values, significance_levels = stats.anderson(normally_distributed, dist='norm')
    df_anderson = pd.DataFrame({'Test Statistic':np.repeat(test_statistic, len(critical_values)), 'Critical Value':critical_values, 'Significance Level': significance_levels})
    df_anderson.loc[df_anderson['Test Statistic'] >= df_anderson['Critical Value'], 'Normally Distributed'] = 'No'
    df_anderson.loc[df_anderson['Test Statistic'] <df_anderson['Critical Value'], 'Normally Distributed'] = 'Yes'
    return df_anderson;


mu, sigma = 19, 1.7
normally_distributed = np.random.normal(mu, sigma, 1000)
print(anderson_test(normally_distributed))



not_normally_distributed = np.exp(normally_distributed)
anderson_test(not_normally_distributed)


#stats.shapiro test for normality
print(f'''Shapiro-wilks test for normality normal distribution:
      {stats.shapiro(normally_distributed)}''')

not_normally_distributed = np.exp(normally_distributed)

#stats.shapiro test for normality
print(f'''Shapiro-wilks test for normality exponential
        {stats.shapiro(not_normally_distributed)}''')


mu, sigma = 0, 1.1

independent_samples = np.random.normal(mu, sigma, 1000)
correlated_samples = np.linspace(-np.pi, np.pi, num=1000)


fig, ax = plt.subplots(1,2, figsize=(10,5))
ax[0].plot(correlated_samples, np.sin(correlated_samples))
ax[0].set_title('Durbin Watson = {}'.format(durbin_watson(correlated_samples)))
ax[1].plot(independent_samples)
ax[1].set_title('Durbin Watson = {}'.format(durbin_watson(independent_samples)))

plt.show()



#Levene's test for equality of variances

np.random.seed(26)
mu1, sigma1, mu2, sigma2, mu3, sigma3 = 0, 0.9, 0, 1.1, 0, 2

distro1, distro2, distro3, = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

distro1['x'] = np.random.normal(mu1, sigma1, 100)
distro2['x'] = np.random.normal(mu2, sigma2, 100)
distro3['x'] = np.random.normal(mu3, sigma3, 100)

f_statistic, p_value = levene( distro1['x'], distro2['x'], distro3['x'])

if p_value <= 0.05:
    print(f'The distributions do not have homogenous vairance. p-value = {round(p_value, 4)}, F-statistic = {round(f_statistic, 4)}')
else:
    print(f'The distributions have homogenous variance. P-value = {round(p_value, 4)}, F-statistic = {round(f_statistic, 4)}')


def f_test(inputA, inputB):
   group1 = np.array(inputA)
   group2 = np.array(inputB)

   if np.var(group1) > np.var(group2):
      f_statistic = np.var(group1) / np.var(group2)
      numeratorDegreesOfFreedom = group1.shape[0] - 1
      denominatorDegreesOfFreedom = group2.shape[0] - 1

   else:
      f_statistic = np.var(group2)/np.var(group1)
      numeratorDegreesOfFreedom = group2.shape[0] - 1
      denominatorDegreesOfFreedom = group1.shape[0] - 1

   p_value = 1 - stats.f.cdf(f_statistic,numeratorDegreesOfFreedom, denominatorDegreesOfFreedom)
   
   if p_value <= 0.05:
      print(f'The distributions do not have homogenous variance. P-value = {round(p_value, 4)}, F-statistic = {round(f_statistic, 4)}')
   else:
      print(f'The distributions have homogenous variance. P-value = {round(p_value, 4)}, F-statistic = {round(f_statistic, 4)}')

f_test(distro3['x'], distro1['x'])

f_test(distro2['x'], distro1['x'])

f_test(distro3['x'], distro2['x'])


#T-tests

# creating normal distribution
x = np.linspace(-5, 5, 1000) #create 1000 point from -5 to 5
y = stats.norm.pdf(x) # create probability density for each point x - normal distribution
# creating Student t distributions for 2 sample sizes n =3 and n =15
degree_freedom1 = 2
t_dis1 = stats.t.pdf(x, degree_freedom1)
degree_freedom2 = 15
t_dis2 = stats.t.pdf(x, degree_freedom2)

plt.figure(figsize=(10,5))
plt.plot(x, y, label='normal')
plt.plot(x, t_dis1, label='3 samples')
plt.plot(x, t_dis2, label='16 samples')
plt.xlabel('value')
plt.ylabel('density')
plt.legend()
plt.grid(True)

plt.show()



#t-test for means

#one-sample t-test
print(f'finding p-value on the value of student t distribution syntax is (one-tailed): scipy.stats.t.sf(abs(x), df), two-tailed is scipy.stats.t.sf(abs(t), df)*2')


print(f"example result left-tailed: {round(stats.t.sf(abs(1.9), df=14),4)}")

print('syntax to get the critical value: scipy.stats.t.ppf(q, df), q=level of significance')

alpha = 0.05 # level of significance
df= 15 # degree of freedom
#find t critical value for left-tailed test
print(f" The critical value is {stats.t.ppf(q= alpha, df =df)}")
#find t critical value for right-tailed test
print(f" The critical value is {stats.t.ppf(q= 1-alpha, df =df)}")
##find t critical value for two-tailed test
print(f" The critical values are {-stats.t.ppf(q= 1-alpha/2, df =df)} and {stats.t.ppf(q= 1-alpha/2, df =df)}")

IQscores = [113, 107, 106, 115, 103, 103, 107, 102,
            108, 107, 104, 104, 99, 102, 102, 105,
            109, 97, 109, 103, 103, 100, 97, 107,
            116, 117, 105, 107, 104, 107]

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.hist(IQscores)
plt.title('Histogram of IQ scores ')

plt.subplot(1,2,2)
stats.probplot(np.array(IQscores), dist="norm", plot=pylab)
plt.title('Q-Q plot of IQ scores')
pylab.show()
plt.show()


#perform one sample t-test
t_statistic, p_value = stats.ttest_1samp(IQscores, popmean =100, axis=0, alternative='greater')
print(f"The test statistic is {t_statistic} and the corresponding p-value is {p_value}.")

IQmean = np.array(IQscores).mean() # sample mean
IQsd = np.array(IQscores).std() # sample standard deviation
sample_size = len(np.array(IQscores)) # sample size
df = sample_size-1 # degree of freedom
alpha = 0.05 # level of significance
t_crit = stats.t.ppf(q=1-alpha, df =df) # critical
confidence_interval = (IQmean-IQsd*t_crit/np.sqrt(sample_size), 
IQmean+IQsd*t_crit/np.sqrt(sample_size))


#Two Sample Mean Test

# Let us look at the IQ scores between 2 high schools, A and B.

IQscoresA = [113, 107, 106, 115, 103, 103, 107, 102, 108, 107,  
            104, 104, 99, 102, 102, 105, 109,  97, 109, 103, 
            103,  100,  97, 107,116, 117, 105, 107,104, 107] 
 
IQscoresB = [102, 108, 110, 101, 98, 98, 97,102, 102, 103,  
             100, 99, 97,97, 94, 100, 104,  98, 92, 104, 
            98,  95,  92, 111,102, 112, 100, 103,103, 100] 

plt.figure(figsize=(10,5))
plt.subplot(2,2,1)
plt.hist(IQscoresA)
plt.title('Histogram of IQ scores - School A ')

plt.subplot(2,2,2)
stats.probplot(np.array(IQscoresA), dist="norm", plot=pylab)
plt.title('Q-Q plot of IQ scores - School A')


plt.subplot(2,2,3)
plt.hist(IQscoresB)
plt.title('Histogram of IQ scores - School B ')

plt.subplot(2,2,4)
stats.probplot(np.array(IQscoresB), dist="norm", plot=pylab)
plt.title('Q-Q plot of IQ scores - School B')

# set the spacing between subplots
plt.subplots_adjust(left=0.2,
                    bottom=0.2,
                    right=0.8,
                    top=0.8,
                    wspace=0.5,
                    hspace=0.5)
plt.show()

# F-test 

IQscoresA = np.array(IQscoresA) 
IQscoresB = np.array(IQscoresB) 
f = np.var(IQscoresA, ddof=1)/np.var(IQscoresB, ddof=1) # F statistic 
dfA = IQscoresA.size-1 #degrees of freedom A 
dfB = IQscoresB.size-1 #degrees of freedom B  
p = 1-stats.f.cdf(f, dfA, dfB) #p-value  


t_statistic, p_value, degree_freedom = ttest(IQscoresA, IQscoresB, alternative='two-sided', usevar ='pooled')

print(f'f-test results for t statistics and p-value{t_statistic, p_value}')

#Two-sample t-test: Welch’s t-test
sample1 = np.array([2,3,4,2,3,4,2,3,5,8,7,10]) 
sample2 = np.array([30,26,32,34,28,29,31,35,36,33,32,27]) 
plt.figure(figsize=(10,5))
plt.subplot(2,2,1)
plt.hist(sample1)
plt.title('Histogram of Sample  1 ')

plt.subplot(2,2,2)
stats.probplot(np.array(sample1), dist="norm", plot=pylab)
plt.title('Q-Q plot of Sample 1')


plt.subplot(2,2,3)
plt.hist(sample2)
plt.title('Histogram of Sample 2 ')

plt.subplot(2,2,4)
stats.probplot(np.array(sample2), dist="norm", plot=pylab)
plt.title('Q-Q plot of Sample 2')

# set the spacing between subplots
plt.subplots_adjust(left=0.2,
                    bottom=0.2,
                    right=0.8,
                    top=0.8,
                    wspace=0.5,
                    hspace=0.5)
plt.show()

t_statistic, p_value = stats.ttest_ind(sample1, sample2, equal_var=False)

print(f'two sample t-test = t statistic and p-value for paired t-test {t_statistic, p_value}')

#Paired t-test
IQ_pre = [95, 98, 90, 115, 112]
IQ_pos = [95, 110, 97, 112, 117]

t_statistic, p_value = stats.ttest_rel(IQ_pos, IQ_pre, alternative = 'greater')

print(f't statistic and p-value for paired t-test {t_statistic, p_value}')

differences = [0, 12, 7,-3,5]


plt.subplot(1,2,1)
plt.hist(differences)
plt.title('Distribution of Difference')

plt.subplot(1,2,2)
stats.probplot(np.array(differences), dist="norm", plot=pylab)
plt.title('Q-Q plot of Difference')

plt.show()