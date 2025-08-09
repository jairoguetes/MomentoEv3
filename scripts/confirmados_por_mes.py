import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

#Rutas
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/COVID-19.xlsx')
OUTPUT_DIR = '../data/graficos/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cargar datos requeridos
df = pd.read_excel(
    DATA_PATH,
    usecols=['COVID-19', 'FECHA DEFUNCIÓN'],
    dtype={'COVID-19': str}
)

#Convertir fechas en formato día/mes/año
df['FECHA'] = pd.to_datetime(
    df['FECHA DEFUNCIÓN'],
    dayfirst=True,
    errors='coerce'
)

#Filtrar por 2020 y casos confirmados
df_2020 = df[
    (df['FECHA'].dt.year == 2020) &
    (df['COVID-19'] == 'CONFIRMADO')
].copy()

#Agrupar por mes
df_mensual = df_2020.resample('M', on='FECHA').size().reset_index(name='MUERTES')

#Configuración del gráfico
plt.figure(figsize=(12, 6))

#Estilos del grafico
plt.plot(
    df_mensual['FECHA'],
    df_mensual['MUERTES'],
    marker='o',
    linestyle='-',
    color='#e63946',
    linewidth=2,
    markersize=8,
    markeredgecolor='black',
    markerfacecolor='white'
)

#Títulos y formato
plt.title('EVOLUCIÓN MENSUAL DE MUERTES COVID-19 (2020)\nCasos Confirmados')
plt.xlabel('Mes')
plt.ylabel('Total de muertes')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(
    df_mensual['FECHA'],
    [fecha.strftime('%b') for fecha in df_mensual['FECHA']],
    rotation=45,
    ha='right'
)

#Etiquetas de valores
for fecha, muertes in zip(df_mensual['FECHA'], df_mensual['MUERTES']):
    plt.text(
        fecha,
        muertes + max(df_mensual['MUERTES']) * 0.02,
        f'{muertes:,}'.replace(',', '.'),
        ha='center',
        va='bottom',
        fontsize=9
    )

#exportar gráfico
output_path = os.path.join(OUTPUT_DIR, 'linea_muertes_covid_2020.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()

print(" Grafico guardado en data/graficos/linea_muertes_covid_2020.png ")