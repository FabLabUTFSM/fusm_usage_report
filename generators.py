import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import math
from datetime import datetime, time

from utils import MONTH_NAMES, month_range

def section(title, content, gray=False):
    return html.Section(className=f'hero is-fullheight is-medium {"has-background-grey-lighter" if gray else ""}', children=[
        html.Div(className='hero-body', children=[
            html.Div(className='container', children=[
                html.Div(className='columns is-centered', children=[
                    html.Div(className='column is-four-fifths is-full-mobile', children=[
                        html.Div(className='level', children=[
                            html.H2(title, className='title')
                        ]),
                    ] + content)
                ])
            ])
        ])
    ])

def quality_index(df):
    indexes = df.sort_values('Valor', ascending=False).fillna('?').values
    return html.Div(className='columns is-multiline is-4 is-variable', children=[
        html.Div(className=f'column is-one-quarter index-container {"unknown-data" if i[1] == "?" else ""}', children=[
            html.H1(i[1], className='title'),
            html.H2(i[0], className='subtitle')
        ]) for i in indexes
    ])

def month_selector(df, first_month=None):
    current_month = datetime.now().month
    return html.Div(dcc.RangeSlider(
        id='month-range-slider',
        marks={i+1: MONTH_NAMES[i] for i in range(first_month-1, current_month)},
        min=first_month, max=current_month,
        value=[current_month-2,current_month],
        pushable=1
    ), className='slider-frame')

def point_list(items):
    return html.Ul([html.Li(item) for item in items])

def first():
    return html.Section(className='hero is-fullheight', children=[
        html.Div(className='hero-body', children=[
            html.Div(className='container', children=[
                html.Div(className='columns is-vcentered is-centered', children=[
                    html.Div(className='column is-5', children=[
                        html.Figure(className='image is-4by4', children=[
                            html.Img(src='/indicadores/assets/logo.png', alt='FabLab UTFSM'),
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
            html.Img(src='/indicadores/assets/footer.png', alt='FabLab UTFSM'),
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
    months = month_range(months)

    def create_frame(df, serie_name):
        count = df['Tipo Máquina'].value_counts()
        frame = pd.DataFrame({'Tipo de Máquina': machine_list})
        frame[serie_name] = [count.get(machine, 0) for machine in machine_list]
        return frame

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
    months=month_range(months)

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

def cap_per_machine_per_month(month_caps, machine, month):
    this_month = month_caps[month_caps['Mes'] == month]
    machine_count = {'Impresora 3D': 5, 'Cortadora Láser': 2, 'Router CNC': 3, 'Torno': 1, 'Cirqoid': 1}
    return (this_month['Dias'] * this_month['Horas']).values[0] * 60 * machine_count[machine]

def fig_total_capacity_2(df, month_caps, months):
    machine_list = df['Tipo Máquina'].unique()
    months = month_range(months)
    month_names = [MONTH_NAMES[m-1] for m in months]
    figure = go.Figure()
    for machine in machine_list:
        texts = []
        caps = []
        for month in months:
            total_cap = cap_per_machine_per_month(month_caps, machine, month)
            hours = total_cap // 60
            used_cap = df[df.index.month==month].groupby('Tipo Máquina')['Tiempo de uso en minutos'].sum().divide(total_cap).multiply(100).round(2).get(machine, 0)
            caps.append(used_cap)
            texts.append(f'{used_cap}% utilizado de una capacidad total de {hours} horas.')
        figure.add_trace(go.Bar(x=month_names, y=caps, name=machine, hovertext=texts))
    figure.update_layout(barmode='group', yaxis=dict(type='linear', ticksuffix='%', title='Capacidad Utilizada'))
    return figure

"""
TODO: Terminar el heatmap de alguna manera...
def fig_uses(df, months):
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    data = df[df.index.month.isin(month_range(months))]
    figure = go.Figure()
    times = data.groupby([data.index.weekday_name, pd.Grouper(freq='60min', key='Hora Inicio')]).fillna(0).sum().reset_index()
    day_times = times[times['Marca temporal'] == 'Monday']['Hora Inicio'].dt.time
    z_dict = dict()
    for i, d in enumerate(days):
        z_dict.update({dias[i]: times[times['Marca temporal'] == d]['Tiempo de uso en minutos'].fillna(0).values})
    z_values = pd.DataFrame(z_dict).values
    figure.add_trace(go.Heatmap(
        x=dias, 
        y=day_times,
        z=z_values))
    return figure
"""

def trace_context_use(df, level=None, **kwargs):
    grouped = None
    if not level:
        grouped = df.groupby('Contexto 1')
    else:
        grouped = df[df['Contexto 1'] == level].groupby('Contexto 2')
    context_data = grouped.sum()['Tiempo de uso en minutos']
    return go.Pie(labels=context_data.index, values=context_data.values, **kwargs)

def fig_contexts_use(df, months, level, **kwargs):
    col_count = 3
    row_count = math.ceil(len(month_range(months))/col_count)
    figure = make_subplots(row_count, col_count, specs=[[{'type':'domain'} for c in range(col_count)] for r in range(row_count)],
                    subplot_titles=[MONTH_NAMES[m-1] for m in month_range(months)])
    def take_month(months):
        for m in month_range(months):
            yield trace_context_use(df[df.index.month == m], level, name=MONTH_NAMES[m-1])
    pie_factory = take_month(months)
    try:
        for r in range(row_count):
            for c in range(col_count):
                figure.add_trace(next(pie_factory), r+1, c+1)
    except StopIteration as stop:
        pass
    return figure

def records_per_machine(df, months=None, stacked=False):
    return dcc.Graph(figure=fig_records(df, months=months, stacked=stacked), style={'height': '80vh'})

def time_per_machine(df, months=None, stacked=False):
    return dcc.Graph(figure=fig_hours(df, months=months, stacked=stacked), style={'height': '80vh'})

def machine_capacity(df, caps, months=None):
    return dcc.Graph(figure=fig_total_capacity_2(df, caps, months), style={'height': '80vh'})

#def uses(df, months):
#    return dcc.Graph(figure=fig_uses(df, months), style={'height': '80vh'})

def contexts(df, months, level=None):
    return dcc.Graph(figure=fig_contexts_use(df, months, level), style={'height': '80vh'})