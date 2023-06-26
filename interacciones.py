#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 19:53:03 2023

@author: samael
"""

import os

# Función para leer un archivo y almacenar la información en un diccionario
def leer_archivo(nombre_archivo):
    diccionario = {}
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            elementos = linea.strip().split()
            if len(elementos) < 3:
                continue # Ignorar líneas con menos de 3 elementos
            genes = tuple(elementos[:2]) # Tomar los primeros 2 elementos como genes
            medida = float(elementos[2]) # Tomar el tercer elemento como medida
            diccionario[genes] = medida
    return diccionario

# Función para obtener las interacciones compartidas entre varios archivos
def obtener_interacciones_compartidas(archivos):
    interacciones_compartidas = set()
    for archivo in archivos:
        interacciones = set(leer_archivo(archivo).keys())
        if len(interacciones_compartidas) == 0:
            interacciones_compartidas = interacciones
        else:
            interacciones_compartidas = interacciones_compartidas.intersection(interacciones)
    return interacciones_compartidas

# Obtener las interacciones compartidas por todos los archivos
archivos = [archivo for archivo in os.listdir('.') if archivo.endswith('.txt')]
interacciones_todas = obtener_interacciones_compartidas(archivos)
with open('interacciones_todas.txt', 'w') as archivo:
    for interaccion in interacciones_todas:
        gene1, gene2 = interaccion
        medida = leer_archivo(archivos[0])[interaccion] # Tomar la medida del primer archivo
        archivo.write(f'{gene1}\t{gene2}\t{medida}\n')

