import dash
import dash_core_components as dcc
import dash_html_components as html

from loader import load_data
from generators import section, records_per_machine, time_per_machine, first, point_list, last
from transform import shape_data

data = load_data('uso_maquinas_2808.csv')
data = shape_data(data)

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server

months = [6, 7, 8]

app.layout = html.Div(children=[
    first(),
    section('Metodología', [
        point_list([
            'Ingreso por parte del encargado de turno y respaldo con tabla de registro.',
            'Se registra inicio y fin de la tarea.',
            'No se utilizará la información del material utilizado.',
            'Categorización de la máquina se hace por tipo, no por instancia.',
            f'{len(data)} registros en total.'
        ])
    ], gray=True),
    section('Usos por máquina', [
        records_per_machine(data, months=months),
        records_per_machine(data, months=months, stacked=True)
    ]),
    section('Horas de uso', [
        time_per_machine(data, months=months),
        time_per_machine(data, months=months, stacked=True)
    ]),
    section('Capacidad utilizada', []),
    section('Media de tiempo de uso', []),
    section('Uso por contexto', []),
    section('Uso por estudiantes', []),
    last()
])


if __name__ == "__main__":
    app.run_server(debug=True)