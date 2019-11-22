import pandas as pd

def fix_date_columns(dataframe):
    # Separa la columna de Marca temporal en dos columnas de fecha y hora de ingreso
    insert_cols = dataframe['Marca temporal'].str.split(' ', n=1, expand=True)
    dataframe['Fecha ingreso'] = insert_cols[0]
    dataframe['Hora ingreso'] = insert_cols[1]
    dataframe['Fecha'].fillna(dataframe['Fecha ingreso'], inplace=True)
    dataframe['Hora Termino'] = pd.to_datetime(dataframe['Hora Termino'])
    dataframe['Hora Inicio'] = pd.to_datetime(dataframe['Hora Inicio'])
    dataframe.index = pd.to_datetime(dataframe['Marca temporal'], dayfirst=True)
    return dataframe.drop(columns=['Marca temporal'])


def context_columns(dataframe):
    dataframe['Contexto del uso'].replace('Desarrollo Interno', 'Interno/Desarrollo', inplace=True)
    dataframe['Contexto del uso'].replace(r'.*cirqoid', 'Interno/Desarrollo', inplace=True, regex=True)
    dataframe['Contexto del uso'].replace(r'[Cc]oncurs?o [Hh]alloween', 'Estudiante/Concurso', inplace=True, regex=True)
    context_cols = dataframe['Contexto del uso'].str.split('/', expand=True)
    dataframe['Contexto 1'] = context_cols[0]
    dataframe['Contexto 2'] = context_cols[1]
    dataframe['Contexto 3'] = context_cols[2]
    return dataframe.drop(columns=['Contexto del uso'])


def split_machines(dataframe):
    machines = dataframe['Maquina usada'].str.split(' - ', expand=True)
    dataframe['Tipo Máquina'] = machines[0]
    dataframe['ID Máquina'] = machines[1]
    dataframe['Tipo Máquina'].replace('Cortadora Laser', 'Cortadora Láser', inplace=True)
    dataframe['Tipo Máquina'].replace('Bodor', 'Cortadora Láser', inplace=True)
    return dataframe.drop(columns=['Maquina usada'])

def drop_unused(dataframe):
    return dataframe.drop(columns=[
        'Usuario de la máquina', 
        'Material usado', 
        'Comentarios', 
        'El material utilizado fue:', 
        'Si el material fue facilitado por FabLab, especificar cuanto se utilizó ', 
        'Quién solicito el trabajo?',
        'Unnamed: 14'])

def round_decimals(dataframe):
    col = 'Tiempo de uso en minutos'
    dataframe[col] = [x.replace(',', '.') for x in dataframe[col]]
    dataframe[col] = dataframe[col].astype(float)
    return dataframe.round({col: 0})

def shape_data(raw_data):
    # Aplica todas las transformaciones iniciales
    data = fix_date_columns(raw_data)
    data = context_columns(data)
    data = split_machines(data)
    data = drop_unused(data)
    data = round_decimals(data)
    return data