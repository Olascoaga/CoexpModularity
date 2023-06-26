#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 08:35:41 2023

@author: samael
"""

import pandas as pd
import glob
import os
from upsetplot import from_memberships, plot
from matplotlib import pyplot

# Obtén la lista de archivos csv en la carpeta
csv_files = glob.glob('*.csv')

# Define un dataframe vacío para almacenar los datos
df = pd.DataFrame()

# Carga cada archivo csv en un dataframe y concatena
for file in csv_files:
    temp_df = pd.read_csv(file)
    # Añade nuevas columnas para indicar el sexo y el rango de edad
    filename = os.path.basename(file)
    temp_df['Sex'], temp_df['AgeRange'] = filename.split("_")[0:2]
    df = pd.concat([df, temp_df])

# Ahora que tenemos los datos, creemos una serie de membership
# Podemos ignorar los datos que no sean de la columna 'description'
series = df.groupby('Term')[['Sex', 'AgeRange']].apply(lambda x: tuple(x.values.tolist())).apply(pd.Series).stack()

# Y ahora utilizamos from_memberships para convertirlo en un formato que UpSetPlot puede usar
data = from_memberships(series)

# Finalmente, dibujamos la gráfica
plot(data)
pyplot.show()
