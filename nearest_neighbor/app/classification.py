from numpy import array
from sklearn import neighbors, preprocessing
from sklearn.model_selection import GridSearchCV
from classification_contract.messages import load_classified_wines

n_jobs = 4
pre_dispatch = '10000*n_jobs'
classifier = None
scaler = None

def init(hosts, topic):
    global classifier, scaler
    if classifier is None:
        classifier, scaler = _initialize_classifier(hosts, topic)

def _initialize_classifier(hosts, topic):
    classified_wines = load_classified_wines(hosts, topic)
    training_set, training_set_classes = _prepare_training_set(classified_wines)
    scaled_training_set, scaler = _scale_training_set(training_set)
    classifier = _create_classifier()
    classifier.fit(scaled_training_set, training_set_classes)
    return classifier, scaler

def _prepare_training_set(classified_wines):
    training_set = []
    training_set_classes = []
    for classified_wine in classified_wines:
        training_set.append(_convert_to_list(classified_wine['wine']))
        training_set_classes.append(classified_wine['wine_class'])
    return array(training_set), array(training_set_classes)

def _scale_training_set(training_set):
    scaler = preprocessing.StandardScaler().fit(training_set)
    return scaler.transform(training_set), scaler

def _create_classifier():
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

def predict_class(wine):
    wine_list = array(_convert_to_list(wine)).reshape(1, -1)
    wine_list = scaler.transform(wine_list)
    prediction = classifier.predict(wine_list)
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
