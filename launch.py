"""
Importar librerías
"""
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import cufflinks as cf

"""
EXTRACCIÓN DE DATOS
"""
# Definimos el tema de la visualización
cf.set_config_file(sharing='public', theme='pearl')

"""
TRANSFORMACIÓN Y MANIPULACIÓN DE DATOS
"""
# Cargar un archivo CSV en un DataFrame de Pandas
df_csv = pd.read_csv('e_learning_data.csv', encoding='latin')
# Borramos las filas con valores nulos
df_csv = df_csv.dropna()
# Convertir la columna Year al tipo datetime
df_csv['Year'] = pd.to_datetime(df_csv['Year'], format='%Y').dt.year
# Eliminar filas con valores nulos
df_csv = df_csv.dropna()
# Tabla pivote
df_csv_pivot = df_csv.pivot(
    index='Year',
    columns='Country',
    values='Total_Courses_Completed')
df_csv_pivot.tail()

"""
CARGA DE DATOS
"""
# Crear la figura de línea con cufflinks
fig_lineplot = df_csv_pivot.iplot(
    kind='line',
    xTitle='Year',
    yTitle='Total Courses Completed',
    title='Total Courses Completed by Country (1991-2024)',
    asFigure=True)

# Filtrar los datos por años de interés
df_barplot = df_csv_pivot[df_csv_pivot.index.isin([2008, 2009, 2010, 2011, 2012,
                                                   2013, 2014, 2015, 2016, 2017,
                                                   2018, 2019, 2020, 2021, 2022,
                                                   2023, 2024])]
# Crear la figura de barras con cufflinks
fig_barplot = df_barplot.iplot(
    kind='bar',
    xTitle='Year',
    yTitle='Total Courses Completed',
    title='Total Courses Completed by Country (2008-2024)',
    asFigure=True)

# Crear la figura de caja con cufflinks
fig_box = df_csv_pivot.iplot(kind='box',
                             xTitle='Country',
                             yTitle='Total Courses Completed',
                             title='Distribution of Courses Completed by Country',
                             asFigure=True)

# Crear la figura de histograma con cufflinks
fig_hist = df_csv_pivot[['USA', 'Mexico']].iplot(kind='hist',
                                      xTitle='Total Courses Completed',
                                      yTitle='Frequency',
                                      title='Distribution of Courses Completed in USA and Mexico',
                                      asFigure=True)

# Crear la figura de pastel con cufflinks
df_pie_2022 = df_csv_pivot.loc[2022]
# Reiniciar el índice para convertir el índice en una columna
df_pie_2022 = df_pie_2022.reset_index()
# Renombrar las columnas para mayor claridad
df_pie_2022.columns = ['Country', 'Total_Courses_Completed']
# Crear la gráfica de pastel
fig_pie = df_pie_2022.iplot(kind='pie',
                           labels='Country',
                           values='Total_Courses_Completed',
                           title='Total Courses Completed by Country in 2022',
                           asFigure=True)

# Crear la figura de dispersión con cufflinks
fig_scatter = df_csv_pivot.iplot(kind='scatter',
                                 mode='markers',
                                 xTitle='Year',
                                 yTitle='Total Courses Completed',
                                 title='Scatter Plot of Courses Completed by Year',
                                 asFigure=True)

# Crear la aplicación Dash
dash_app = Dash(__name__)
# Definir el layout de la aplicación
dash_app.layout = html.Div(children=[
    html.H1(children='Visualización de Cursos Completados por País'),
    dcc.Graph(
        id='line-graph',
        figure=fig_lineplot
    ),
    dcc.Graph(
        id='bar-graph',
        figure=fig_barplot
    ),
    dcc.Graph(
        id='box-graph',
        figure=fig_box
    ),
    dcc.Graph(
        id='hist-graph',
        figure=fig_hist
    ),
    html.H2(children='Datos de Cursos Completados por País'),
    dcc.Graph(
        id='pie-graph',
        figure=fig_pie
    ),
    dcc.Graph(
        id='scatter-graph',
        figure=fig_scatter
    )
])
# Ejecutar la aplicación
if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8053)