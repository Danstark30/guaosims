# -*- coding: utf-8 -*-
"""
Created on Thu May 23 11:09:32 2019
@author: Juan Camilo
Modificated on Mon Jul 13 14:50:00 2021
@by: Soren Acevedo
"""
import numpy as np
import math


def NoiseAdd(ECG, noise, t):
    """
    Función que añade uno o más ruidos a la señal
    Args:
    - ECG: señal ecg, dos dimensiones, 12 * cantidad de datos
    - noise: lista de diccionarios con la forma 
        { 
            'check': booleano, --> True - Se aplica ruido
            'value': número, --> Frecuencia
            'amp': entero o str --> Amplitud de ruido en porcentaje
        }
    - t: array que contiene valores de tiempo
    """
    frequencies = [i.get('value') for i in noise if i.get('check') == True]
    amplitudes = [int(i.get('amp')) /
                  100 for i in noise if i.get('check') == True]
    ECGN = ECG[:]

    for i in range(len(frequencies)):
        for j in range(len(ECGN)):
            for k in range(0, len(t)):
                ECGN[j][k] = ECGN[j][k] + \
                    (amplitudes[i] * math.sin(2 *
                     math.pi * frequencies[i] * t[k]))

    return ECGN


def noise_single_derivation(signal, freq, amp, t):
    """
    Función que añade ruido a una sola derivación de ecg, o una señal
    de forma array, dimensión (1,).
    Args:
    - signal: señal | array
    - freq: frecuencia de ruido | número
    - amp: amplitud de ruido | número
    - t: vector de tiempo | array
    Return:
    - Señal con ruido | array
    """
    for i in range(len(signal)):
        signal[i] = signal[i] + (amp * math.sin(2 * math.pi * freq * t[i]))

    return signal


def irregular_noise(signal, freq, num_parts, amp, t):
    """
    Función que añade ruido en tramos aleatorios de la señal
    Args:
    - signal: señal | array
    - freq: frecuencia de ruido | número
    - num_parts: cantidad de tramos | entero
    - amp: amplitud del ruido | entero
    Return:
    - Señal con ruido | array
    """
  
    for i in range(num_parts):
        periodo = 1 / freq
        total_indx_periodo = int((periodo // 0.05))
        index_start = np.random.randint(0, len(signal) - total_indx_periodo)
        index_end = index_start + total_indx_periodo
        for j in range(index_start, index_end):
            signal[j] = signal[j] + (int(amp) / 100 * math.sin(2 * math.pi * freq * t[j - index_start]))
    return signal