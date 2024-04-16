"""
UAO SpO2 Simulator GUI - No Hardware Required !
-------------------------------------
Created on Thu Dec 21 12:07:49 2017
by the author: Kevin Machado Gamboa
Contact: ing.kevin@hotmail.com
Modified on Sun Oct 11 10:29:39 2020
------------------------------------
REFERENCES: 
    [1] Development of a Low-Cost Pulse Oximeter Simulator for Educational Purposes
    https://github.com/kevinmgamboa/UAO_SpO2_Sim
    [2] Sebastian Sepulveda - plot data from a function in real time 
    https://github.com/ssepulveda/RTGraph/tree/oldRTGraph
    [3] Qt for Python - https://doc.qt.io/qtforpython/
"""
# -----------------------------------------------------------------------------
#                             Libraries Needed
# -----------------------------------------------------------------------------
import numpy as np
import json
#from time import time
import scipy.io as sio
from scipy.signal import savgol_filter
#from collections import deque
#from multiprocessing import Queue
#import matplotlib.pyplot as plt

class SpO2():

    def __init__(self, spo2value, hr):
        # Initiate QMainWindow Object
        self.dataR = []
        self.dataIR = []
        self.TIME = []
        self.ampR = 0.4  # amplitude for Red signal
        self.ampIR = 0.270  # amplitude for InfraRed signal
        self.minR = 1.45  # Displacement from zero for Red signal
        self.minIR = 1.45  # Displacement from zero for Red signal
        self.spo2value =  spo2value
        self.hr = hr

    ## -----------------------------------
    ##    SpO2 Parameters & Plotting
    ## -----------------------------------
    def ppg_parameters(self, minR, ampR, minIR, ampIR, t, HR):
        """
        Store the function of two signals - e.g PPG Red and Infrared channel signals
        We can also put here a sine, cosine, etc.
        """
        f = HR * (1 / 60)
        # Spo2 Red signal function
        self.sR = minR + ampR * (0.05 * np.sin(2 * np.pi * t * 3 * f) + 0.4 * np.sin(2 * np.pi * t * f) +
                                 0.22 * np.sin(2 * np.pi * t * 2 * f + 45))
        # self.sR = minR + ampR * (0.5 * np.sin(2 * np.pi * t * f) + 0.22 * np.sin(2 * np.pi * t * 2 * f + 40))
        # Spo2 InfraRed signal function
        self.sIR = minIR + ampIR * (0.05 * np.sin(2 * np.pi * t * 3 * f) + 0.4 * np.sin(2 * np.pi * t * f) +
                                    0.22 * np.sin(2 * np.pi * t * 2 * f + 45))
        # self.sIR = minIR + ampIR * (0.5 * np.sin(2 * np.pi * t * f) + 0.22 * np.sin(2 * np.pi * t * 2 * f + 40))

        return self.sR, self.sIR

    def spo2sl_change(self):
        """
        Change the value of the SpO2 when moving the slider.
        It also have the list of SpO2 values vs the R value
        """
        # Creación de gráfica %SpO2 vs R-Value #

        sp02 = list(range(50, 101))[::-1]

        R = [0.50, 0.55, 0.60, 0.64, 0.66, 0.70, 0.71, 0.72, 0.73, 0.75, 0.76, 0.77, 0.78, 0.80, 0.81, 0.82, 0.83,
             0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.00,
             1.01, 1.00, 1.05, 1.11, 1.12, 1.16, 1.19, 1.25, 1.27, 1.32, 1.33, 1.35, 1.39, 1.43, 1.47, 1.52, 1.50]

        Ri = [0] * 51

        Ri[sp02.index(self.spo2value)] = R[sp02.index(self.spo2value)]

        # R-IR values & SpO2
        rR = [0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.4, 0.4,
              0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
              0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]

        IR = [0.6, 0.71, 0.68, 0.65, 0.62, 0.45, 0.43, 0.56, 0.54, 0.53, 0.52, 0.52, 0.51, 0.5, 0.5, 0.49, 0.49, 0.48,
              0.59, 0.47, 0.46, 0.46, 0.45, 0.44, 0.44, 0.44, 0.43, 0.43, 0.43, 0.42, 0.42, 0.41, 0.41, 0.4, 0.4, 0.39,
              0.38, 0.37, 0.36, 0.35, 0.34, 0.33, 0.32, 0.31, 0.3, 0.29, 0.29, 0.28, 0.28, 0.27, 0.27]

        self.ampR = rR[sp02.index(self.spo2value)]
        self.ampIR = IR[sp02.index(self.spo2value)]

        # Suavizar señal
        R = np.array(R)
        sp02 = np.array(sp02)
        R = savgol_filter(R, 53, 11, mode='nearest')
        R[0] = 0.5
        R[50] = 1.5

        # Crear identificador de punto de saturación
        R_new = np.arange(0.5, 1.502, 0.02)
        sp02 = np.interp(R_new, R, sp02)
        cercano = [(abs(i - self.spo2value)) for i in sp02]
        idx_spo2 = cercano.index(min(cercano))
        Ri = np.full(len(R), None)
        sp02 = sp02.tolist()
        for i in range(len(Ri)):
            if i <= idx_spo2:
                Ri[i] = self.spo2value

        Ri[idx_spo2] = 50

        R = R*10

        return R_new.tolist(), json.dumps(Ri.tolist()), sp02, idx_spo2

        ##### COLORES #####
        #  R VS SPO2 = ROJO
        #  Ri vs SPO2 = AZUL
        # en una misma gráfica ambos vectores

    def _initial(self):
        """
        contain the initial figure in the UI
        """
        t = np.linspace(0, (1 / (self.hr / 60)), 100)
        s_r, s_ir = self.ppg_parameters(self.minR, self.ampR, self.minIR, self.ampIR, t, self.hr)

        # Change this to sio.loadmat('curvesHB') in localhost and to deploy in pythonanywhere: '/home/fullstacklatam/fullstacklatam.pythonanywhere.com/curvesHB.mat'
        data = sio.loadmat('curvesHB')
        x = data['x']

        xhb_o2, hb_o2, x_oxy_hb, oxy_hb = x[0], x[1], x[2], x[3]

        # Recorrido de longitud de onda
        hb_x = np.linspace((600 + (100 - self.spo2value) / 2), 1000, 100)
        hb_y = x[5]

        # Data para representación acorde a %SpO2
        x_estandar = np.arange(600, 1000, 2)
        hb = np.interp(x_estandar, hb_x, oxy_hb)
        for i in range(len(hb) // 2):
            if hb[i] == hb[i + 1] and hb[i] > 0.5:
                hb[i] = None
        # Interpolación para estándar 100 %SpO2
        hb100 = np.interp(x_estandar, x_oxy_hb, oxy_hb)

        # Interpolación para estándar 0 %
        h0 = np.interp(x_estandar, xhb_o2, hb_o2)

        for i in range(len(h0) // 2):
            if h0[i] == h0[i + 1]:
                h0[i] = None

        # Indicadores de ln para emisores y abs
        ln = np.full(len(x_estandar), None)
        idx_ln = x_estandar.tolist().index(650)
        idx_ln2 = x_estandar.tolist().index(940)
        ln[idx_ln] = 2.5
        ln[idx_ln2] = 2.5
        ln[idx_ln-1] = 0
        ln[idx_ln2-1] = 0

        # Iniciar gráfica estática en punto mínimo
        min_idx = s_r.tolist().index(min(s_r))
        s_r1 = s_r[:min_idx]
        s_r2 = s_r[min_idx:-1]
        s_r = list(s_r2) + list(s_r1)

        min_idxi = s_ir.tolist().index(min(s_ir))
        s_ir1 = s_ir[:min_idxi]
        s_ir2 = s_ir[min_idxi:-1]
        s_ir = list(s_ir2) + list(s_ir1)

        return t[:-1], s_r, s_ir, hb100.tolist(), json.dumps(hb.tolist()), json.dumps(h0.tolist()), x_estandar.tolist(), json.dumps(ln.tolist()), hb[idx_ln], hb[idx_ln2]

        ##### COLORES ##### DE ESTE SALEN DOS GRÁFICAS
        # GRÁFICA 1:
        #  xhb_o2 vs hb_o2 AZUL
        #  x_oxy_hb vs oxy_hb AZUL
        #  hb_x vs hb_y ROJO
        # en una misma gráfica ambos vectores
        # GRÁFICA 2:
        # t VS s_ir AZUL
        # t VS s_r ROJO

    def _update_plot(self, time):
        """
        Updates and redraws the graphics in the plot.
        """
        # Getting heart rate
        # generates the time
        for i in np.arange(0, time, 0.02):
            self.sR, self.sIR = self.ppg_parameters(self.minR, self.ampR, self.minIR, self.ampIR, i, self.hr)

        # store data into variables 
            self.TIME.append(i)
            self.dataR.append(self.sR)
            self.dataIR.append(self.sIR)

        return self.TIME, self.dataR, self.dataIR

        ##### COLORES #####
        #  dataR VS SPO2 = ROJO
        #  dataRi vs SPO2 = AZUL
        # en una misma gráfica ambos vectores

########################################### Creación Objeto SpO2 ###############################################

#mio = SpO2(100, 72)

#################################### Creación de gráfica %SpO2 vs R-Value ######################################

#R, Ri, sp02 = mio.spo2sl_change()
#plt.plot(R, sp02)
#plt.plot(Ri, sp02)
#plt.show()

################################### Creación de gráfica Longitud de Onda vs Absorción ##########################

#t, s_r, s_ir, xhb_o2, hb_o2, x_oxy_hb, oxy_hb, hb_x, hb_y = mio._initial()

#plt.plot(xhb_o2, hb_o2, 'b')
#plt.plot(x_oxy_hb, oxy_hb, 'b')
#plt.plot(hb_x, hb_y, 'r')
#plt.show()

################################## Creación de gráfica estática de V vs t #####################################

#t, s_r, s_ir, xhb_o2, hb_o2, x_oxy_hb, oxy_hb, hb_x, hb_y = mio._initial()

#plt.plot(t, s_ir, 'b')
#plt.plot(t, s_r, 'r')
#plt.show()

################################# Creación de gráfica completa V vs t #########################################

#TIME, dataR, dataIR = mio._update_plot(15)
#plt.plot(TIME, dataR, 'r')
#plt.plot(TIME, dataIR, 'b')
#plt.show()