import statsmodels.api as sm

df_affairs = sm.datasets.fair.load().data

print(df_affairs.head())

total_count = df_affairs.shape[0]

positive_count = df_affairs.loc[df_affairs['affairs'] > 0].shape[0]

positive_pct = positive_count / total_count

negative_pct = 1- positive_pct

print("Class 1 Balance: {}%".format(round(positive_pct*100, 2)))
print("Class 2 Balance: {}%".format(round(negative_pct*100, 2)))

#if the balance is close to 90/10 it becomes a major issue
#  and upsampling or downsampling might be a possible option

#convert affairs into a binary classification problem
df_affairs['affairs'] = np.where(df_affairs['affairs']> 0, 1, 0)


#features to use
X=df_affairs[['rate_marriage','age','yrs_married','children','religious','educ','occupation','occupation_husb']]
y=df_affairs['affairs']

