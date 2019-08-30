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

def section(title, content, gray=False):
    return html.Section(className=f'section is-medium {"has-background-grey-lighter" if gray else ""}', children=[
        html.Div(className='container', children=[
            html.H2(title, className='title is-2'),
        ] + content)
    ])

def point_list(items):
    return html.Ul([html.Li(item) for item in items])

def first():
    return html.Section(className='hero is-fullheight', children=[
        html.Div(className='hero-body', children=[
            html.Div(className='container', children=[
                html.Div(className='columns is-vcentered', children=[
                    html.Div(className='column is-5', children=[
                        html.Figure(className='image is-4by4', children=[
                            html.Img(src='/assets/logo.png', alt='FabLab UTFSM'),
                        ]),
                    ]),
                    html.Div(className='column is-5 main-title', children=[
                        html.H1('Informe de Gestión de Operaciones', className='title')
                    ])
                ])
            ]),
        ])
    ])

def last():
    return html.Footer(className='footer has-background-white', children=[
        html.Div(className='content has-text-centered', children=[
            html.Img(src='/assets/footer.png', alt='FabLab UTFSM'),
            html.P(className='is-size-7', children=[
                'FabLab UTFSM 2019', html.Br(),
                'UTFSM Campus San Joaquín, Edificio C', html.Br(),
                'Av. Vicuña Mackenna 3939, Santiago de Chile', html.Br(),
                'Desarrollado bajo licencia MIT'
            ])
        ])
    ])

def fig_records(df, months=None, stacked=False):
    machine_list = df['Tipo Máquina'].unique()

    def create_frame(df, serie_name):
        count = df['Tipo Máquina'].value_counts()
        frame = pd.DataFrame({'Tipo de Máquina': machine_list})
        frame[serie_name] = [count.get(machine, 0) for machine in machine_list]
        return frame

    cdf = None
    extras = {'barmode': 'relative' if stacked else 'group'}

    figure = go.Figure()
    for m in months:
        name = MONTH_NAMES[m-1]
        frame = create_frame(df[df.index.month == m], name)
        figure.add_trace(go.Bar(x=frame['Tipo de Máquina'], y=frame[name], name=name, hoverinfo='name+y'))
    
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

def fig_hours(df, months=None, stacked=False):
    machine_list = df['Tipo Máquina'].unique()

    def create_frame(df, serie_name):
        count = df.groupby('Tipo Máquina').sum()['Tiempo de uso en minutos'].divide(60).round(0)
        frame = pd.DataFrame({'Tipo de Máquina': machine_list})
        frame[serie_name] = [count.get(machine, 0) for machine in machine_list]
        return frame

    if months and type(months) == list:
        df = df[df.index.month.isin(months)]

    frame = create_frame(df, 'Total')

    figure = go.Figure()

    extras = {'barmode': 'relative' if stacked else 'group'}

    for m in months:
        name = MONTH_NAMES[m-1]
        frame = create_frame(df[df.index.month == m], name)
        figure.add_trace(go.Bar(y=frame['Tipo de Máquina'], x=frame[name], name=name, hoverinfo='name+x', orientation='h'))

    if stacked and months:
        frame = create_frame(df[df.index.month.isin(months)], 'Total')
        figure.add_trace(go.Scatter(
            y=frame['Tipo de Máquina'],
            x=frame['Total'],
            text=frame['Total'],
            textposition='middle right',
            mode='text',
            showlegend=False,
            hoverinfo='skip'
        ))
    
    figure.update_layout(xaxis={ 'title': f'Horas de uso {"total" if stacked else ""}'}, **extras)

    return figure

def records_per_machine(df, months=None, stacked=False):
    return dcc.Graph(figure=fig_records(df, months=months, stacked=stacked))

def time_per_machine(df, months=None, stacked=False):
    return dcc.Graph(figure=fig_hours(df, months=months, stacked=stacked))