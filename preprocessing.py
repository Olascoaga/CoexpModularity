# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 15:23:51 2023

@author: olask
"""
import pandas as pd
import numpy as np

df = pd.read_csv('skeletal.gct', sep='\t', skiprows=2)
df = df.set_index(df['Name'])
df = df.drop(['id', 'Name', 'Description'], axis=1)


df['Mean'] = np.mean(df, axis=1)
df = df[df['Mean'] > 10]
df = df.drop(['Mean'], axis=1)
def zero_count(row):
    return (row == 0).sum() >= len(row)/2
df = df[~df.apply(zero_count, axis=1)]
