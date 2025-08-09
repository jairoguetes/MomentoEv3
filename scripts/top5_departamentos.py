import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Rutas
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/COVID-19.xlsx')
OUTPUT_DIR = '../data/graficos/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

#Carga de datos requeridos
df = pd.read_excel(
    DATA_PATH,
    usecols=['COVID-19', 'MUNICIPIO', 'FECHA DEFUNCIÓN'],
    dtype={'MUNICIPIO': str, 'FECHA DEFUNCIÓN': str}
)

# Conversión de fechas con formato día/mes/año
df['FECHA'] = pd.to_datetime(df['FECHA DEFUNCIÓN'], dayfirst=True, errors='coerce')

#Filtrado de datos (confirmados en 2021)
df_2021 = df[
    (df['COVID-19'] == 'CONFIRMADO') &
    (df['FECHA'].dt.year == 2021) &
    (df['MUNICIPIO'].notna())
].copy()

# Selección del Top 5 municipios
top5 = (
    df_2021['MUNICIPIO']
    .value_counts()
    .nlargest(5)
    .sort_values()  # Orden ascendente
)

# Configuración del gráfico
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(12, 6))

# Paleta de colores profesional
colors = plt.cm.viridis(np.linspace(0.3, 0.9, 5))

# Gráfico de barras horizontales
top5.plot(kind='barh', color=colors, width=0.7, edgecolor='gray')

# Personalización del gráfico
ax.set_title(
    'TOP 5 MUNICIPIOS - MUERTES COVID-19 CONFIRMADAS (2021)',
    fontsize=14,
    pad=20,
    loc='left'
)
ax.set_xlabel('Número de fallecidos', fontsize=10)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Añadir etiquetas de datos
for i, (municipio, conteo) in enumerate(top5.items()):
    ax.text(
        conteo + max(top5) * 0.02,
        i,
        f'{conteo:,}'.replace(',', '.'),
        va='center',
        fontsize=10
    )

#Exportar el gráfico
output_path = os.path.join(OUTPUT_DIR, 'top5_municipios_2021.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(" Grafico guardado en data/graficos/top5_municipios_2021.png ")