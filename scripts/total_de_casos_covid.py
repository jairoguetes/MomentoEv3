import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configuración de rutas y directorios
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/COVID-19.xlsx')
OUTPUT_DIR = '../data/graficos/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

#Carga de datos requeridos
df = pd.read_excel(
    DATA_PATH,
    usecols=['COVID-19', 'FECHA DEFUNCIÓN'],
    dtype={'COVID-19': str}
)

#Conversión de fechas en formato día/mes/año
df['FECHA'] = pd.to_datetime(
    df['FECHA DEFUNCIÓN'],
    dayfirst=True
)

#Filtrado para 2021 de las tres categorias
df_2021 = df[
    (df['FECHA'].dt.year == 2021) &
    (df['COVID-19'].isin(['CONFIRMADO', 'SOSPECHOSO', 'DESCARTADO']))
]

#Conteo de casos por categoría
conteo_casos = df_2021['COVID-19'].value_counts()

#Configuración del gráfico circular
plt.figure(figsize=(10, 8))
colors = ['#4e79a7', '#f28e2b', '#e15759']  # Paleta de colores

# Creación del pie chart
wedges, texts, autotexts = plt.pie(
    conteo_casos,
    labels=conteo_casos.index,
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    pctdistance=0.85,
    textprops={'fontsize': 12}
)

# Personalización
plt.setp(autotexts, color='white', weight='bold')
plt.setp(texts, fontsize=12)

# Círculo central
plt.gca().add_artist(plt.Circle((0, 0), 0.70, fc='white'))

# Título del gráfico
plt.title(
    'DISTRIBUCIÓN DE CASOS COVID-19 (2021)\n'
    'Confirmados vs Sospechosos vs Descartados',
    fontsize=14,
    pad=20
)

#exportar grafico
output_path = os.path.join(
    OUTPUT_DIR,
    f"pie_casos_covid_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
)
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()

print(f" Grafico guardado en data/graficos/pie_casos_covid_{datetime.now().strftime('%Y%m%d_%H%M')}.png")