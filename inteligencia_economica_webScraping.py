import requests
from lxml import html
import pandas as pd

#header necesario para evitar bloqueos
encabezados = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

#Función que extrae la información de cada url
def data_extraction(k,url):
    response= requests.get(url, headers=encabezados) #obtención del html de la url
    parser = html.fromstring(response.text) #Parseo del html

    #Empleo de xpath para extraer la información deseada: period, value, y obs. status dentro de la tabla
    info_extraction = parser.xpath("//table[@id = 'dataTableID']//td[contains(@class, 'light') or contains(@class, 'dark')]/text()")

    #Creación de listas que permitirán almacenar la información
    period_list, value_list, obs_status_list = [], [], []
    
    #Ciclo para separar la información
    for i in range(0,len(info_extraction), 3):
        element = info_extraction[i:i+3]
        period_list.append(element[0])
        value_list.append(element[1])
        obs_status_list.append(element[2])

    #Diccionario con la información
    data = {'Period': period_list,
        'Value': value_list,
        'Obs Status': obs_status_list}

    #Uso de la libreria pandas para crear un Data Frame
    df = pd.DataFrame(data, columns=['Period', 'Value', 'Obs Status'])

    #Guardando la información en archivos csv
    df.to_csv('data_'+k+'.csv')
    print("Se extrajo la información correspondiente a "+k)

urls = {
    'reservas_internacionales': "https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=340.RA6.M.N.U2.W1.S121.S1.LE.A.FA.R.F._Z.EUR.X1._X.N",
    'tipo_de_cambio': "https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=120.EXR.M.USD.EUR.SP00.A",
    'exportaciones': "https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=320.MNA.Q.N.I8.W1.S1.S1.D.P6._Z._Z._Z.EUR.LR.N",
    'liquidez': "https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=117.BSI.Q.U2.N.F.T00.A.4.Z5.0000.Z01.E",
    'solvencia': "https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=117.BSI.M.U2.N.A.A20.A.1.U2.1100.Z01.E",
    'inversion_de_portafolio': "https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.N.I8.W1.S1.S1.T.L.FA.P.F._Z.EUR._T.M.N",
    'deuda_externa': "https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.Q.N.I8.W1.S1.S1.LE.L.FA._T.FGED._Z.EUR._T._X.N",
    'PIB': "https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=320.MNA.Q.N.I8.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.V.N"
}

#Ciclo que permite recorrer las claves y valores del diccionario urls
for k, v in list(urls.items()):
    data_extraction(k,v) 