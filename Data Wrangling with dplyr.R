# Touching base on some of the new functions in dplyr

#install.packages("tidyverse")
library(tidyverse)
attach(starwars)

data("starwars")


glimpse(starwars)

#across()

#This would be a way to do it without across, and how it becomes repetitive
starwars %>% summarize(height_mean = mean(height, na.rm = TRUE),
                       mass_mean = mean(mass, na.rm = TRUE))

#across allows us not to duplicate code
starwars %>% summarize(across(height:mass, mean, na.rm=TRUE))

# This can do it across all columns of similar type regardless of location
starwars %>% summarize(across(where(is.numeric), mean, na.rm=TRUE))

#Other functions are available, such as mean, min, median

# we can also do more than one function with a list
starwars %>% summarize(across(where(is.numeric), 
                              list(min=min, max=max), 
                              na.rm=TRUE))
#if we need the function syntax
starwars %>% summarize(across(where(is.numeric), ~min(.x, 
                              na.rm=TRUE)))

#the min=min the first is just a name to help us understand the variable name

#can also be done on strings etc. Doesn't have to be numeric

#find number of unique values in character variables
#We need the function syntax which is the ~
#The .x is a stand in for the variables within the across
starwars %>% summarize(across(where(is.character), ~ length(unique(.x))))





