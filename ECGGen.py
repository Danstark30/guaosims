# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 19:46:29 2018
@author: Juan Camilo
"""
import math
import numpy as np



def ECG_NS(t,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Aqrs,Ap,At,N):
    Signal=np.zeros([len(t),1],dtype=np.float64)
    A0qrs=(-Aqrs*TQRS/T)
    A0p=(2*Ap*TPW/(pi*T))*(math.sin((pi*B/TPW)+DesfaseP)-math.sin((pi*A/TPW)+DesfaseP))
    A0t=(2*At*TTW/(pi*T))*(math.sin((pi*D/TTW)+DesfaseT)-math.sin((pi*C/TTW)+DesfaseT))
    A0w=A0p+A0qrs+A0t

    for i in range(1,N):
        ANqrs=(2*Aqrs*T/((pi**2)*(i**2)*TQRS))*(1-math.cos(pi*i*TQRS/T))
        ANp=(Ap*TPW)*((1/(pi*T+2*pi*i*TPW))*(math.sin((pi*B/(TPW))+(2*pi*i*B/T)+DesfaseP)-math.sin((pi*A/(TPW))+(2*pi*i*A/T)+DesfaseP))+(1/(pi*T-2*pi*i*TPW))*(math.sin((pi*B/(TPW))-(2*pi*i*B/T)+DesfaseP)-math.sin((pi*A/(TPW))-(2*pi*i*A/T)+DesfaseP)))
        ANt=-(At*TTW)*((1/(pi*T+2*pi*i*TTW))*(math.sin((pi*D/(TTW))+(2*pi*i*D/T)+DesfaseT)-math.sin((pi*C/(TTW))+(2*pi*i*C/T)+DesfaseT))+(1/(pi*T-2*pi*i*TTW))*(math.sin((pi*D/(TTW))-(2*pi*i*D/T)+DesfaseT)-math.sin((pi*C/(TTW))-(2*pi*i*C/T)+DesfaseT)))
        ANw=ANqrs+ANp+ANt
        BNqrs=0
        BNp=(Ap*TPW)*((-1/(pi*T+2*pi*i*TPW))*(math.cos((pi*B/(TPW))+(2*pi*i*B/T)+DesfaseP)-math.cos((pi*A/(TPW))+(2*pi*i*A/T)+DesfaseP))+(1/(pi*T-2*pi*i*TPW))*(math.cos((pi*B/(TPW))-(2*pi*i*B/T)+DesfaseP)-math.cos((pi*A/(TPW))-(2*pi*i*A/T)+DesfaseP)))
        BNt=-(At*TTW)*((-1/(pi*T+2*pi*i*TTW))*(math.cos((pi*D/(TTW))+(2*pi*i*D/T)+DesfaseT)-math.cos((pi*C/(TTW))+(2*pi*i*C/T)+DesfaseT))+(1/(pi*T-2*pi*i*TTW))*(math.cos((pi*D/(TTW))-(2*pi*i*D/T)+DesfaseT)-math.cos((pi*C/(TTW))-(2*pi*i*C/T)+DesfaseT)))
        BNw=BNqrs+BNp+BNt;
        for j in range (1,len(t)):
            SignTemp=ANw*math.cos(2*pi*i*t[j]/T)+BNw*math.sin(2*pi*i*t[j]/T);
            Signal[j]=Signal[j]+SignTemp;

    return Signal

def ECG_S(t,DesfaseP,DesfaseT,A,B,C,D,pi,TPW,TTW,TQRS,TPQ,TST,T,Ap1,Ar1,As1,At1,N):
    Signal=np.zeros([len(t),1],dtype=np.float64)
    A0qrs1=(TQRS/T)*(-1.5*Ar1-0.5*As1)
    A0p1=(2*Ap1*TPW/(pi*T))*(math.sin((pi*B/TPW)+DesfaseP)-math.sin((pi*A/TPW)+DesfaseP))
    A0t1=(2*At1*TTW/(pi*T))*(math.sin((pi*D/TTW)+DesfaseT)-math.sin((pi*C/TTW)+DesfaseT))
    A0w1=A0p1+A0qrs1+A0t1
    for i in range (1,N):
        ANqrs1=(T/((pi**2)*(i**2)*TQRS))*((Ar1*(1-math.cos(pi*i*TQRS/T)))+As1*(math.cos(pi*i*TQRS/T)-1))
        ANp1=(Ap1*TPW)*((1/(pi*T+2*pi*i*TPW))*(math.sin((pi*B/(TPW))+(2*pi*i*B/T)+DesfaseP)-math.sin((pi*A/(TPW))+(2*pi*i*A/T)+DesfaseP))+(1/(pi*T-2*pi*i*TPW))*(math.sin((pi*B/(TPW))-(2*pi*i*B/T)+DesfaseP)-math.sin((pi*A/(TPW))-(2*pi*i*A/T)+DesfaseP)))
        ANt1=-(At1*TTW)*((1/(pi*T+2*pi*i*TTW))*(math.sin((pi*D/(TTW))+(2*pi*i*D/T)+DesfaseT)-math.sin((pi*C/(TTW))+(2*pi*i*C/T)+DesfaseT))+(1/(pi*T-2*pi*i*TTW))*(math.sin((pi*D/(TTW))-(2*pi*i*D/T)+DesfaseT)-math.sin((pi*C/(TTW))-(2*pi*i*C/T)+DesfaseT)))
        ANw1=ANqrs1+ANp1+ANt1
        BNqrs1=(1/(pi*i))*(((T/(pi*i*TQRS))*(Ar1+As1)*math.sin(pi*i*TQRS/T))-Ar1-As1)
        BNp1=(Ap1*TPW)*((-1/(pi*T+2*pi*i*TPW))*(math.cos((pi*B/(TPW))+(2*pi*i*B/T)+DesfaseP)-math.cos((pi*A/(TPW))+(2*pi*i*A/T)+DesfaseP))+(1/(pi*T-2*pi*i*TPW))*(math.cos((pi*B/(TPW))-(2*pi*i*B/T)+DesfaseP)-math.cos((pi*A/(TPW))-(2*pi*i*A/T)+DesfaseP)))
        BNt1=-(At1*TTW)*((-1/(pi*T+2*pi*i*TTW))*(math.cos((pi*D/(TTW))+(2*pi*i*D/T)+DesfaseT)-math.cos((pi*C/(TTW))+(2*pi*i*C/T)+DesfaseT))+(1/(pi*T-2*pi*i*TTW))*(math.cos((pi*D/(TTW))-(2*pi*i*D/T)+DesfaseT)-math.cos((pi*C/(TTW))-(2*pi*i*C/T)+DesfaseT)))
        BNw1=BNqrs1+BNp1+BNt1
        for j in range (1,len(t)):            
            SignTemp=ANw1*math.cos(2*pi*i*t[j]/T)+BNw1*math.sin(2*pi*i*t[j]/T);
            Signal[j]=Signal[j]+SignTemp;
        
    return Signal
