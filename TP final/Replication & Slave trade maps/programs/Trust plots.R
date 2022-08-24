library(dplyr)
library(ggplot2)
library(tidyverse)
library(scales)

setwd("C:/Users/felip/Documents/UdeSA/Maestría/Herramientas computacionales/TrabajosPracticos/TP final/Replication & Slave trade maps")

trust = read.csv("input/esclavos_trust.csv")

# Hago el atlantic trade

trust_atlantic = trust %>% filter(atlantica>0 & prom_trust_gov>=0 & prom_trust_inter>=0 & prom_trust_intra>=0 & prom_trust_neigh>=0 & prom_trust_relative>=0)

atl_neigh = ggplot(trust_atlantic, aes(atlantica,prom_trust_neigh))
atl_neigh + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

atl_relat = ggplot(trust_atlantic, aes(atlantica,prom_trust_relative))
atl_relat + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

atl_intra = ggplot(trust_atlantic, aes(atlantica,prom_trust_intra))
atl_intra + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

atl_inter = ggplot(trust_atlantic, aes(atlantica,prom_trust_inter))
atl_inter + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

atl_gov = ggplot(trust_atlantic, aes(atlantica,prom_trust_gov))
atl_gov + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

# Hago el indian trade

trust_indian = trust %>% filter(indianall>0 & prom_trust_gov>=0 & prom_trust_inter>=0 & prom_trust_intra>=0 & prom_trust_neigh>=0 & prom_trust_relative>=0)

ind_neigh = ggplot(trust_atlantic, aes(indianall,prom_trust_neigh))
ind_neigh + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

ind_relat = ggplot(trust_atlantic, aes(indianall,prom_trust_relative))
ind_relat + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

ind_intra = ggplot(trust_atlantic, aes(indianall,prom_trust_intra))
ind_intra + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

ind_inter = ggplot(trust_atlantic, aes(indianall,prom_trust_inter))
ind_inter + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)

ind_gov = ggplot(trust_atlantic, aes(indianall,prom_trust_gov))
ind_gov + geom_point() + geom_smooth(method="lm", formula=y~x) + scale_y_continuous(labels = comma)