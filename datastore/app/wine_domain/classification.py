from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import svm, preprocessing
import app.wine_domain.database as database

def initialize_svc_classifier():
    training_set, training_set_classes = _load_training_set()
    scaled_training_set = _scale_training_set(training_set)
    classifier = _create_svc_classifier()
    _fit_classifier(classifier, scaled_training_set, training_set_classes)
    return classifier

def _load_training_set():
    training_set = []
    training_set_classes = []
    for wine in database.read_all():
        conversion.to_wine_property_list(wine)
        training_set_classes.append(wine.wine_class)
    return training_set, training_set_classes

def to_wine_property_list(wine):
    pass
    #return from_wine_property_dict_to_list(to_wine_property_dict(wine))

def from_wine_property_dict_to_list(wine_dict):
    sorted_keys = sorted(wine_dict)
    return [wine_dict[key] for key in sorted_keys]


def _scale_training_set(training_set):
    return training_set
    #scaler = preprocessing.StandardScaler().fit(training_set)
    #training_set = scaler.transform(training_set)

def _create_svc_classifier():
    C = [10 ** i for i in range(-2, 3)]
    class_weight = [None, 'balanced']
    gamma = [10 ** i for i in range(-4, 0)]
    gamma.append('auto')
    hyper_parameter_grid = [
        {'kernel': ['rbf'], 'C': C, 'class_weight': class_weight, 'gamma': gamma},
        {'kernel': ['linear'], 'C': C, 'class_weight': class_weight},
        {'kernel': ['poly'], 'C': C, 'class_weight': class_weight, 'gamma': gamma, 'degree': range(2, 5), 'coef0' : [0.0, 1.0]}]
    classifier = GridSearchCV(svm.SVC(), hyper_parameter_grid, scoring='recall_macro',
        n_jobs=n_jobs, pre_dispatch=pre_dispatch, cv=5)
    return classifier

def _fit_classifier(classifier, training_set, training_set_classes):
    classifier.fit(training_set, training_set_classes)
    print('best params: {}'.format(classifier.best_params_))
