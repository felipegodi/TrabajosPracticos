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
library(broom)
library(ggpubr)

# Configuramos el directorio en el que vamos a trabajar
#setwd("G:\\Mi unidad\\UdeSA Maestria en Economia\\Segundo Trimestre\\Herramientas\\TrabajosPracticos\\TrabajosPracticos\\TP 5")
#setwd("~/Documents/UdeSA/Maestría/Herramientas computacionales/TrabajosPracticos/TP 5")
setwd("/Volumes/GoogleDrive/My Drive/UdeSA Maestria en Economia/Segundo Trimestre/Herramientas/TrabajosPracticos/TrabajosPracticos/TP 5")
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
#Para poder usar ggplot para armar el mapa, convertimos los datos a un dataframe, usando la función tidy().
lnd_f <- broom::tidy(lnd)

#Agregamos al dataframe los nombres de los barrios
lnd$id <- row.names(lnd) # allocate an id variable to the sp data
lnd_f <- left_join(lnd_f, lnd@data) # join the data

aux <- lnd_f[lnd_f$order == 1, ]



map <- ggplot(lnd_f, aes(long, lat, group = group, fill = CrimeCount)) +
  geom_polygon(colour="darkgray") + coord_equal() +
  geom_text(aes(label = name), data = aux, check_overlap = TRUE, stat = "identity",position = "identity", size = 3, hjust = 0.5)+ #ALGO ASI DEBERIAMOS USAR PARA AGREGARLE LAS LABELS, PERO APARECEN FEAS :( PORQUE HAY MUCHAS FILAS CON EL MISMO NAME. CREO QUE DEBERÍAMOS HACER ALGO TIPO COLLAPSE, PERO LE PREGUNTARÍA A AMELIA, intente varias cosas y nada me funcionó. 
  labs(x = "x", y = "y",
       fill = "Amount of thefts")
  #ggtitle("London Thefts")

map + scale_fill_distiller(name="Amount of thefts", 
                           palette = "Reds", 
                           direction= +1
                           #breaks = pretty_breaks()
                           )+ theme_transparent()




## ---- Mapa de thefts con tmap ----

tmap_thefts <- tm_shape(lnd) +
              #tm_style("classic") +                             # esto es para fijar algun estilo para los mapas (sobre todo cuando hacemos muchos mapas y queremos que todos tengan el mismo formato)
               tm_polygons("CrimeCount", 
                          palette = "Reds",                      # paleta de colores
                          #style = "jenks",                      # partición de ls categorías
                          n=4,                                   # cantidad de categorías preferida
                          title = "Amount of thefts by borough", # titulo de la leyenda
                          #legend.hist = TRUE                    # esto sirve para agregar un histograma y ver la distribución de los valores, pero no queda bien
                          ) +
               tm_text("name",                                   # agrego las etiquetas a los barrios
                       size = 0.6,                               # tamaño de la etiqueta. puede ser "AREA" tambien, para que el tamaño de cada etiqueta se ajuste al tamaño del distrito que representa
                       col = "black",                            # color de la etiqueta
                       remove.overlap = TRUE,                    # evito que se superpongan
                       overwrite.lines = TRUE,                   # permito que el nombre se encime con las lineas
                       shadow = TRUE                             # le agrego el sombreado
                       ) +
               tm_layout(#main.title = "Thefts in London",       # lo saco porque vamos a agregarlo en latex
                         #main.title.size = 3,
                         #main.title.position = "center",
                         title.position = c("center", "top"),
                         #bg.color = "grey85",                   # para setear el color de fondo
                         legend.outside = TRUE,
                         #legend.outside.position = "right",
                         legend.position = c("right", "bottom"),
                         legend.title.size = 1.3,
                         legend.text.size = 0.9,
                         frame = FALSE, #                        # le saco el marco al mapa
                         #legend.hist.height = 0.5,              # alto del histograma en la leyenda (lo sacaría) 
                         #legend.hist.width = 1,                 # ancho del histograma en la leyenda (lo sacaría)
                        )

tmap_thefts

tmap_save(tmap_thefts, "map1.png")

