import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuración de rutas
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/COVID-19.xlsx')

# Carga y procesamiento de datos requeridos
df = pd.read_excel(DATA_PATH)
df_confirmed = df[df['COVID-19'] == 'CONFIRMADO'].copy()
df_confirmed['FECHA DEFUNCIÓN'] = pd.to_datetime(df_confirmed['FECHA DEFUNCIÓN'], dayfirst=True)

# Filtrado para el año 2021
df_2021 = df_confirmed[df_confirmed['FECHA DEFUNCIÓN'].dt.year == 2021]
deaths = df_2021['DEPARTAMENTO'].value_counts()

# Generación del gráfico
plt.figure(figsize=(12, 7))
deaths.plot(kind='bar', color='#e63946')
plt.title('Muertes por COVID-19 por departamento (2021)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('../data/graficos/Grafico1_Barras_Muertes_Confirmadas.png', dpi=120)
print(" Gráfico generado en data/graficos/resultado.png")