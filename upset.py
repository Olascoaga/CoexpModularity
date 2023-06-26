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

csv_files = glob.glob('*.csv')

df = pd.DataFrame()

for file in csv_files:
    temp_df = pd.read_csv(file)
    filename = os.path.basename(file)
    temp_df['Sex'], temp_df['AgeRange'] = filename.split("_")[0:2]
    df = pd.concat([df, temp_df])
    
series = df.groupby('Term')[['Sex', 'AgeRange']].apply(lambda x: tuple(x.values.tolist())).apply(pd.Series).stack()

data = from_memberships(series)

plot(data)
pyplot.show()
