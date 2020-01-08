"""
Module to store, load an preprocess (training) data. ##TODO: preprocess data better in nlu not here?
"""
import pandas as pd

# load training data
class TrainDataLoader:
    def __init__(self):
        pass

    def load(self, path_to_data):
        df = pd.read_csv(path_to_data, header=None, comment="#")

        pass
