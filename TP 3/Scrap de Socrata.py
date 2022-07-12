# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:59:30 2022

@author: felip
"""

#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
import os
os.chdir(r"C:\Users\felip\Documents\UdeSA\Maestría\Herramientas computacionales\TrabajosPracticos\TP 3")
# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("odn.data.socrata.com", None)

# Example authenticated client (needed for non-public datasets):
client = Socrata("odn.data.socrata.com",
                 "nColKKrqJghxr2dgibNZm6W49",
                 username="seminarioseconomia@udesa.edu.ar",
                 password="EconUdesa2020+")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("tt5s-y5fc", limit=100000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df.to_csv("crime.csv", header=True, index=False)