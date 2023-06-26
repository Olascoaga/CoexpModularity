#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 18:27:18 2023

@author: samael
"""

import os
import pandas as pd
from collections import OrderedDict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def process_file(file_path):
    df = pd.read_csv(file_path, sep='\t', header=None, usecols=[0, 1])
    unique_genes = set(df[0].unique()).union(set(df[1].unique()))
    return unique_genes

def create_label(file_name):
    parts = file_name.split('_')
    label = parts[0][0] + parts[1][0]
    return label

def read_gene_files(directory):
    gene_sets = OrderedDict()
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            file_path = os.path.join(directory, file_name)
            label = create_label(file_name)
            unique_genes = process_file(file_path)
            gene_sets[label] = unique_genes
    return gene_sets

directory = '/home/samael/Escritorio/Proyectos/Modularity/MI/ARACNE-multicore/launch/Top/'
gene_sets = read_gene_files(directory)


# Crear matriz de intersección con una columna y una fila adicionales
intersection_matrix = pd.DataFrame(index=gene_sets.keys(), columns=gene_sets.keys())

for row_set in gene_sets.keys():
    for col_set in gene_sets.keys():
        intersection_matrix.loc[row_set, col_set] = len(gene_sets[row_set].intersection(gene_sets[col_set]))

# Rellenar los valores faltantes en la matriz de intersección con ceros
intersection_matrix.fillna(0, inplace=True)

# Convertir los elementos de la matriz a enteros
intersection_matrix = intersection_matrix.astype(int)

# Enmascarar el triángulo inferior y la diagonal
mask = np.triu(np.ones_like(intersection_matrix, dtype=bool), k=1)

# Crear el mapa de calor
plt.figure(figsize=(10, 8))
sns.heatmap(intersection_matrix, annot=True, fmt='d', cmap='coolwarm', linewidths=0.5, mask=mask)
plt.title("Matriz de intersección con tamaño de conjuntos (triángulo superior)")
plt.savefig('intersection_matrix_heatmap_upper_triangle.png')