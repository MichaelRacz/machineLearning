from sklearn.model_selection import GridSearchCV
from sklearn import svm, preprocessing
import app.wine_domain.database as database
from app.api.logger import logger
from numpy import array

# TODO: remove
import numpy as np
from random import random

n_jobs = 4
pre_dispatch = '10000*n_jobs'
#TODO: are classifiers thread safe?, create class
classifiers = {}

def initialize_svc_classifier():
    global classifiers
    if 'svc' not in classifiers:
        training_set, training_set_classes = _load_training_set()
        classifier = _create_svc_classifier()
        _fit_classifier(classifier, training_set, training_set_classes)
        classifiers['svc'] = ClassifierAdapter(classifier)
    return classifiers['svc']

def _load_training_set():
    training_set = []
    training_set_classes = []
    for classified_wine in database.read_all():
        print('loaded: {}, class {}'.format(str(_convert_to_list(classified_wine['wine'])), classified_wine['wine_class']))
        training_set.append(_convert_to_list(classified_wine['wine']))
        training_set_classes.append(classified_wine['wine_class'])
    return array(training_set), array(training_set_classes)

def _scale_training_set(training_set):
    return preprocessing.normalize(training_set)
    #scaler = preprocessing.StandardScaler().fit(training_set)
    #return scaler.transform(training_set)

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
    logger.info('initialized classifier with params: {}'.format(classifier.best_params_))

class ClassifierAdapter:
    def __init__(self, classifier):
        self.classifier = classifier

    def predict_class(self, wine):
        wine_list = array(_convert_to_list(wine)).reshape(1, -1)
        print('predicting {}'.format(wine_list))
        prediction = self.classifier.predict(wine_list)
        print('prediction: {}'.format(str(prediction)))
        predicted_class = prediction[0]
        return predicted_class

def _convert_to_list(wine_dict):
    return [
        wine_dict['alcohol'],
        wine_dict['malic_acid'],
        wine_dict['ash'],
        wine_dict['alcalinity_of_ash'],
        wine_dict['magnesium'],
        wine_dict['total_phenols'],
        wine_dict['flavanoids'],
        wine_dict['nonflavanoid_phenols'],
        wine_dict['proanthocyanins'],
        wine_dict['color_intensity'],
        wine_dict['hue'],
        wine_dict['odxxx_of_diluted_wines'],
        wine_dict['proline']]
    #sorted_keys = sorted(wine_dict)
    #return [wine_dict[key] for key in sorted_keys]

def initialize(training_set, training_set_classes):
    global classifiers
    if 'svc' not in classifiers:
        #scaled_training_set = _scale_training_set(training_set)
        classifier = _create_svc_classifier()
        _fit_classifier(classifier, training_set, training_set_classes)
        classifiers['svc'] = ClassifierAdapter(classifier)
    return classifiers['svc']

if __name__ == '__main__':
    f = open("/home/yumyumfish/machineLearning/playground/wine.data")
    data = np.loadtxt(f, delimiter=',')
    X = data[:, 1:]
    y = data[:, 0]
    training_set = []
    training_set_classes = []
    test_set = []
    test_set_classes = []
    for i in range(0, len(data)):
        if random() < 0.7:
            training_set.append(X[i])
            training_set_classes.append(y[i])
        else:
            test_set.append(X[i])
            test_set_classes.append(y[i])
    print('training set: {}'.format(str (training_set)))
    print('training set classes: {}'.format(str(training_set_classes)))
    classifier = initialize(array(training_set), array(training_set_classes))
    success = 0
    for i in range(0, len(test_set)):
        prediction = classifier.classifier.predict(test_set[i].reshape(1, -1))
        if prediction[0] == test_set_classes[i]:
            success += 1
        print('predicted: {}, expected {}'.format(str(prediction), test_set_classes[i]))
    print('success rate: {}'.format(success / len(test_set)))