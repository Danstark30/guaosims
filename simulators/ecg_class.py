import numpy as np
# import matplotlib.pyplot as plt
from ECGTot import ECGDualGuide as ECGen
from NoiseAdd import NoiseAdd
from ECGAnomalias import AnomFunc


def derivadas(bpm, amplitud, tiempo):
    """ Método para obtener derivadas normales

    """
    t = np.arange(0, tiempo, 0.008)
    e = ECGen(amplitud, bpm, 120, t)
    p_i_iii = e[0].tolist() + e[1].tolist() + e[2].tolist()
    p_a = e[3].tolist() + e[4].tolist() + e[5].tolist()
    p_v1_v3 = e[6].tolist() + e[7].tolist() + e[8].tolist()
    p_v4_v6 = e[9].tolist() + e[10].tolist() + e[11].tolist()

    return e, t, p_i_iii, p_a, p_v1_v3, p_v4_v6


def anomalias(anomalia, amplitud, tiempo):
    """ Método para obtener anomalía
    Args:
    - bpm: latidos por minuto
    - anomalia: entero correspondiente a anomalía
    - amplitud: amplitud de onda en mV
    - tiempo: tiempo de generación en s
    Retorno:
    - anom_signal: matriz con 12 arrays-derivadas
    - t: array de tiempo
    """
    anom = {'Fibrilación auricular': 2,
            'Fibrilación ventricular': 3,
            'Perdida de latido': 8,
            'Bradicarida extrema': 11,
            'Taquicardia extrema': 12,
            'Flúter auricular': 13,
            'Ritmo nodal': 15,
            'Taquicardia supraventricular': 16,
            }
    t = np.arange(0, tiempo, 0.008)

    anom_signal, t = AnomFunc(60, (60 / 60), t, anom[anomalia])
    anom_signal = anom_signal * amplitud

    return anom_signal, t


def add_noise(signal, fre, t):
    """ Método para añadir ruido """
    return NoiseAdd(signal, fre, t)


def fourier(signal, t):
    """ Método para representar espectro de fourier """
    ECGFourier = []
    Freq = (1 / 0.008) * np.arange(0, len(t)) / len(t)

    for i in range(len(signal)):
        ECGFourier.append(np.fft.fft(signal[i, :])[:len(Freq) // 2])

    return Freq[:len(Freq) // 2].tolist(), ECGFourier


def fourier_envolvente(signal):
    """
    Método que retorna la envolvente de un espectro de fourier
    considerando solo los valores más altos
    específicamente mayores a uno y generando los datos alrededor
    de los picos de frecuencia para que puedan ser ploteados
    en JS usando la librería chart JS
    Args:
    - signal: array de enteros
    Return:
    - envolvente: array de enteros
    """
    envolvente = signal[:]
    for i in range(len(envolvente)):
        if envolvente[i] < 1.5:
        	envolvente[i] = 0
        if i > int(0.3 * len(envolvente)) and envolvente[i-1] >= max(envolvente) * 0.3:
            if envolvente[i-2] < 1.5:
                envolvente[i-2] = 0.5
            if envolvente[i] < 1.5:
                envolvente[i] = 0.5
    envolvente = [i if i >= 0.5 else None for i in envolvente]
    envolvente[-1] = 0.5
    return envolvente

############ FREQ EJE HORIZONTAL, ECGFOURIER EJE VERTICAL ##############
# fig = plt.figure(figsize=(10, 10))
# plt.xlim(0, EjX)
# plt.ylim(0, EjY)
# plt.stem(Freq, ECGFourier.real)
# plt.show()


"""def show_ecg(signal, t):
	# Método para mostrar derivadas
	name = ['I','II','III', 'avR', 'avF', 'avL', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
	fig = plt.figure(figsize=(10, 10))
	for i in range(0, 12):
		fig.tight_layout(pad=2.0)
		ax = plt.subplot(3, 4, i + 1)
		ax.plot(t, signal[i])
		ax.set_xlabel('x')
		ax.set_ylabel('y')
		ax.set_title('Derivada:' + name[i])
	plt.show()
"""

########################################### Creación de objeto ####################################################

########################################## ECG NORMAL #############################################################

# array, t = derivadas(72, 10, 5)
# show_ecg(array, t)

######################################### ECG ANOMALÍA ############################################################

# anom = {'Fibrilación auricular': 2,
#	'Perdida de latido': 8,
#	'Bradicarida extrema': 11,
#	'Taquicardia extrema': 12,
#	'Flúter auricular': 13,
#	'Ritmo nodal': 15,
#	'Taquicardia supraventricular': 16,
# }
# for i in anom.keys():
#	array2, t2 = anomalias(72, i, 5)
#	#show_ecg(array2, t2)
#
######################################### ECG CON RUIDO ###########################################################
# withnoise = add_noise(array, 60, t)
# show_ecg(withnoise, t)

######################################## Espectro de Fourier ######################################
# Freq, ECGFourier = fourier(array, t)
# show_ecg(ECGFourier, Freq)
