import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def section(title, content):
    return html.Div([
        html.H2(title),
        html.Div(content)
    ])

def header():
    return html.H1('FabLab UTFSM')

def records_per_machine(df, month=None, compare_with=None, stacked=False):
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    machine_list = df['Tipo Máquina'].unique()

    def create_frame(df):
        count = df['Tipo Máquina'].value_counts()
        frame = pd.DataFrame({'Tipo de Máquina': machine_list})
        frame['Cantidad'] = [count.get(machine, 0) for machine in machine_list]
        frame.columns = ['Tipo de Máquina', 'Registros']
        return frame

    cdf = None
    extras = {}

    if month and type(month) == int:
        mdf = df[df.index.month == month]
        if compare_with and type(compare_with) == int:
            cdf = df[df.index.month == compare_with]
        df = mdf

    if cdf is not None:
        compare_frame = create_frame(cdf)
        compare_frame['Mes'] = months[compare_with-1]
        count_frame = create_frame(df)
        count_frame['Mes'] = months[month-1]
        display_frame = pd.concat([compare_frame, count_frame])
        extras.update({
            'color': 'Mes', 
            'barmode':'relative' if stacked else 'group'
        })
    else:
        display_frame = create_frame(df)

    return dcc.Graph(
        figure=px.bar(display_frame, x='Tipo de Máquina', y='Registros', text='Registros', **extras),
        config={'displaylogo': False}
    )