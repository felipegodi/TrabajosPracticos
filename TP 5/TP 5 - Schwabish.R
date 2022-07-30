################################################################################################
#                       HERRAMIENTAS COMPUTACIONALES DE INVESTIGACION                          #
#                                     TRABAJO PRACTICO 5                                       #
#                           FELIPE GARCIA VASSALLO & ROCIO SENRA                               #
################################################################################################

## ---- Configuración preliminar ----

# Cargo paquetes
library("ggplot2")
library("tibble")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")
library("purrr")

# Pongo el path en donde tengo la data
setwd("~/Documents/UdeSA/Maestría/Herramientas computacionales/TrabajosPracticos/TP 5/Applied-Data-Visualization-with-R-and-ggplot2-master")

# Cargo la data
gapminder <- read.csv("data/gapminder-data.csv")
edu <- read.csv("data/xAPI-Edu-Data.csv")
loan <- read.csv("data/LoanStats.csv")

# Primer gráfico a "corregir"

##Grammar of graphics and visual components
#Subtopic - Layers
p1 <- ggplot(gapminder,aes(x=Electricity_consumption_per_capita))
p3 <- p1+geom_histogram(bins=15)
#Exercise-Layers
p4 <- p3+xlab("Electricity consumption per capita")
p4

# Cambios

# Filtro solo las observaciones que tienen el consumo pc de electricidad
paises = gapminder %>% filter(Electricity_consumption_per_capita != 0)
# Cuento la cantidad de observaciones que hay de cada país
paises2 = paises %>% group_by(Country) %>% summarise(obs=n())
paises2[-1]
# Me fijo cuantos paises tengo
count(unique(paises2[1]))

# SOlo hay 8 paises y usa muchas observaciones de un mismo país por lo tanto el histograma no parece lo más
# acorde para este gráfico. Pueden ser 8 plots distintos mostrando el progreso de los diferentes países o
# un plot que muestre los 8 juntos. 

paises3 = paises %>% filter(Year > 1979)

# Por ahora me quedé con este
p1 = ggplot(paises3, aes(y=Electricity_consumption_per_capita, x = Year, color = Country))
p2 = p1 + geom_line(size=1.5) + theme_minimal()
p3 = p2 + labs(x="",
               y="",
               title="Consumo de electricidad per cápita",
               subtitle="(kWh anual)")
p4 = p3 + theme(legend.position="top")
p5 = p4 + scale_color_discrete(name="",
                               labels=c("Brasil","China","Alemania","India","Japón","Reino Unido","Estados Unidos"))
p5

# Extras

# Histograma simple queda raro
p1 = ggplot(paises, aes(x=Electricity_consumption_per_capita, color = Country))
p2 = p1 + geom_histogram(fill="white", bins=10) + theme(legend.position="top")
p2

# Histogramas por décadas de forma vertical y en cuadrículas

paises4 = paises3 %>% filter(Year == 1980 | Year == 1990 | Year == 2000 | Year == 2010)

p1 = ggplot(paises4, aes(x=Electricity_consumption_per_capita))
p2 = p1 + geom_histogram(bins=4, fill="cadetblue4") +theme_minimal()
p3 = p2 + facet_grid(rows=vars(Year)) + labs(x="",
                                             y="",
                                             title="Histogramas del consumo de electricidad per cápita",
                                             subtitle="(kWh anual)")
p3

# Acá empieza el de cuadrículas
p1 = ggplot(paises4, aes(x=Electricity_consumption_per_capita))
p2 = p1 + geom_histogram(bins=4, fill="cadetblue4") +theme_minimal()
p3 = p2 + facet_wrap(~Year) + labs(x="",
                                             y="",
                                             title="Histogramas del consumo de electricidad per cápita",
                                             subtitle="(kWh anual)")
p3
paises

#########################################################################

# Segundo gráfico a "corregir"

#Gráfico original
dfn <- loan[,c("home_ownership","loan_amnt","grade")]
dfn <- na.omit(dfn) #remove NA y NONE
dfn <- subset(dfn, !dfn$home_ownership %in% c("NONE"))
#People with higher credit grades take smaller loans
#People with lower credit grades take small loans if they don't have a mortgage.

#Finer labelling in y 
ggplot(dfn,aes(x=home_ownership,y=loan_amnt))+geom_boxplot(aes(fill=grade))+
  scale_y_continuous(breaks=seq(0,40000,2000))

# Cambios

# Me quedo con las columnas que me interesan
loan_sub = loan[,c("home_ownership","loan_amnt","grade")]
# Saco los NA
loan_sub = na.omit(loan_sub)
# Divido por situación de hogar
loan_sub = subset(loan_sub, !loan_sub$home_ownership %in% c("NONE"))

loan_sub_mean = loan_sub %>% group_by(grade, home_ownership) %>% mutate(prom = mean(loan_amnt))

p1 = ggplot(loan_sub_mean %>% group_by(grade, home_ownership) %>% summarise(prom = mean(prom)), aes(x=grade,y=prom,fill=grade))
p2 = p1 + geom_bar(stat="identity")
p3 = p2 + facet_wrap(~home_ownership)
p4 = p3 + labs(x="",
               y="",
               title="Average loan amount per credit grade depending on house status",
               subtitle="(Dollars)")
p5 = p4 + guides(fill="none")
p5 + scale_fill_brewer(palette="Accent")

##########################################################################

# Tercer gráfico a "corregir"

# Gráfico original
dfn <- subset(HollywoodMovies2013, Genre %in% c("Action","Adventure","Comedy","Drama","Romance")
              & LeadStudio %in% c("Fox","Sony","Columbia","Paramount","Disney"))
p1 <- ggplot(dfn,aes(Genre,WorldGross)) 
p1
p2 <- p1+geom_bar(stat="Identity",aes(fill=LeadStudio),position="dodge")
p2

# Cambios