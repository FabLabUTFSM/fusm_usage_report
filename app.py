import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from loader import load_data
from generators import section, records_per_machine, time_per_machine, first, point_list, last, month_selector, machine_capacity, contexts#, uses
from transform import shape_data

records = load_data('uso_maquinas_2808.csv', shape_data)
capacity = load_data('capacidad_maquinas_2019.csv', index_col=0)

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server

app.title = 'FabLab UTFSM :: Informe de gestión de operaciones'

app.layout = html.Div(children=[
    first(),
    section('Metodología', [
        point_list([
            'Ingreso por parte del encargado de turno y respaldo con tabla de registro.',
            'Se registra inicio y fin de la tarea.',
            'No se utilizará la información del material utilizado.',
            'Categorización de la máquina se hace por tipo, no por instancia.',
            f'{len(records)} registros en total.'
        ]),
        month_selector(records, first_month=4)
    ], gray=True),
    section('Usos por máquina', [
        dcc.Tabs(id='records-per-machine-tabs', value='separate', children=[
            dcc.Tab(label='Separados', value='separate'),
            dcc.Tab(label='Acumulativos', value='stacked')
        ]),
        html.Div(id='records-per-machine-tab')
    ]),
    section('Horas de uso', [
        dcc.Tabs(id='time-per-machine-tabs', value='separate', children=[
            dcc.Tab(label='Separados', value='separate'),
            dcc.Tab(label='Acumulativos', value='stacked')
        ]),
        html.Div(id='time-per-machine-tab')
    ]),
    section('Capacidad utilizada', [
        html.P('La capacidad utilizada está calculada sobre un uso total del laboratorio de 8 horas diarias, 5 días a la semana.'),
        html.Div(id='machine-capacity')
    ]),
    #section('Distribución de usos', [
    #    html.Div(id='uses-distribution')
    #]),
    section('Uso por contexto', [
        html.Div(id='contexts-use')
    ]),
    section('Uso por estudiantes', [
        html.Div(id='students-use')
    ]),
    last()
])

@app.callback(Output('records-per-machine-tab', 'children'), [Input('records-per-machine-tabs', 'value'), Input('month-range-slider', 'value')])
def records_per_machine_tab_content(value, months):
    stacked = value == 'stacked'
    return records_per_machine(records, months=months, stacked=stacked)

@app.callback(Output('time-per-machine-tab', 'children'), [Input('time-per-machine-tabs', 'value'), Input('month-range-slider', 'value')])
def time_per_machine_tab_content(value, months):
    stacked = value == 'stacked'
    return time_per_machine(records, months=months, stacked=stacked)

@app.callback(Output('machine-capacity', 'children'), [Input('month-range-slider', 'value')])
def machine_capacity_content(months):
    return machine_capacity(records, capacity, months)

# @app.callback(Output('uses-distribution', 'children'), [Input('month-range-slider', 'value')])
# def uses_distribution_content(months):
#     return uses(records, months)

@app.callback(Output('contexts-use', 'children'), [Input('month-range-slider', 'value')])
def contexts_use_content(months):
    return contexts(records, months)

@app.callback(Output('students-use', 'children'), [Input('month-range-slider', 'value')])
def students_use_content(months):
    return contexts(records, months, level='Estudiante')

if __name__ == "__main__":
    app.run_server(debug=True)