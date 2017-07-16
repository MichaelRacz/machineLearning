from sklearn.model_selection import GridSearchCV
from sklearn import svm, neighbors, preprocessing
import app.wine_domain.database as database
from app.api.logger import logger
from numpy import array
from threading import Lock

n_jobs = 4
pre_dispatch = '10000*n_jobs'

class ClassifierFactory:
    def __init__(self):
        self._svc = None
        self._nearest_neighbor = None
        self._lock = Lock()

    def create_svc_classifier(self):
        if self._svc is None:
            self._lock.acquire()
            try:
                training_set, training_set_classes = self._load_training_set()
                classifier = self._create_svc_classifier()
                self._fit_classifier(classifier, training_set, training_set_classes)
                self._svc = ClassifierAdapter(classifier)
            finally:
                self._lock.release()
        return self._svc

    def create_nearest_neighbor_classifier(self):
        if self._nearest_neighbor is None:
            self._lock.acquire()
            try:
                training_set, training_set_classes = self._load_training_set()
                scaled_training_set, scaler = self._scale_training_set(training_set)
                classifier = self._create_nearest_neighbor_classifier()
                self._fit_classifier(classifier, scaled_training_set, training_set_classes)
                self._nearest_neighbor = ClassifierAdapter(classifier, scaler)
            finally:
                self._lock.release()
        return self._nearest_neighbor

    def _load_training_set(self):
        training_set = []
        training_set_classes = []
        for classified_wine in database.read_all():
            training_set.append(_convert_to_list(classified_wine['wine']))
            training_set_classes.append(classified_wine['wine_class'])
        return array(training_set), array(training_set_classes)

    def _scale_training_set(self, training_set):
        scaler = preprocessing.StandardScaler().fit(training_set)
        return scaler.transform(training_set), scaler

    def _create_svc_classifier(self):
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

    def _create_nearest_neighbor_classifier(self):
        common_parameters = {
            'n_neighbors': range(2, 30),
            'weights': ['uniform', 'distance'],
            'algorithm': ['ball_tree', 'kd_tree', 'brute']}
        hyper_parameter_grid = [
            {**common_parameters, **{'metric': ['manhattan', 'euclidean', 'chebyshev']}},
            {**common_parameters, **{'metric': ['minkowski'], 'p': [3, 4]}}]
        classifier = GridSearchCV(neighbors.KNeighborsClassifier(), hyper_parameter_grid, scoring='accuracy',
            n_jobs=n_jobs, pre_dispatch=pre_dispatch, cv=5)
        return classifier

    def _fit_classifier(self, classifier, training_set, training_set_classes):
        classifier.fit(training_set, training_set_classes)
        logger.info('initialized classifier with params: {}'.format(classifier.best_params_))

classifier_factory = ClassifierFactory()

class ClassifierAdapter:
    def __init__(self, classifier, scaler=None):
        self._classifier = classifier
        self._scaler = scaler

    def predict_class(self, wine):
        wine_list = array(_convert_to_list(wine)).reshape(1, -1)
        if self._scaler is not None:
            wine_list = self._scaler.transform(wine_list)
        prediction = self._classifier.predict(wine_list)
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
