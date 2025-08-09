import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# Configuración de rutas y directorios
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/COVID-19.xlsx')
OUTPUT_DIR = '../data/graficos/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

#Carga selectiva de datos
df = pd.read_excel(
    DATA_PATH,
    usecols=['COVID-19', 'FECHA DEFUNCIÓN', 'EDAD FALLECIDO'],
    dtype={'EDAD FALLECIDO': str}
)

# Procesamiento de edades
df['EDAD'] = df['EDAD FALLECIDO'].str.extract(r'(\d+)')[0].astype(float)

# Filtrado para 2020 (casos confirmados con edad válida)
df['FECHA'] = pd.to_datetime(df['FECHA DEFUNCIÓN'], dayfirst=True)
df_2020 = df[
    (df['FECHA'].dt.year == 2020) &
    (df['COVID-19'] == 'CONFIRMADO') &
    (df['EDAD'].notna())
].copy()

#Creación de grupos de edad
bins = list(range(0, 95, 5)) + [120]
labels = [f"{i}-{i+4}" for i in range(0, 90, 5)] + ["90+"]
df_2020['GRUPO_EDAD'] = pd.cut(
    df_2020['EDAD'],
    bins=bins,
    labels=labels,
    right=False
)

# Conteo por grupos de edad
conteo_edades = df_2020['GRUPO_EDAD'].value_counts().sort_index()

# Configuración del gráfico de barras
plt.figure(figsize=(14, 7))
bars = plt.bar(
    conteo_edades.index.astype(str),
    conteo_edades.values,
    color='#3a7ca5',
    edgecolor='white',
    linewidth=0.7,
    width=0.85
)

# estilos del grafico
plt.title('Distribución de muertes COVID-19 por edad (2020)')
plt.xlabel('Grupo de Edad (años)')
plt.ylabel('Número de Fallecidos')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle=':', alpha=0.4)

# agregamos etiquetas de valores
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + max(conteo_edades)*0.01,
        f'{int(height):,}'.replace(',', '.'),
        ha='center',
        va='bottom',
        fontsize=9
    )

#Exportación del gráfico
output_path = os.path.join(OUTPUT_DIR, 'histograma_edades_2020.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()

print(" Grafico guardado en data/graficos/histograma_edades_2020.png ")