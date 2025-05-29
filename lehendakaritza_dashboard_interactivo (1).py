
import pandas as pd
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px

# Cargar los datos
df = pd.read_excel("export_20250529081355.xls.xlsx")

# Crear la app Dash
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Dashboard Lehendakaritza"),
    html.Div([
        html.Label("Centro Orgánico"),
        dcc.Dropdown(
            options=[{"label": i, "value": i} for i in df["Centro Orgánico"].unique()],
            id="centro-dropdown",
            multi=True
        ),
    ]),
    dcc.Graph(id="sunburst"),
    dash_table.DataTable(
        id="tabla",
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        style_table={'overflowX': 'auto'}
    )
])

# Callbacks
@app.callback(
    Output("sunburst", "figure"),
    Output("tabla", "data"),
    Input("centro-dropdown", "value")
)
def update_output(centros):
    if centros:
        filtered_df = df[df["Centro Orgánico"].isin(centros)]
    else:
        filtered_df = df

    fig = px.sunburst(
        filtered_df,
        path=["Centro Orgánico", "Escala Preferente", "Perfil Lingüístico"],
        values="Código",
        title="Distribución Funcional"
    )

    return fig, filtered_df.to_dict("records")

# Run the server
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=10000, debug=False)
