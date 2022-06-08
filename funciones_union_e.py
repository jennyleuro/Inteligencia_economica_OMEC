from datetime import datetime
import locale
import pandas as pd
from numpy import NaN
import numpy as np


def infoSplitDf(info_extraction, indicador):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    period_list, value_list = [], []

    for i in range(0,len(info_extraction), 3):
        element = info_extraction[i:i+3]

        if('Q1' in element[0]):
            element[0] = element[0][0:4]+'-03'
        elif('Q2' in element[0]):
            element[0] = element[0][0:4]+'-06'
        elif('Q3' in element[0]):
            element[0] = element[0][0:4]+'-09'
        elif('Q4' in element[0]):
            element[0] = element[0][0:4]+'-12'
        
        if(element[0]== '1999-12'):
            break
        elif (element[1] == 'N/E'):
            value_list.append(NaN)
        else:
            value = locale.atof(element[1])
            value_list.append(value)
        element_date = datetime.strptime(element[0], '%Y-%m')
        period_list.append(str(element_date))

    data = {'Fecha': period_list,
        indicador: value_list}
    df = pd.DataFrame(data, columns=['Fecha', indicador])

    return df

def dataCleaning(df):
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df.dropna()
    return df

def tasaCrecimiento(df, columna):
    tasa_crecimiento_list = [NaN]
    for i in range(1, len(df[columna]-1)):
        v2 = df.iloc[i][columna]
        v1 = df.iloc[i-1][columna]
        tasa_crecimiento = ((v2-v1)/v1)*100
        tasa_crecimiento_list.append(tasa_crecimiento)
    df['Tasa Crecimiento'] = tasa_crecimiento_list    
    return df

def text_format(val):
    color = 'white'
    if (val == 'Crisis'):
      color = '#ff0000'
    elif (val == 'Alerta'):
      color = '#ffff00'
    return 'background-color: %s' % color

def espisodios(df, columns_names):
    df['Media Movil']=df[columns_names[-1]].rolling(window=8).mean()
    df['D.E']=df[columns_names[-1]].rolling(window=8).std()
    df['Sistem Alertas'] = (df[columns_names[-1]]-df['Media Movil'])/df['D.E']
    conditionlist = []

    if(columns_names[0] == 'liquidez' or columns_names[0] == 'solvencia' or columns_names[0] == 'reservas_internacionales' or columns_names[0] == 'PIB' or columns_names[0] == 'inversion_de_portafolio'):
        conditionlist = [
            ((-1.5 >= df['Sistem Alertas'])) & ((df['Sistem Alertas'] > -2.0)),
            (-2.0 >= df['Sistem Alertas']),
            (-1.5 < df['Sistem Alertas'])]
    # Indicadores en alerta y crisis con calores positivos
    else:
        conditionlist = [
            ((1.5 <= df['Sistem Alertas'])) & ((df['Sistem Alertas'] < 2.0)),
            (2.0 <= df['Sistem Alertas']),
            (1.5 > df['Sistem Alertas'])]


    choicelist = ['Alerta', 'Crisis', 'Sin Episodio']
    df['Episodio'] = np.select(conditionlist, choicelist, default='Not Specified')
    return df

