#Factorial MANOVA
#install.packages("MASS")
library(car)
data(Soils)
options(scipen = 999)
library(MASS)
attach(Soils)


Contour <- factor(Contour)
Countour
Depth <- factor(Depth)
Depth


soils.mod <- lm(cbind(pH, Dens, Conduc)~ Contour + Depth + Contour*Depth -1, 
                data = Soils)
summary(soils.mod)

#Because there is no significance in the interaction term we can use the type II sum of squares

Manova(soils.mod, multivariate=TRUE, type=c("II"), test=("Wilks"))
Manova(soils.mod, multivariate=TRUE, type=c("II"), test=("Pillai"))
Manova(soils.mod, multivariate=TRUE, type=c("II"), test=("Hotelling-Lawley"))
Manova(soils.mod, multivariate=TRUE, type=c("II"), test=("Roy"))


#Eta Squared for Contour
#Effects of Size (Partial Eta-Squared Values)

wilks_lamda = 0.00939 #From the summary of the wilks manova

#S = min(P, df_effect)
min(3, 3)

#Partial Eta squared = 1 - wilks_lamnda ^ 1/s

1-(0.00939)^(1/3)


#78.9% of variance of the pH, Density, and Conductivity of the soil are due to
#to the differences in the Contour in the soil



#Eta Squared for Depth
#Effects of Size (Partial Eta-Squared Values)

wilks_lamda = 0.03164 #From the summary of the wilks manova

#S = min(P, df_effect)
min(3, 3)

#Partial Eta squared = 1 - wilks_lamnda ^ 1/s

1-(0.03164)^(1/3)

#68.37% of variance of the pH, Density, and Conductivity of the soil are due to
#to the differences in the Depth in the soil

