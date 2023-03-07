#Testing the 3 Assumptions of Multivariate analysis

#Cleaning the dataset

attach(attitude)

attitude <-  data.frame(attitude$complaints, attitude$learning, attitude$raises)

#1 Testing the Normality Assumption

#Shapiro-Wilks Test for normality
#install.packages("mvnormtest")
library(mvnormtest)

transpose_attidue <- t(attitude)
mshapiro.test(transpose_attidue)


#2 Testing Positive Determinant of Variance-Covariance Matrix Assumption
CovAttitude <- cov(attitude)
det(CovAttitude)

#3 Testing Equality of Variance-Covariance Matrices of Groups (Gender)

group <- rep(c('male', 'female'), c(15,15))
factor(group)
group

#install.packages("biotools")
library(biotools)

boxM(attitude, group)


#Hotelling T2 Test

#Compare Two Independent Group Means vectors

#Graph the means of the 3 variables for male and females
#install.packages('gplots')
library(gplots)

plotmeans(attitude.complaints ~ group, data=attitude, ylim=c(0,100), xlab = "Groups",
          legends = c("Males", "Females"), main="Attitude", connect=FALSE, mean.labels=TRUE, col=NULL,
          p=1.0)

plotmeans(attitude.learning ~ group, data=attitude, ylim=c(0,100), xlab = "Groups",
          legends = c("Males", "Females"), main="Attitude", connect=FALSE, mean.labels=TRUE, col=NULL,
          p=1.0)

plotmeans(attitude.raises ~ group, data=attitude, ylim=c(0,100), xlab = "Groups",
          legends = c("Males", "Females"), main="Attitude", connect=FALSE, mean.labels=TRUE, col=NULL,
          p=1.0)


#Perform Hotelling T2 Test
#install.packages("ICSNP")
library(ICSNP)

HotellingsT2(attitude[1:15,], attitude[16:30,])