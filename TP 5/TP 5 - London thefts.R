################################################################################################
#                       HERRAMIENTAS COMPUTACIONALES DE INVESTIGACION                          #
#                                     TRABAJO PRACTICO 5                                       #
#                           FELIPE GARCIA VASSALLO & ROCIO SENRA                               #
################################################################################################

## ---- Configuración preliminar ----

# Librerias que vamos a usar
library(rgdal)
library(dplyr)
library(ggplot2)
library(tmap)

#Configuramos el directorio en el que vamos a trabajar
setwd("G:\\Mi unidad\\UdeSA Maestria en Economia\\Segundo Trimestre\\Herramientas\\TrabajosPracticos\\TrabajosPracticos\\TP 5")


## ---- Preparamos los datos ----


# Cargamos el shapefile "london_sport"
lnd <- readOGR("data/london_sport.shp")

# Cargamos el csv con datos de crimen en Londres
crime_data <- read.csv("data/mps-recordedcrime-borough.csv",
                       stringsAsFactors = FALSE)

# Nos quedamos con los crimenes "Theft & Handling"
crime_theft <- crime_data[crime_data$CrimeType == "Theft & Handling", ]

# Calculamos la cantidad (suma) de thefts para cada distrito (borough) en Londres
crime_ag <- aggregate(CrimeCount ~ Borough, FUN = sum, data = crime_theft)

# Chequeamos que los nombres de los boroughs coincidan en lnd  y crime_ag, luego vemos cuáles son las que no coinciden (City of London no está en la base crime_ag)
lnd$name %in% crime_ag$Borough
lnd$name[!lnd$name %in% crime_ag$Borough]


# Mergeamos las bases de datos con un left join (nos quedamos con los datos que coinciden)
lnd@data <- left_join(lnd@data, crime_ag, by = c('name' = 'Borough'))





## ---- Mapa de thefts con ggplot ----





## ---- Mapa de thefts con tmap ----

tm_shape(lnd) +
  #tm_style("classic")+
  tm_polygons("CrimeCount", 
              #palette = "-RdYlGn",
              #style = "jenks",
              n=4,
              #legend.hist = TRUE #esto sirve para agregar un histograma y ver la distribución de los valores, pero no queda bien
              )+
  tm_layout(main.title = "Thefts in London",
            main.title.position = "center",
            title.snap.to.legend = TRUE,
            title = "Amount of thefts by borough",
            panel.show = FALSE,
            #bg.color = "grey85", # para setear el color de fondo
            legend.outside = TRUE,
            frame = FALSE, #le saco el marco al mapa
            #legend.hist.height = 0.5, #alto del histograma en la leyenda (lo sacaría) 
            #legend.hist.width = 1,  #ancho del histograma en la leyenda (lo sacaría)
            title.position = c("center", "top"))

tmap_mode("view")

qtm(lnd, "CrimeCount") # plot the basic map
qtm(shp = lnd, 
    fill = "CrimeCount", 
    #fill.palette = "OrRd", 
    fill.title = "Thefts by borough in London",
    main.title = "AAAAAAAAA",
    breaks = c(1, 20, 40, 60, 80),
    legend.hist = TRUE,
    legend.outside = TRUE,
    legend.outside.position = "right",
    ) 



tmap_style("cobalt")
qtm(lnd, fill = "CrimeCount", format = "World")


#As a first attempt with ggplot2 we can create a scatter plot with the attribute data in the lnd object created previously:

library(ggplot2)
p <- ggplot(lnd@data, aes(Partic_Per, Pop_2001))

p + geom_point(aes(colour = Partic_Per, size = Pop_2001)) +
  geom_text(size = 2, aes(label = name))

install.packages("broom")
## ggmap requires spatial data to be supplied as data.frame, using tidy(). The generic plot() function can use Spatial objects directly; ggplot2 cannot. Therefore we need to extract them as a data frame. The tidy function was written specifically for this purpose. For this to work, broom package must be installed.
lnd_f <- broom::tidy(lnd)

# This step has lost the attribute information associated with the lnd object. We can add it back using the left_join function from the dplyr package (see ?left_join).
lnd$id <- row.names(lnd) # allocate an id variable to the sp data
head(lnd@data, n = 2) # final check before join (requires shared variable name)
lnd_f <- left_join(lnd_f, lnd@data) # join the data

# The new lnd_f object contains coordinates alongside the attribute information associated with each London Borough. It is now straightforward to produce a map with ggplot2. coord_equal() is the equivalent of asp = T in regular plots with R:

## ----"Map of Lond Sports Participation"-------------------------------
map <- ggplot(lnd_f, aes(long, lat, group = group, fill = Partic_Per)) +
  geom_polygon() + coord_equal() +
  labs(x = "Easting (m)", y = "Northing (m)",
       fill = "% Sports\nParticipation") +
  ggtitle("London Sports Participation")
map + scale_fill_gradient(low = "white", high = "black")
map



