import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

from utils import MONTH_NAMES


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

def fig_records(df, months=None, stacked=False):
    machine_list = df['Tipo Máquina'].unique()

    def create_frame(df, serie_name):
        count = df['Tipo Máquina'].value_counts()
        frame = pd.DataFrame({'Tipo de Máquina': machine_list})
        frame[serie_name] = [count.get(machine, 0) for machine in machine_list]
        return frame

    cdf = None
    extras = {'barmode': 'relative' if stacked else 'group'}

    frame = create_frame(df, 'Total')
    figure = go.Figure()
    for m in months:
        name = MONTH_NAMES[m-1]
        frame = create_frame(df[df.index.month == m], name)
        figure.add_trace(go.Bar(x=frame['Tipo de Máquina'], y=frame[name], name=name, hoverinfo='y'))
    
    if stacked and months:
        frame = create_frame(df[df.index.month.isin(months)], 'Total')
        figure.add_trace(go.Scatter(
            x=frame['Tipo de Máquina'],
            y=frame['Total'],
            text=frame['Total'],
            textposition='top center',
            mode='text',
            showlegend=False,
            hoverinfo='skip'
        ))
    figure.update_layout(yaxis={ 'title': 'Número de registros'}, **extras)

    return figure

def records_per_machine(df, month=None, compare_with=None, stacked=False):
    months = None
    if month:
        months = [month,]
    if compare_with:
        months.append(compare_with)
    return dcc.Graph(
        figure=fig_records(df, months=months, stacked=stacked)
    )