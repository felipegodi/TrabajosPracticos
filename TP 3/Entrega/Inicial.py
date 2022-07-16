# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:01:47 2022

@author: felip
"""

# ACLARACIÓN: Este .py debe estar adentro de la carpeta WorldWeatherOnline-master para que la llamada del paquete funcione.
# hay una versión puesta en esa misma carpeta. Solo se puso acá el .py para un mejor acceso en la entrega

#### Import package

from wwo_hist import retrieve_hist_data


#### Set working directory to store output csv file(s)

import os
os.chdir(r"C:\Users\felip\Documents\UdeSA\Maestría\Herramientas computacionales\TrabajosPracticos\TP 3\Maryland\Weather")



#### Example code
#key de roro = '878d932ddac1487f9db124051221107'
frequency=24
start_date = '01-JAN-2015'
end_date = '31-DEC-2015'
api_key = 'e65da32c84d841cc8d7215553221107'
location_list = ["20603","20607","20615","20619","20758","20759","20810","21001","21074","21087",
                 "21212","21502","21520","21601","21607","21613","21629","21651","21701","21713",
                 "21804","21811","21817","21901"]

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)