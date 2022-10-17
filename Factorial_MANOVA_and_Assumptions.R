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
