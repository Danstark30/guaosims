import numpy as np
import json
#from matplotlib import pyplot as plt


def gen_nibp(ps=90, pd=70, fc=60):
    """ Método para generar nibp
    Args:
    - ps: presión sistólica
    - pd: presión diastólica
    - fc: frecuencia cardíaca
    Retorno:
    - x: array de tiempo
    - y1: presión en brazalete
    - y2: pulsos de presión
    - a_idx_s: array with ps index
    - a_idx_d: array with pd index
    - a_idx_m: array with pm index
    - y2_m: array de zeros con pico en pm
    - y2_s: array de zeros con pico en ps
    - y2_d: array de zeros con pico en pd
    """
    pm = ((ps - pd) / 3) + pd  # Presión Media
    level = ps * 1.40  # Presión de insuflado máxima
    lim = pd * 0.8  # Presión hasta la cual realizá escalones
    x, y1, y2, r = [], [], [], []

    ######### Definition Oscilometric Pulses ###########

    maxi = 4
    df = 0.75
    sf = 0.80

    ######### Cálculo de pulsos #######################
    def pulse_calculation(pres):

        if ((pres <= pm) and (pres > pd * 0.7)):
            pulso = (maxi * (1 - df) / (pm - pd)) * (pres - pm) + 4
    
        elif ((pres > pm) and (pres <= ps)):
            pulso = (maxi * (1 - sf) / (ps - pm)) * (ps - pres) + maxi * sf

        elif (pres > ps) and (pres < ps * 1.5):
            pulso = maxi * sf * (((2.5 * (ps - pres)) / (250 - ps)) + 1)

        else:
            pulso = 0
        return pulso

    ######### Time Real Graph ###############

    tiempo_insuflado = round(level / 33, 1)
    for i in np.arange(0, tiempo_insuflado + 0.05, 0.05):
        x.append(i)
        y1.append(i * level / tiempo_insuflado)
        y2.append(0)

    longitud_insuflado = len(x)

    while level > lim:

        r.append(x[-1] + 0.05)
        level -= 5

        ############ Presion Peeks ######################
        for j in np.arange(0, 1.05, 0.05):
            y1.append(level)
            y2.append(0)

            x.append(x[-1] + 0.05)
    ############## Final ###############################

    for i in np.arange(0, 3.05, 0.05):
        x.append(x[-1] + 0.05)
        y1.append(y1[-1] - y1[-1] * .5)
        y2.append(0)

    ############## Redondear a dos decimales ###########
    x = list(map(lambda x: round(x, 2), x))
    r = list(map(lambda r: round(r, 2), r))

    ############# Vector de pulsos acorde a frecuencia ##
    puls = np.arange(x.index(r[0] + 1), len(x), 20 * (60 / fc)).astype(int)
    intercepcion = y1[puls[0]]
    for i in puls:

        pres = (-5 * (x[i] - x[puls[0]])) + intercepcion
        pulse = pulse_calculation(pres)

        if pulse > 0:
            y1[i] += pulse
            y2[i] = pulse

    ########## Encontrar pulso de presión media ############################

    idx_m = y2.index(max(y2))

    ########## Encontrar pulso de presión sistólica ########################

    i_ps = [(abs(i - maxi * sf)) for i in y2[:y2.index(max(y2))]]
    idx_s = i_ps.index(min(i_ps))

    ########## Encontrar pulso de presión diastólica #######################

    i_pd = [(abs(i - maxi * df)) for i in y2[y2.index(max(y2)):]]
    idx_d = i_pd.index(min(i_pd)) + y2.index(max(y2))

    ######### Crear arreglos relacionados a los pulsos de presión #########

    a_idx_m = np.full(len(x), None)
    for i in range(len(a_idx_m)):
        if i < idx_m:
            a_idx_m[i] = pm
    a_idx_m[idx_m] = 0

    a_idx_s = np.full(len(x), None)
    for i in range(len(a_idx_s)):
        if i < idx_s:
            a_idx_s[i] = ps
    a_idx_s[idx_s] = 0

    a_idx_d = np.full(len(x), None)
    for i in range(len(a_idx_d)):
        if i < idx_d:
            a_idx_d[i] = pd
    a_idx_d[idx_d] = 0

    ######### Crear arreglos en señal oscilométrica #########

    y2_m = np.zeros(len(x))
    y2_m[idx_m] = 4
    y2_s = np.zeros(len(x))
    y2_m[idx_s] = 4
    y2_d = np.zeros(len(x))
    y2_m[idx_d] = 4

    simulator = [x, y1, y2, json.dumps(a_idx_m.tolist()), json.dumps(a_idx_s.tolist(
    )), json.dumps(a_idx_d.tolist()), y2_d.tolist(), y2_m.tolist(), y2_s.tolist(), pm]
    return simulator
