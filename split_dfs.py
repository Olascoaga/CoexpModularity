#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 09:15:05 2023

@author: samael
"""

import pandas as pd

sample_info = pd.read_csv('SampleAttributes.csv')
sample_interest = sample_info[sample_info['SMTSD'] == 'Muscle - Skeletal']
df = pd.read_csv('quantile_nor_skeletal.csv', index_col=0)

# Obtener IDs de muestras masculinas y femeninas presentes tanto en sample_interest como en df
male_ids = list(set(sample_interest[sample_interest['SEX'] == 'M']['SAMPID']).intersection(df.columns))
female_ids = list(set(sample_interest[sample_interest['SEX'] == 'F']['SAMPID']).intersection(df.columns))

# Seleccionar las columnas correspondientes a las IDs de muestras masculinas y femeninas en df
male_df = df.loc[:, df.columns.isin(male_ids)]
female_df = df.loc[:, df.columns.isin(female_ids)]

# Obtener IDs de muestras presentes tanto en sample_interest como en male_df o female_df
male_sample_ids = list(set(sample_interest[sample_interest['SEX'] == 'M']['SAMPID']).intersection(male_df.columns))
female_sample_ids = list(set(sample_interest[sample_interest['SEX'] == 'F']['SAMPID']).intersection(female_df.columns))

# Seleccionar las columnas correspondientes a las IDs de muestras para cada grupo en male_df y female_df
male_list = []
female_list = []
groups = sample_interest['GROUP'].unique().tolist()

for group in groups:
    male_g = male_df.loc[:, male_df.columns.isin(sample_interest[(sample_interest['GROUP'] == group) & (sample_interest['SEX'] == 'M') & (sample_interest['SAMPID'].isin(male_sample_ids))]['SAMPID'])]
    male_list.append(male_g)
    female_g = female_df.loc[:, female_df.columns.isin(sample_interest[(sample_interest['GROUP'] == group) & (sample_interest['SEX'] == 'F') & (sample_interest['SAMPID'].isin(female_sample_ids))]['SAMPID'])]
    female_list.append(female_g)
    
# Guardar cada DataFrame en un archivo CSV separado
for i, male_df in enumerate(male_list):
    group = groups[i]
    sex = 'M'
    filename = f'male_{group}.tsv'
    male_df.to_csv(filename, index=True, sep="\t")

for i, female_df in enumerate(female_list):
    group = groups[i]
    sex = 'F'
    filename = f'female_{group}.tsv'
    female_df.to_csv(filename, index=True, sep="\t")