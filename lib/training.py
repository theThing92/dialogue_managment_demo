"""
Module for training statistical DM models.
"""
from data import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import pandas as pd
from joblib import dump,load

class Trainer:
    def __init__(self, model_type="svm"):
        self.model_type = model_type
        self.model = None

    def train(self, X, y, parameters, scores):


        if self.model_type == "svm":

            for score in scores:
                print("# Tuning hyper-parameters for %s" % score)
                print()

                clf = GridSearchCV(
                    SVC(), parameters, scoring='%s_micro' % score
                )
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                clf.fit(X_train, y_train)

                print("Best parameters set found on development set:")
                print()
                print(clf.best_params_)
                print()
                print("Grid scores on development set:")
                print()
                means = clf.cv_results_["mean_test_score"]
                stds = clf.cv_results_["std_test_score"]
                for mean, std, params in zip(means, stds, clf.cv_results_['params']):
                    print("%0.3f (+/-%0.03f) for %r"
                          % (mean, std * 2, params))
                print()

                print("Detailed classification report:")
                print()
                print("The model is trained on the full development set.")
                print("The scores are computed on the full evaluation set.")
                print()
                y_true, y_pred = y_test, clf.predict(X_test)
                print(classification_report(y_true, y_pred))
                print()

            self.model = clf

    def predict(self, X):
        if self.model is not None:
            return self.model.predict(X)

        else:
            raise Exception("Empty model detected, please use the train method to fit the model on the given data.")

    def save(self, model_path="../data/stat_model.joblib"):
        if self.model is not None:
            dump(self.model, model_path)

        else:
            raise Exception("Empty model detected, please use the train method to fit the model on the given data.")

    def load(self, model_path="../data/stat_model.joblib"):
        self.model = load(model_path)

        return self


if __name__ == "__main__":
    data = TrainDataLoader().data

    # get feature matrix and target variable
    X = data.drop(columns=["SYSTEM_ACTION"])
    y = data["SYSTEM_ACTION"]

    params_svm = {"kernel": ["rbf", "linear"], "gamma": [1e-3, 1e-4],"C": [1, 10, 100, 1000]}

    eval_metrics = ['f1']

    trainer = Trainer("svm")
    trainer.train(X, y, params_svm, eval_metrics)
    pd.DataFrame(trainer.model.cv_results_).to_excel("../data/cv_results_svm.xlsx")

    trainer.save()
    trainer.load()
