#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:37:06 2023

@author: samael
"""

import pandas as pd
import glob

# Buscamos todos los archivos .txt
archivos = glob.glob('*.txt')

# Creamos un diccionario para almacenar las interacciones de cada archivo
interacciones = {}

for archivo in archivos:
    # Leemos el archivo y agregamos las interacciones al diccionario
    df = pd.read_csv(archivo, sep='\t', header=None, names=['Gene1', 'Gene2', 'Interaction'])
    # Aseguramos que el par de genes esté ordenado alfabéticamente
    interacciones[archivo] = set(tuple(sorted([gene1, gene2])) for gene1, gene2 in zip(df['Gene1'], df['Gene2']))

# Ahora buscamos las interacciones únicas
interacciones_unicas = {}

for archivo in archivos:
    # Comenzamos asumiendo que todas las interacciones son únicas
    unicas = interacciones[archivo].copy()

    for otro_archivo in archivos:
        if otro_archivo != archivo:
            # Quitamos las interacciones que también están en los otros archivos
            unicas -= interacciones[otro_archivo]

    # Las interacciones que quedan son únicas para este archivo
    interacciones_unicas[archivo] = unicas

    # Guardamos las interacciones únicas en un archivo .txt
    with open(archivo.replace('.txt', '_unicas.txt'), 'w') as f:
        for gene1, gene2 in unicas:
            f.write(f'{gene1}\t{gene2}\n')
