import pandas as pd
import funciones_union_e as fune

excel_doc = 'indicadores_trimestrales_UE.xlsx'
archivo_excel = pd.ExcelFile(excel_doc)
columns_names = archivo_excel.sheet_names

try:
    df_reservas = archivo_excel.parse(columns_names[0], index_col='Fecha')
    df_tipo_cambio = archivo_excel.parse(columns_names[1], index_col='Fecha')
    df_exportaciones = archivo_excel.parse(columns_names[2], index_col='Fecha')
    df_liquidez = archivo_excel.parse(columns_names[3], index_col='Fecha')
    df_solvencia = archivo_excel.parse(columns_names[4], index_col='Fecha')
    df_portafolio = archivo_excel.parse(columns_names[5], index_col='Fecha')
    df_deuda = archivo_excel.parse(columns_names[6], index_col='Fecha')
    df_PIB = archivo_excel.parse(columns_names[7], index_col='Fecha')
except:
    print('Error al cargar los datos')


indicadores_dolares = [df_reservas, df_PIB, df_portafolio]

#Calculo de tasas de crecimiento
for indicador in indicadores_dolares:
    columns_names = list(indicador.columns.values)
    indicador = fune.tasaCrecimiento(indicador, columns_names[-1])

#Deuda pública/ Exportaciones
df_deuda_export = df_deuda.join(df_exportaciones)
df_deuda_export['Deuda_Export'] = df_deuda_export['deuda_externa']/df_deuda_export['exportaciones']

indicadores_listos = [df_deuda_export, df_liquidez, df_solvencia, df_PIB, df_portafolio, df_reservas, df_tipo_cambio]

writer = pd.ExcelWriter('episodios_indicadores_UE.xlsx')

for indicador in indicadores_listos:
    columns_names = list(indicador.columns.values)
    indicador = fune.espisodios(indicador, columns_names)
    indicador = indicador.style.applymap(fune.text_format)
    indicador.to_excel(writer, sheet_name = columns_names[0])

writer.save()

print('se calcularon y guardaron los episodios de los indicadores')

