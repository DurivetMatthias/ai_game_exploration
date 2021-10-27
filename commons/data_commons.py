from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

from sklearn import model_selection

from sklearn.model_selection import cross_val_score

from sklearn.metrics import classification_report, confusion_matrix


def flatten(_list):

    return [item for sublist in _list for item in sublist]


def input_labels_split(*, df, label_column='label'):
    X = df.drop(label_column, axis=1)
    y = df[label_column]
    return X, y


def train_test_split(*, X, y, test_size=0.33):
    return model_selection.train_test_split(X, y, test_size=test_size, random_state=123)


def load_data_from_csv(file_path, column_names=None):
    return pd.read_csv(file_path, names=column_names)


def one_hot_encode(*, X):
    onehotencoder = OneHotEncoder()
    onehotencoder.fit(X)
    encoded_X = onehotencoder.transform(X).toarray()
    decoded = onehotencoder.inverse_transform(encoded_X)
    print(onehotencoder.categories_)
    return encoded_X, onehotencoder
