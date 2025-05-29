
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from dash import dash_table

# === Cargar datos desde Excel ===
EXCEL_FILE = 'export_20250529081355.xls.xlsx'
df = pd.read_excel(EXCEL_FILE, sheet_name='Sheet1')

# === Filtrar a Lehendakaritza ===
df = df[df['Departamento-Organismo Autónomo'] == 'LEHENDAKARITZA'].copy()
df['Perfil Lingüístico'] = pd.to_numeric(df['Perfil Lingüístico'], errors='coerce')
df['Centro Orgánico'] = df['Centro Orgánico'].str.strip()
df['Escala Preferente'] = df['Escala Preferente'].fillna('No especificada')

# === Crear app Dash ===
app = Dash(__name__)
app.title = "Dashboard Lehendakaritza"

app.layout = html.Div([
    html.H1("Dashboard Interactivo - Lehendakaritza"),

    html.Label("Selecciona un Centro Orgánico:"),
    dcc.Dropdown(
        id='centro-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(df['Centro Orgánico'].dropna().unique())],
        placeholder="Selecciona un centro o deja vacío para ver todos"
    ),

    dcc.Graph(id='heatmap-escalas'),
    dcc.Graph(id='sunburst-funcional'),

    html.H2("Tabla Interactiva de Puestos"),
    dash_table.DataTable(
        id='tabla-puestos',
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "5px"},
        style_header={"backgroundColor": "#f2f2f2", "fontWeight": "bold"}
    )
])

@app.callback(
    Output('heatmap-escalas', 'figure'),
    Output('sunburst-funcional', 'figure'),
    Output('tabla-puestos', 'data'),
    Input('centro-dropdown', 'value')
)
def actualizar_dashboard(centro):
    filtered = df if centro is None else df[df['Centro Orgánico'] == centro]

    heatmap_data = filtered.pivot_table(
        index='Escala Preferente',
        columns='Perfil Lingüístico',
        values='Código',
        aggfunc='count',
        fill_value=0
    )
    fig1 = px.imshow(
        heatmap_data,
        labels={'color': 'Nº Puestos'},
        title=f"Perfiles por Escala {'- ' + centro if centro else ''}"
    )

    fig2 = px.sunburst(
        filtered,
        path=['Centro Orgánico', 'Escala Preferente', 'Perfil Lingüístico'],
        values='Código',
        title="Jerarquía funcional por escala y perfil"
    )

    return fig1, fig2, filtered.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
