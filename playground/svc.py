from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import svm
import classification
import numpy as np
from random import random


"""
Dependencies:

pip3 install scipy
pip3 install numpy
pip3 install sklearn
"""

n_jobs = 4
pre_dispatch = '10000*n_jobs'

def create_svc_classifier(training_set, training_set_classes):
    # C = [2 ** i for i in range(-5, 20)]
    C = [10 ** i for i in range(-2, 3)]
    class_weight = [None, 'balanced']
    # gamma = [2.0 ** i for i in range(-15, 3)]
    gamma = [10 ** i for i in range(-4, 0)]
    gamma.append('auto')
    # C = [10,1000]
    # gamma = [1e-3, 1e-4]
    # scaling?
    # https://www.csie.ntu.edu.tw/~cjlin/libsvm/

    hyper_parameter_grid = [
        {'kernel': ['rbf'], 'C': C, 'class_weight': class_weight, 'gamma': gamma},
        {'kernel': ['linear'], 'C': C, 'class_weight': class_weight},
        {'kernel': ['poly'], 'C': C, 'class_weight': class_weight, 'gamma': gamma, 'degree': range(2, 5), 'coef0' : [0.0, 1.0]}] #,
        # {'kernel': ['sigmoid'], 'C': C, 'gamma': gamma}, #'coef0' : coef0},
        # {'kernel': ['precomputed'], 'C': C}]

    # TODO: iterate using diffenent scores, cv strategies
    score = 'recall_macro'
    classifier = GridSearchCV(svm.SVC(), hyper_parameter_grid, scoring=score,
        n_jobs=n_jobs, pre_dispatch=pre_dispatch, cv=5)

    classification.fit_classifier(classifier, training_set, training_set_classes)
    return classifier

def create_svc_classifier_random(training_set, training_set_classes):
    gamma = [2.0 ** i for i in range(-15, 3)]
    gamma.append('auto')

    hyper_parameter_distribution = {
        'kernel': ['poly', 'rbf', 'linear'],
        'C': [2 ** i for i in range(-5, 20)],
        'class_weight': [None, 'balanced'],
        'gamma': gamma,
        'degree': range(2, 7),
        'coef0' : [0.0, 1.0]}

    score = 'recall_macro'
    classifier = RandomizedSearchCV(svm.SVC(), hyper_parameter_distribution, scoring=score,
        n_jobs=n_jobs, pre_dispatch=pre_dispatch, cv=5, n_iter=200)

    classification.fit_classifier(classifier, training_set, training_set_classes)
    return classifier

def create_linear_svc_classifier(training_set, training_set_classes):
    C = [10 ** i for i in range(-2, 3)]
    multi_class = ['ovr', 'crammer_singer']
    class_weight = [None, 'balanced']

    hyper_parameter_grid = [
        {'C': C,
        'loss': ['squared_hinge', 'hinge'],
        'penalty': ['l2'],
        'dual': [True],
        'multi_class': multi_class,
        'class_weight': class_weight},
        {'C': C,
        'loss': ['squared_hinge'],
        'penalty': ['l1'],
        'dual': [False],
        'multi_class': multi_class,
        'class_weight': class_weight}]

    score = 'recall_macro'
    classifier = GridSearchCV(svm.LinearSVC(), hyper_parameter_grid, scoring=score,
        n_jobs=n_jobs, pre_dispatch=pre_dispatch, cv=5)

    classification.fit_classifier(classifier, training_set, training_set_classes)
    return classifier

def create_nu_svc_classifier(training_set, training_set_classes):
    nu = [0.1 * i for i in range(1,9)]
    class_weight = [None, 'balanced']
    decision_function_shape = ['ovr']
    gamma = [10 ** i for i in range(-4, 0)]
    gamma.append('auto')
    # C = [10,1000]
    # gamma = [1e-3, 1e-4]
    # scaling?
    # https://www.csie.ntu.edu.tw/~cjlin/libsvm/

    hyper_parameter_grid = [
        {'kernel': ['rbf'], 'nu': nu, 'class_weight': class_weight, 'decision_function_shape': decision_function_shape, 'gamma': gamma},
        {'kernel': ['linear'], 'nu': nu, 'class_weight': class_weight, 'decision_function_shape': decision_function_shape},
        {'kernel': ['poly'], 'nu': nu, 'class_weight': class_weight, 'decision_function_shape': decision_function_shape, 'gamma': gamma, 'degree': range(2, 5), 'coef0' : [0.0, 1.0]}] #,

    score = 'recall_macro'
    classifier = GridSearchCV(svm.NuSVC(), hyper_parameter_grid, scoring=score,
        n_jobs=n_jobs, pre_dispatch=pre_dispatch, cv=5)

    classification.fit_classifier(classifier, training_set, training_set_classes)
    return classifier

def load_wine():
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
    return training_set, training_set_classes, test_set, test_set_classes

if __name__ == '__main__':
    training_set, training_set_classes, test_set, test_set_classes = load_wine()
    print('size of training set: {}'.format(len(training_set)))
    print('size of test set: {}'.format(len(test_set)))
    # todo: different kernels
    print('svc')
    svc_classifier = create_svc_classifier(training_set, training_set_classes)
    classification.classify(svc_classifier, test_set, test_set_classes)
    print('svc random')
    # svc_classifier_random = create_svc_classifier_random(training_set, training_set_classes)
    # classify(svc_classifier_random, test_set, test_set_classes)
    print('linear svc')
    #linear_svc_classifier = create_linear_svc_classifier(training_set, training_set_classes)
    #classify(linear_svc_classifier, test_set, test_set_classes)
    print('nu svc')
    # nu_svc_classifier = create_nu_svc_classifier(training_set, training_set_classes)
    # classify(nu_svc_classifier, test_set, test_set_classes)
    # TODO: use + for list concatenation
