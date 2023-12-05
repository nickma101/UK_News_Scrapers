library(tidyverse)
library(rjson)
library(data.table)
library(ggplot2)

data = read.csv('environment.csv')
data$dates = substring(data$datePublished,0,10)

ggplot(data, mapping = aes(x=dates)) +
  geom_bar()
