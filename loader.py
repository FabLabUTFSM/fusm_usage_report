import pandas as pd
import pathlib


def load_data(file_name):  
    DATA_PATH = pathlib.Path(__file__).parent.joinpath('data').resolve()
    data = pd.read_csv(DATA_PATH.joinpath(file_name))
    return data

def load_copy(file_name):
    DATA_PATH = pathlib.Path(__file__).parent.resolve()
    with open(DATA_PATH.joinpath(file_name)) as text_file:
        return text_file.read()