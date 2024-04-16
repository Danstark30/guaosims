# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 10:33:01 2019
@author: Juan Camilo
"""

################ IMPORTAR LIBRERIAS ######################

import math
#import matplotlib.pyplot as plt
import ECGGen as ECG
import time
import numpy as np

def ECGDualGuide(ATotal,BPM,N,t):
    ############## VALORES DETERMINADOS POR EL USUARIO ######

    Frecs=BPM/60
    T=1/Frecs
    pi=3.1416
    
    ############### DURACIÓN DE ONDAS ########################
    
    TPW=0.37*(math.sqrt(T))-0.22*T-0.06
    TTW=1.06*(math.sqrt(T))-0.51*T-0.33
    TQRS=0.25*(math.sqrt(T))-0.16*T-0.01 
    TPQ=0.33*(math.sqrt(T))-0.18*T-0.08
    TST=-0.09*(math.sqrt(T))+0.13*T+0.04
    
    ############## DESFASES ONDA P Y T #######################
    
    DesfaseP=-0.5*TPW-TPQ-0.5*TQRS
    DesfaseT=0.5*TPW+TST+0.5*TQRS
    
    ############# INTERVALOS DE TIEMPO #######################
    
    A=-TPQ-0.5*TQRS-TPW
    B=-TPQ-0.5*TQRS
    C=TST+0.5*TQRS
    D=TTW+TST+0.5*TQRS
    

    
    ############ LEAD 1 ######################################
    
    Ar=(6/10)*ATotal
    As=(0/10)*ATotal
    At=(1.5/10)*ATotal
    Ap=(1/10)*ATotal
    
    one_period = np.arange(0, T + 0.008, 0.008)
    
    D1=ECG.ECG_S(one_period,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Ap,Ar,As,At,N)
    Corte=((TQRS/2)+TST*0.5)/0.01
    Corte=math.ceil(Corte)
    D1[:]=D1[:]-D1[Corte]
    
    for index, x in np.ndenumerate(one_period):
        if (x > TST and x < T - TPQ) and D1[index] < D1[Corte]:
            D1[index] = D1[Corte]

    while len(D1) < len(t):
        D1 = np.concatenate((D1, D1[1:]), axis=0)
    D1 = D1[:len(t)]
    
    ########### LEAD 2 ########################################
    
    Ar=(9/10)*ATotal
    As=(2/10)*ATotal
    At=(2.5/10)*ATotal
    Ap=(1.5/10)*ATotal
    D2=ECG.ECG_S(one_period,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Ap,Ar,As,At,N)
    D2[:]=D2[:]-D2[Corte]

    for index, x in np.ndenumerate(one_period):
        if (x > TST and x < T - TPQ) and D2[index] < D2[Corte]:
            D2[index] = D2[Corte]

    while len(D2) < len(t):
        D2 = np.concatenate((D2, D2[1:]), axis=0)
    D2 = D2[:len(t)]
    
    ########### LEAD 3 ############################################
    D2_3=ECG.ECG_S(one_period,DesfaseP - TPW / 2,DesfaseT,A,B,C,D,pi,TPW / 2,TTW,TQRS,TPQ,TST,T,Ap,Ar,As,At,N)
    
    for index, x in np.ndenumerate(one_period):
        if (x > TST and x < T - TPQ) and D2_3[index] < D2_3[Corte]:
            D2_3[index] = D2_3[Corte]

    while len(D2_3) < len(t):
        D2_3 = np.concatenate((D2_3, D2_3[1:]), axis=0)
    
    D2_3 = D2_3[:len(t)]
    D2_3[:]=D2_3[:]-D2_3[Corte]
    D3 = D2_3 - D1
    
    ################################################################
    ################ LAS BIPOLARES AUMENTADAS ######################
    ################################################################ 
    
    ##################### aVR ######################################
    
    avR=(-1/2)*(D1+D2)
    
    #################### aVL ########################################
    
    avL=D1-(1/2)*D2
    
    ################### aVF #########################################
    
    avF=D2-(1/2)*D1
    
    ################################################################
    ################ LAS PRECORDIALES ##############################
    ################################################################ 
    
    ################### V1 #########################################
    
    Ar=(2/10)*ATotal
    As=(4.5/10)*ATotal
    At=(0.7/10)*ATotal
    Ap=(0.5/10)*ATotal
    
    V1=ECG.ECG_S(one_period,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Ap,Ar,As,At,N)
    V1[:]= V1[:] - V1[Corte]
    
    for index, x in np.ndenumerate(one_period):
        if (x > TST and x < T - TPQ) and V1[index] < V1[Corte]:
            V1[index] = V1[Corte]

    while len(V1) < len(t):
        V1 = np.concatenate((V1, V1[1:]), axis=0)
    V1 = V1[:len(t)]
    
    ################## V2 #############################################
    
    Ar=(4/10)*ATotal
    As=(7/10)*ATotal
    At=(1.7/10)*ATotal
    Ap=(1/10)*ATotal
    
    V2=ECG.ECG_S(one_period,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Ap,Ar,As,At,N)
    V2[:]= V2[:] - V2[Corte]
    
    for index, x in np.ndenumerate(one_period):
        if (x > TST and x < T - TPQ) and V2[index] < V2[Corte]:
            V2[index] = V2[Corte]

    while len(V2) < len(t):
        V2 = np.concatenate((V2, V2[1:]), axis=0)
    V2 = V2[:len(t)]
    
    
    ################## V3 #############################################
    
    Ar=(9/10)*ATotal
    As=(5/10)*ATotal
    At=(3/10)*ATotal
    Ap=(2/10)*ATotal
    
    V3=ECG.ECG_S(one_period,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Ap,Ar,As,At,N)
    V3[:]= V3[:] - V3[Corte]
    
    for index, x in np.ndenumerate(one_period):
        if (x > TST and x < T - TPQ) and V3[index] < V3[Corte]:
            V3[index] = V3[Corte]

    while len(V3) < len(t):
        V3 = np.concatenate((V3, V3[1:]), axis=0)
    V3 = V3[:len(t)]
    
    ################## V4 #############################################
    
    Ar=(6/10)*ATotal
    As=(5/10)*ATotal
    At=(2/10)*ATotal
    Ap=(1.2/10)*ATotal

    V4=ECG.ECG_S(one_period,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Ap,Ar,As,At,N)
    V4[:]= V4[:] - V4[Corte]
    
    for index, x in np.ndenumerate(one_period):
        if (x > TST and x < T - TPQ) and V4[index] < V4[Corte]:
            V4[index] = V4[Corte]

    while len(V4) < len(t):
        V4 = np.concatenate((V4, V4[1:]), axis=0)
    V4 = V4[:len(t)]
    ################ V5 #######################################################
    
    Ap=(1/10)*ATotal
    At=(2/10)*ATotal
    Aqrs=(9/10)*ATotal
    V5=ECG.ECG_NS(t,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Aqrs,Ap,At,N)
    V5[:]=V5[:]-V5[Corte]
    for i in range (0,len(t)):
        if (V5[i]<-0.01):
            V5[i]=V5[Corte]
    
    ################################## V6 #####################################
    
    Ap=(1/10)*ATotal
    At=(1.2/10)*ATotal
    Aqrs=(7/10)*ATotal
    V6=ECG.ECG_NS(t,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Aqrs,Ap,At,N)
    V6[:]=V6[:]-V6[Corte]
    for i in range (0,len(t)):
        if (V6[i]<-0.01):
            V6[i]=V6[Corte]
    
    ################################ LATIGUILLOS PREDIALES ###################
    LV1=V1+(1/3)*(D1+D2)
    LV2=V2+(1/3)*(D1+D2)
    LV3=V3+(1/3)*(D1+D2)
    LV4=V4+(1/3)*(D1+D2)
    LV5=V5+(1/3)*(D1+D2)
    LV6=V6+(1/3)*(D1+D2)
    
    Signal=np.zeros((12,len(t)))
    Signal[0,0:len(t)]=D1[:,0]
    Signal[1,0:len(t)]=D2[:,0]
    Signal[2,0:len(t)]=D3[:,0]
    Signal[3,0:len(t)]=avR[:,0]
    Signal[4,0:len(t)]=avL[:,0]
    Signal[5,0:len(t)]=avF[:,0]
    Signal[6,0:len(t)]=V1[:,0]
    Signal[7,0:len(t)]=V2[:,0]
    Signal[8,0:len(t)]=V3[:,0]
    Signal[9,0:len(t)]=V4[:,0]
    Signal[10,0:len(t)]=V5[:,0]
    Signal[11,0:len(t)]=V6[:,0]
    
    
    return Signal