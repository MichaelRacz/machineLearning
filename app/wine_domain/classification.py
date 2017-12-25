from sklearn.model_selection import GridSearchCV
from sklearn import svm, neighbors, preprocessing
from common.app.logger import logger
from numpy import array
from threading import Lock
import app.wine_domain.distributed_log as distributed_log

n_jobs = 4
pre_dispatch = '10000*n_jobs'

class ClassifierFactory:
    def __init__(self):
        self._svc = None
        self._nearest_neighbor = None
        self._lock = Lock()

#-------------
#nn

    def create_nearest_neighbor_classifier(self):
        self._lock.acquire()
        try:
            if self._nearest_neighbor is None:
                training_set, training_set_classes = self._load_training_set()
                scaled_training_set, scaler = self._scale_training_set(training_set)
                classifier = self._create_nearest_neighbor_classifier()
                classifier.fit(training_set, training_set_classes)
                self._nearest_neighbor = ClassifierAdapter(classifier, scaler)
        finally:
            self._lock.release()
        return self._nearest_neighbor

    def _scale_training_set(self, training_set):
        scaler = preprocessing.StandardScaler().fit(training_set)
        return scaler.transform(training_set), scaler

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

    def _load_training_set(self):
        training_set = []
        training_set_classes = []
        classified_wines = distributed_log.read().values
        for classified_wine in classified_wines:
            training_set.append(_convert_to_list(classified_wine['wine']))
            training_set_classes.append(classified_wine['wine_class'])
        return array(training_set), array(training_set_classes)

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
