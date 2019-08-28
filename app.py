import dash
import dash_core_components as dcc
import dash_html_components as html

from loader import load_data
from generators import section, records_per_machine, header
from transform import shape_data

data = load_data('uso_maquinas_2308.csv')
data = shape_data(data)

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width", "encoding": "UTF-8"}])
server = app.server

app.layout = html.Div([
    header(),
    section('Metodología', []),
    section('Usos por máquina', [
        records_per_machine(data, month=8, compare_with=7),
        records_per_machine(data, month=8, compare_with=7, stacked=True)
    ]),
    section('Horas de uso', []),
    section('Capacidad utilizada', [])
])

if __name__ == "__main__":
    app.run_server(debug=True)