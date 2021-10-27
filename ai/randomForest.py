from sklearn.model_selection import RandomizedSearchCV
from sklearn import ensemble
import pandas as pd
from commons.data_commons import *
from commons.pathlib_commons import *
from games.super_auto_pets import get_animals


def test_random_forest():
    df = load_data_from_csv("data/test.csv")

    for new_file_path in get_all_files("data/games"):
        new_df = load_data_from_csv(new_file_path)
        df = df.append(new_df, ignore_index=True)

    df['animals'] = (df['animal_0'] + ',' + df['animal_1'] + ',' +
                     df['animal_2'] + ',' + df['animal_3'] + ',' + df['animal_4']).str.split(',')
    df = df.drop(['animal_0', 'animal_1', 'animal_2',
                 'animal_3', 'animal_4'], axis=1)

    df = df.drop(['wins', 'losses'], axis=1)
    df = df.explode('animals')

    rfc = ensemble.RandomForestRegressor()

    X, y = input_labels_split(df=df, label_column='score')
    X, onehotencoder = one_hot_encode(X=X)

    # X_train, X_test, y_train, y_test = train_test_split(
    #     X=X, y=y)
    X_train = X
    y_train = y
    rfc.fit(X_train, y_train)

    get_animal_scores(rfc=rfc, onehotencoder=onehotencoder)
    best_rfc = tune_hyper_params(rfc=rfc, X_train=X_train, y_train=y_train)
    get_animal_scores(rfc=best_rfc, onehotencoder=onehotencoder)


def get_animal_scores(*, rfc, onehotencoder):
    X_manual = pd.DataFrame([
        [1, animal] for animal in get_animals()[0]
    ])

    X_manual = onehotencoder.transform(X_manual).toarray()
    predictions = rfc.predict(X_manual)
    animal_to_score = {
        onehotencoder.inverse_transform(features.reshape(1, -1))[0][1]: round(score, 2) for features, score in sorted(zip(X_manual, predictions), key=lambda x: x[1], reverse=True)
    }
    print(animal_to_score)
    return animal_to_score


def tune_hyper_params(*, rfc, X_train, y_train):
    n_estimators = [int(x) for x in np.linspace(start=10, stop=200, num=10)]
    max_features = ['auto', 'sqrt']
    max_depth = [int(x) for x in np.linspace(10, 200, num=10)]
    max_depth.append(None)
    random_grid = {
        'n_estimators': n_estimators,
        'max_features': max_features,
        'max_depth': max_depth
    }
    rfc_random = RandomizedSearchCV(estimator=rfc, param_distributions=random_grid,
                                    n_iter=100, cv=3, verbose=2, random_state=42, n_jobs=-1)
    rfc_random.fit(X_train, y_train)
    hyper_parameters = rfc_random.best_params_
    print(hyper_parameters)
    best_rfc = ensemble.RandomForestRegressor(
        n_estimators=hyper_parameters['n_estimators'],
        max_depth=hyper_parameters['max_depth'],
        max_features=hyper_parameters['max_features']
    )
    best_rfc.fit(X_train, y_train)
    return best_rfc
