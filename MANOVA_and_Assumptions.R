#One-Way MANOVA
#install.packages("car")
library(car)
data(Baumann)
attach(Baumann)


#Testing the Independence Assumption
#install.packages("psych")
library(psych)

ICC(Baumann[,4:6])


#Shapiro-Wilks Test for normality
library(mvnormtest)

transpose_Baumann <- t(Baumann[,4:6])
mshapiro.test(transpose_Baumann)


#2 Testing Positive Determinant of Variance-Covariance Matrix Assumption
CovBaumann <- cov(Baumann[,4:6])
det(CovBaumann )

group = factor(group)#encode group as a categorical variable

Y = cbind(post.test.1, post.test.2, post.test.3)

Baumann.manova = manova(Y~group)

summary(Baumann.manova, test="Wilks")
summary(Baumann.manova, test="Pillai")
summary(Baumann.manova, test="Hotelling-Lawley")
summary(Baumann.manova, test="Roy")


#Effects of Size (Partial Eta-Squared Values)

wilks_lamda = 0.63202 #From the summary of the wilks manova

#S = min(P, df_effect)
min(3, 2)

#Partial Eta squared = 1 - wilks_lamnda ^ 1/s

1-(0.63202)^(1/2)

#20.5% of the variance of grades of the 3 tests taken by the students are
#due to the difference of education style

