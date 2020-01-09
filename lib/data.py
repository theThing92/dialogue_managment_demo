"""
Module to store, load an preprocess (training) data.
"""
import pandas as pd

# load training data
class TrainDataLoader:
    def __init__(self, path_to_data="../data/Dialogs_Pizza.txt"):
        self.path_to_data = path_to_data
        self.data = self.load()

    def load(self):
        df = pd.read_csv(self.path_to_data,
                         header=None,
                         comment="#",
                         names =["PREV_SYSTEM_ACTION",
                                 "TypeOrder",
                                 "NumberPizzas",
                                 "TypesPizzas",
                                 "SizesPizzas",
                                 "TypesDoughs",
                                 "Drinks",
                                 "Acceptance",
                                 "Rejection",
                                 "NotUnderstood",
                                 "SYSTEM_ACTION"])

        # select subset of data for simplicity
        valid_system_reactions = [1,3,4,5,9,10,11,14]
        df = df[df["PREV_SYSTEM_ACTION"].isin(valid_system_reactions) & df["SYSTEM_ACTION"].isin(valid_system_reactions)]

        df.TypeOrder = 0
        df.TypesDoughs = 0
        df.Drinks = 0


        return df


if __name__ == "__main__":
    tdl = TrainDataLoader()
    df = tdl.data
