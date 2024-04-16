from django.shortcuts import render
from simulators.nibp_app import gen_nibp as nibp_simulator
from simulators.ecg_class import derivadas as ecg_simulator
from simulators.ecg_class import add_noise as noise
from simulators.ecg_class import fourier, anomalias
from simulators.spo2_class import SpO2 as spo2_simulator
from simulators.gen_datasets import gen_csv as csv
from NoiseAdd import irregular_noise
from collections import deque
import numpy as np
import math
import json


def round_down(number: float, decimals: int = 2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor


def index(request):
    return render(request, 'simulators/index.html', {})


def sim_abiertos(request):
    return render(request, 'simulators/circuits.html', {})


def videos(request):
    return render(request, 'simulators/videos.html', {})


def links(request):
    return render(request, 'simulators/links.html', {})


def nibp(request):
    setps = 120
    setpm = 93
    setpd = 80
    setfc = 72
    animation = ''
    s = '---'
    d = '---'
    m = '---'
    f = '---'
    selected_idx = 0
    dataset = ''
    if request.method == 'POST':
        form = request.POST
        setps = int(form['ps'])
        setpd = int(form['pd'])
        setfc = int(form['fc'])
        noise_list = json.loads(form['noise'])
        simulator = nibp_simulator(
            int(form['ps']), int(form['pd']), int(form['fc']))
        if any([i.get("check") for i in noise_list]):
            noise_nibp = noise_list[0]
            simulator[1] = irregular_noise(simulator[1], noise_nibp.get(
                "value"), 1, noise_nibp.get("amp"), simulator[0])
        animation = 'interval()'
        s = int(form['ps'])
        d = int(form['pd'])
        f = int(form['fc'])
        m = str(np.round(simulator[9], 1))
        setpm = np.round(simulator[9], 1)
        columns = ['tiempo(s)', 'presión(mmHg)', 'oscilométrica(mmHg)']
        dataset = csv(new_columns=columns, data=np.transpose(simulator[:3]))
        options_values = ['aa', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        selected_option = form['clase']
        selected_idx = options_values.index(selected_option)
    else:
        simulator = [[0], [0], [0], [0], [0], [0], [], [], []]
    x = simulator[0]
    x = [round_down(i, 1) for i in list(x)]
    y1 = [round(i) for i in simulator[1]]
    y2 = simulator[2]
    a_idx_m = simulator[3]
    a_idx_s = simulator[4]
    a_idx_d = simulator[5]
    y2_d = simulator[6]
    y2_m = simulator[7]
    y2_s = simulator[8]
    
    return render(request, 'simulators/nibp.html', {'x': x, 'y1': y1, 'y2': y2, 'a_idx_m': a_idx_m, 'a_idx_s': a_idx_s, 'selected_idx': selected_idx,
                                                    'a_idx_d': a_idx_d, 'y2_d': y2_d, 'y2_m': y2_m, 'y2_s': y2_s, 'animation': animation, 'setpm': setpm,
                                                    's': s, 'm': m, 'd': d, 'f': f, 'setps': setps, 'setpd': setpd, 'setfc': setfc, 'dataset': dataset})


def ecg(request):
    setnormal = 'selected'
    setfiba = ''
    setfibv = ''
    setfibv = ''
    setbe = ''
    sette = ''
    setflua = ''
    setrn = ''
    setts = ''
    setfc = '60'
    setamp = '1'
    setruido = '60'
    setruidocb = ''
    setgraphtiempo = 'selected'
    setgraphfourier = ''
    set5 = 'selected'
    set10 = ''
    set15 = ''
    set20 = ''
    set25 = ''
    set30 = ''
    set35 = ''
    set40 = ''
    set45 = ''
    set50 = ''
    setderivadas1 = 'selected'
    setderivadas2 = ''
    setderivadas3 = ''
    setderivadas4 = ''
    animation = ''
    borderColor = '#2bff00'
    borderColor2 = '#ff0000'
    simulator = [np.zeros((12, 1)), [0]]
    x = [round_down(i, 2) for i in list(simulator[1])]
    x2 = []
    p_i_iii_max = [0, 1]
    p_i_iii_min = [0, 0]
    y1 = np.array(simulator[0][0]).tolist()
    y2 = np.array(simulator[0][1]).tolist()
    y3 = np.array(simulator[0][2]).tolist()
    y4 = np.array(simulator[0][3]).tolist()
    y5 = np.array(simulator[0][4]).tolist()
    y6 = np.array(simulator[0][5]).tolist()
    y7 = np.array(simulator[0][6]).tolist()
    y8 = np.array(simulator[0][7]).tolist()
    y9 = np.array(simulator[0][8]).tolist()
    y10 = np.array(simulator[0][9]).tolist()
    y11 = np.array(simulator[0][10]).tolist()
    y12 = np.array(simulator[0][11]).tolist()
    monitorfc = '------'
    monitoramp = '------'
    monitornoise = '------'
    monitortype = '------'
    graphtitle1, graphtitle2, graphtitle3 = ['', '', '']
    ruidocb = 'true'
    dataset_ecg = ''
    if request.method == 'POST':
        animation = 'interval()'
        form = request.POST
        noise_list = json.loads(form['noise'])
        if form['bpm'] != "--":
            setfc = int(form['bpm'])
        setamp = str(form['amplitud'])
        columns_ecg = [
            'tiempo(s)', 'I', 'II', 'III',
            'avR', 'avL', 'avF', 'v1', 'v2',
            'v3', 'v4', 'v5', 'v6',
        ]
        data_to_convert = []
        if form['clase'] == 'Fibrilación auricular':
            setfiba = 'selected'
        if form['clase'] == 'Fibrilación ventricular':
            setfibv = 'selected'
            setfc = "--"
        if form['clase'] == 'Bradicarida extrema':
            setbe = 'selected'
        if form['clase'] == 'Taquicardia extrema':
            sette = 'selected'
        if form['clase'] == 'Flúter auricular':
            setflua = 'selected'
        if form['clase'] == 'Ritmo nodal':
            setrn = 'selected'
        if form['clase'] == 'Taquicardia supraventricular':
            setts = 'selected'
        if form['setgraph'] == 'FOURIER':
            setgraphfourier = 'selected'
        if int(form['tiempo']) == 5:
            set5 = 'selected'
        if int(form['tiempo']) == 10:
            set10 = 'selected'
        if int(form['tiempo']) == 15:
            set15 = 'selected'
        if int(form['tiempo']) == 20:
            set20 = 'selected'
        if int(form['tiempo']) == 25:
            set25 = 'selected'
        if int(form['tiempo']) == 30:
            set30 = 'selected'
        if int(form['tiempo']) == 35:
            set35 = 'selected'
        if int(form['tiempo']) == 40:
            set40 = 'selected'
        if int(form['tiempo']) == 45:
            set45 = 'selected'
        if int(form['tiempo']) == 50:
            set50 = 'selected'
        if int(form['derivadas']) == 1:
            setderivadas1 = 'selected'
        if int(form['derivadas']) == 2:
            setderivadas2 = 'selected'
        if int(form['derivadas']) == 3:
            setderivadas3 = 'selected'
        if int(form['derivadas']) == 4:
            setderivadas4 = 'selected'
        monitorfc = str(form['bpm'])+' lpm'
        monitoramp = str(float(form['amplitud'])) + ' mV'
        monitortype = str(form['clase'])
        if any([i.get('check') for i in noise_list]):
            monitornoise = ''.join(
                [str(i.get('value')) + ' ' for i in noise_list if i.get('check')]) + ' Hz'
            ruidocb = 'true'
        else:
            ruidocb = 'false'
        if monitortype == 'Normal':
            monitortype = 'Ritmo Sinusal'
        if form['clase'] == 'Normal':
            simulator = ecg_simulator(int(form['bpm']), float(
                form['amplitud']), int(form['tiempo']))
            x = [round_down(i, 1) for i in list(simulator[1])]
            # -- Creación de Dataset Normal --
            data_to_convert.append(simulator[1])
            data_to_convert.extend(simulator[0])
            # -- Cierre --
            if int(form['derivadas']) == 1:
                graphtitle1, graphtitle2, graphtitle3 = ['I', 'II', 'III']
                p_i_iii_max = np.array(simulator[2]).tolist()
                p_i_iii_min = np.array(simulator[2]).tolist()
                y1 = np.array(simulator[0][0]).tolist()
                y2 = np.array(simulator[0][1]).tolist()
                y3 = np.array(simulator[0][2]).tolist()
            if int(form['derivadas']) == 2:
                graphtitle1, graphtitle2, graphtitle3 = ['aVR', 'aVL', 'aVF']
                p_i_iii_max = np.array(simulator[3]).tolist()
                p_i_iii_min = np.array(simulator[3]).tolist()
                y1 = np.array(simulator[0][3]).tolist()
                y2 = np.array(simulator[0][4]).tolist()
                y3 = np.array(simulator[0][5]).tolist()
            if int(form['derivadas']) == 3:
                graphtitle1, graphtitle2, graphtitle3 = ['V1', 'V2', 'V3']
                p_i_iii_max = np.array(simulator[4]).tolist()
                p_i_iii_min = np.array(simulator[4]).tolist()
                y1 = np.array(simulator[0][6]).tolist()
                y2 = np.array(simulator[0][7]).tolist()
                y3 = np.array(simulator[0][8]).tolist()
            if int(form['derivadas']) == 4:
                graphtitle1, graphtitle2, graphtitle3 = ['V4', 'V5', 'V6']
                p_i_iii_max = np.array(simulator[5]).tolist()
                p_i_iii_min = np.array(simulator[5]).tolist()
                y1 = np.array(simulator[0][9]).tolist()
                y2 = np.array(simulator[0][10]).tolist()
                y3 = np.array(simulator[0][11]).tolist()
            y4 = np.array(simulator[0][3]).tolist()
            y5 = np.array(simulator[0][4]).tolist()
            y6 = np.array(simulator[0][5]).tolist()
            y7 = np.array(simulator[0][6]).tolist()
            y8 = np.array(simulator[0][7]).tolist()
            y9 = np.array(simulator[0][8]).tolist()
            y10 = np.array(simulator[0][9]).tolist()
            y11 = np.array(simulator[0][10]).tolist()
            y12 = np.array(simulator[0][11]).tolist()
        if form['clase'] != 'Normal' and form['clase'] != '------':
            simulator = anomalias(form['clase'], float(
                form['amplitud']), int(form['tiempo']))
            simulator = np.array(simulator)
            x = [round_down(i, 1) for i in list(simulator[1])]
            if int(form['derivadas']) == 1:
                graphtitle1, graphtitle2, graphtitle3 = ['I', 'II', 'III']
                y1 = np.array(simulator[0][0]).tolist()
                y2 = np.array(simulator[0][1]).tolist()
                y3 = np.array(simulator[0][2]).tolist()
                p_i_iii_max = y1+y2+y3
                p_i_iii_min = y1+y2+y3
            if int(form['derivadas']) == 2:
                graphtitle1, graphtitle2, graphtitle3 = ['aVR', 'aVL', 'aVF']
                y1 = np.array(simulator[0][3]).tolist()
                y2 = np.array(simulator[0][4]).tolist()
                y3 = np.array(simulator[0][5]).tolist()
                p_i_iii_max = y1 + y2 + y3
                p_i_iii_min = y1 + y2 + y3
            if int(form['derivadas']) == 3:
                graphtitle1, graphtitle2, graphtitle3 = ['V1', 'V2', 'V3']
                y1 = np.array(simulator[0][6]).tolist()
                y2 = np.array(simulator[0][7]).tolist()
                y3 = np.array(simulator[0][8]).tolist()
                p_i_iii_max = y1 + y2 + y3
                p_i_iii_min = y1 + y2 + y3
            if int(form['derivadas']) == 4:
                graphtitle1, graphtitle2, graphtitle3 = ['V4', 'V5', 'V6']
                y1 = np.array(simulator[0][9]).tolist()
                y2 = np.array(simulator[0][10]).tolist()
                y3 = np.array(simulator[0][11]).tolist()
                p_i_iii_max = y1 + y2 + y3
                p_i_iii_min = y1 + y2 + y3
            y4 = np.array(simulator[0][3]).tolist()
            y5 = np.array(simulator[0][4]).tolist()
            y6 = np.array(simulator[0][5]).tolist()
            y7 = np.array(simulator[0][6]).tolist()
            y8 = np.array(simulator[0][7]).tolist()
            y9 = np.array(simulator[0][8]).tolist()
            y10 = np.array(simulator[0][9]).tolist()
            y11 = np.array(simulator[0][10]).tolist()
            y12 = np.array(simulator[0][11]).tolist()
            data_to_convert.append(simulator[1])
            data_to_convert.extend(simulator[0])
        if any([i.get('check') for i in noise_list]):
            t = simulator[1]
            simulator = noise(simulator[0], noise_list, t)
            x = [round_down(i, 1) for i in list(t)]
            if int(form['derivadas']) == 1:
                y1 = np.array(simulator[0]).tolist()
                y2 = np.array(simulator[1]).tolist()
                y3 = np.array(simulator[2]).tolist()
                p_i_iii_max = y1 + y2 + y3
                p_i_iii_min = y1 + y1 + y3
            if int(form['derivadas']) == 2:
                y1 = np.array(simulator[3]).tolist()
                y2 = np.array(simulator[4]).tolist()
                y3 = np.array(simulator[5]).tolist()
                p_i_iii_max = y1 + y2 + y3
                p_i_iii_min = y1 + y1 + y3
            if int(form['derivadas']) == 3:
                y1 = np.array(simulator[6]).tolist()
                y2 = np.array(simulator[7]).tolist()
                y3 = np.array(simulator[8]).tolist()
                p_i_iii_max = y1 + y2 + y3
                p_i_iii_min = y1 + y1 + y3
            if int(form['derivadas']) == 4:
                y1 = np.array(simulator[9]).tolist()
                y2 = np.array(simulator[10]).tolist()
                y3 = np.array(simulator[11]).tolist()
                p_i_iii_max = y1 + y2 + y3
                p_i_iii_min = y1 + y1 + y3
            y4 = np.array(simulator[3]).tolist()
            y5 = np.array(simulator[4]).tolist()
            y6 = np.array(simulator[5]).tolist()
            y7 = np.array(simulator[6]).tolist()
            y8 = np.array(simulator[7]).tolist()
            y9 = np.array(simulator[8]).tolist()
            y10 = np.array(simulator[9]).tolist()
            y11 = np.array(simulator[10]).tolist()
            y12 = np.array(simulator[11]).tolist()
            columns_ecg.extend(['I_ruido', 'II_ruido', 'III_ruido',
                                'avR_ruido', 'avL_ruido', 'avF_ruido', 'v1_ruido', 'v2_ruido',
                                'v3_ruido', 'v4_ruido', 'v5_ruido', 'v6_ruido'])
            data_to_convert.extend(simulator)
        if form['fourier'] == 'fourier':
            animation = 'interval()'
            borderColor2 = '#ff0000'
            if any([i.get('check') for i in noise_list]):
                simulator = fourier(simulator, simulator[1])
            else:
                simulator = fourier(simulator[0], simulator[1])
            dataset_ecg = csv(new_columns=columns_ecg,
                              data=np.transpose(data_to_convert))
            x2 = simulator[0]
            if int(form['derivadas']) == 1:
                y4 = json.dumps(abs(simulator[1][0]).tolist())
                y5 = json.dumps(abs(simulator[1][1]).tolist())
                y6 = json.dumps(abs(simulator[1][2]).tolist())
            if int(form['derivadas']) == 2:
                y4 = json.dumps(abs(simulator[1][3]).tolist())
                y5 = json.dumps(abs(simulator[1][4]).tolist())
                y6 = json.dumps(abs(simulator[1][5]).tolist())
            if int(form['derivadas']) == 3:
                y4 = json.dumps(abs(simulator[1][6]).tolist())
                y5 = json.dumps(abs(simulator[1][7]).tolist())
                y6 = json.dumps(abs(simulator[1][8]).tolist())
            if int(form['derivadas']) == 4:
                y4 = json.dumps(abs(simulator[1][9]).tolist())
                y5 = json.dumps(abs(simulator[1][10]).tolist())
                y6 = json.dumps(abs(simulator[1][11]).tolist())
            y7 = np.array(abs(simulator[1][6])).tolist()
            y8 = np.array(abs(simulator[1][7])).tolist()
            y9 = np.array(abs(simulator[1][8])).tolist()
            y10 = np.array(abs(simulator[1][9])).tolist()
            y11 = np.array(abs(simulator[1][10])).tolist()
            y12 = np.array(abs(simulator[1][11])).tolist()
    return render(request, 'simulators/ecg.html', {'x': x, 'x2': x2, 'y1': y1, 'y2': y2, 'y3': y3, 'y4': y4, 'y5': y5, 'y6': y6,
                                                   'y7': y7, 'y8': y8, 'y9': y9, 'y10': y10, 'y11': y11, 'y12': y12,
                                                   'p_i_iii_max': p_i_iii_max, 'p_i_iii_min': p_i_iii_min,
                                                   'animation': animation, 'borderColor': borderColor, 'borderColor2': borderColor2,
                                                   'monitorfc': monitorfc, 'monitoramp': monitoramp, 'monitortype': monitortype,
                                                   'monitornoise': monitornoise, 'graphtitle1': graphtitle1, 'graphtitle2': graphtitle2,
                                                   'graphtitle3': graphtitle3, 'ruidocb': ruidocb, 'setfc': setfc, 'setamp': setamp,
                                                   'setruido': setruido, 'setruidocb': setruidocb, 'setgraphfourier': setgraphfourier,
                                                   'setgraphtiempo': setgraphtiempo,
                                                   'set5': set5, 'set10': set10, 'set15': set15, 'set20': set20, 'set25': set25,
                                                   'set30': set30, 'set35': set35, 'set40': set40, 'set45': set45, 'set50': set50,
                                                   'setderivadas1': setderivadas1, 'setderivadas2': setderivadas2,
                                                   'setderivadas3': setderivadas3, 'setderivadas4': setderivadas4,
                                                   'setnormal': setnormal, 'setfiba': setfiba, 'setfibv': setfibv, 'setbe': setbe,
                                                   'sette': sette, 'setflua': setflua, 'setrn': setrn, 'setts': setts,
                                                   'dataset_ecg': dataset_ecg})


def spo2(request):
    setSpO2 = 95
    setfc = 60
    set5 = 'selected'
    set10 = ''
    set15 = ''
    fc = "---"
    set20 = ''
    set25 = ''
    set30 = ''
    set35 = ''
    set40 = ''
    set45 = ''
    set50 = ''
    setppg = 'selected'
    setppgfull = ''
    setirvsr = ''
    setspo2vsr = ''
    setavsl = ''
    animation = ''
    dataset_spo2 = ''
    if request.method == 'POST':
        animation = 'interval();'
        form = request.POST
        setSpO2 = int(form['spo2'])
        setfc = int(form['hr'])
        if int(form['tiempo']) == 5:
            set5 = 'selected'
        if int(form['tiempo']) == 10:
            set10 = 'selected'
        if int(form['tiempo']) == 15:
            set15 = 'selected'
        if int(form['tiempo']) == 20:
            set20 = 'selected'
        if int(form['tiempo']) == 25:
            set25 = 'selected'
        if int(form['tiempo']) == 30:
            set30 = 'selected'
        if int(form['tiempo']) == 35:
            set35 = 'selected'
        if int(form['tiempo']) == 40:
            set40 = 'selected'
        if int(form['tiempo']) == 45:
            set45 = 'selected'
        if int(form['tiempo']) == 50:
            set50 = 'selected'
        if str(form['graphSelector']) == 'PPG':
            setppg = 'selected'
        if str(form['graphSelector']) == 'PPGFULL':
            setppgfull = 'selected'
        if str(form['graphSelector']) == 'IRvsR':
            setirvsr = 'selected'
        if str(form['graphSelector']) == 'SpO2vsR':
            setspo2vsr = 'selected'
        if str(form['graphSelector']) == 'AvsL':
            setavsl = 'selected'
        simulator = spo2_simulator(int(form['spo2']), int(form['hr']))
        R, Ri, SpO2, idx_spo2 = simulator.spo2sl_change()
        R = [round_down(i, 2) for i in list(R)]
        IRdc = '1,45'
        Rdc = '1,45'
        Rac = simulator.ampR
        IRac = simulator.ampIR
        varR = round(Rac / IRac, 2)
        varR2 = round(R[idx_spo2], 2)
        varSpO2 = str(int(form['spo2']))+'%'
        x1, y1, y2 = simulator._update_plot(int(form['tiempo']))
        x = [round_down(i, 1) for i in x1]
        t, s_r, s_ir, hb100, hb, h0, x_estandar, ln, idx_ln, idx_ln2 = simulator._initial()
        t = list([round_down(i, 2) for i in list(t)])
        s_ir = list(s_ir)
        s_r = list(s_r)
        alpha650 = round(idx_ln, 2)
        alpha940 = round(idx_ln2, 2)
        columns_spo2 = ['Tiempo(s)', 'R(mV)', 'IR(mV)']
        dataset_spo2 = csv(new_columns=columns_spo2,
                           data=np.transpose([x1, y1, y2]))
        fc = form['hr']
    else:
        simulator2 = [[0], [0], [0]]
        x = simulator2[0]
        y1 = simulator2[1]
        y2 = simulator2[2]
        R = simulator2[0]
        Ri = simulator2[1]
        SpO2 = simulator2[2]
        t = simulator2[0]
        s_ir = simulator2[1]
        s_r = simulator2[2]
        hb100 = simulator2[0]
        hb = simulator2[0]
        h0 = simulator2[0]
        x_estandar = simulator2[0]
        idx_spo2 = 0
        ln = 0
        idx_ln = 0
        idx_ln2 = 0
        Rdc = '---'
        IRdc = '---'
        Rac = '---'
        IRac = '---'
        varR = '---'
        varR2 = '---'
        varSpO2 = '---'
        alpha650 = '---'
        alpha940 = '---'
    return render(request, 'simulators/spo2.html', {'x': x, 'y1': y1, 'y2': y2, 'Ri': Ri, 'R': R, 'SpO2': SpO2, 't': t,
                                                    's_ir': s_ir, 's_r': s_r, 'hb100': hb100, 'hb': hb, 'h0': h0,
                                                    'x_estandar': x_estandar, 'idx_spo2': idx_spo2, 'animation': animation,
                                                    'ln': ln, 'idx_ln': idx_ln, 'idx_ln2': idx_ln2, 'Rac': Rac, 'IRac': IRac,
                                                    'varR': varR, 'Rdc': Rdc, 'IRdc': IRdc, 'varR2': varR2, 'varSpo2': varSpO2,
                                                    'alpha650': alpha650, 'alpha940': alpha940, 'setSpO2': setSpO2, 'setfc': setfc,
                                                    'set5': set5, 'set10': set10, 'set15': set15, 'set20': set20, 'set25': set25,
                                                    'set30': set30, 'set35': set35, 'set40': set40, 'set45': set45, 'set50': set50,
                                                    'setppg': setppg, 'setirvsr': setirvsr, 'setspo2vsr': setspo2vsr, 'setavsl': setavsl,
                                                    'dataset_spo2': dataset_spo2, 'setppgfull': setppgfull, 'fc': fc
                                                    })
