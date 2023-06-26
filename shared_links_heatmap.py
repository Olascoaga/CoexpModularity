#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 19:12:26 2023

@author: samael
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.colors import ListedColormap


def process_file(file_path):
    df = pd.read_csv(file_path, sep='\t', header=None, usecols=[0, 1, 2])
    interactions = {frozenset([row[0], row[1]]): row[2] for _, row in df.iterrows()}
    return interactions

def create_label(file_name):
    parts = file_name.split('_')
    label = parts[0][0] + parts[1][0]
    return label


def read_gene_files(directory):
    interactions_dict = OrderedDict()
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            file_path = os.path.join(directory, file_name)
            label = create_label(file_name)
            interactions = process_file(file_path)
            interactions_dict[label] = interactions
    return interactions_dict


directory = '/home/samael/Escritorio/Proyectos/Modularity/MI/ARACNE-multicore/launch/Top/'
interactions_dict = read_gene_files(directory)

# Crear matriz de intersección con una columna y una fila adicionales
intersection_matrix = pd.DataFrame(index=interactions_dict.keys(), columns=interactions_dict.keys())

for row_set in interactions_dict.keys():
    for col_set in interactions_dict.keys():
        shared_interactions = 0
        for gene_pair, interaction_value in interactions_dict[row_set].items():
            if gene_pair in interactions_dict[col_set]:
                shared_interactions += 1
        intersection_matrix.loc[row_set, col_set] = shared_interactions

# Convertir los elementos de la matriz a enteros
intersection_matrix = intersection_matrix.astype(int)

# Enmascarar el triángulo inferior y la diagonal
mask = np.triu(np.ones_like(intersection_matrix, dtype=bool), k=1)

# Crear el mapa de calor para el triángulo superior sin la diagonal
plt.figure(figsize=(10, 8))
ax = sns.heatmap(intersection_matrix, annot=True, fmt='d', cmap='coolwarm', linewidths=0.5, mask=mask, cbar=False)

plt.title("Matriz de intersección de interacciones compartidas (triángulo superior)")
plt.savefig('interaction_matrix_heatmap_upper_triangle.png')
