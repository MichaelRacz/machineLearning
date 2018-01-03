from numpy import array
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from classification_contract.messages import load_classified_wines

n_jobs = 4
pre_dispatch = '10000*n_jobs'
classifier = None

def init(hosts, topic):
    global classifier
    if classifier is None:
        classifier = _initialize_classifier(hosts, topic)

def _initialize_classifier(hosts, topic):
    classified_wines = load_classified_wines(hosts, topic)
    training_set, training_set_classes = _prepare_training_set(classified_wines)
    classifier = _create_classifier()
    classifier.fit(training_set, training_set_classes)
    return classifier

def _prepare_training_set(classified_wines):
    training_set = []
    training_set_classes = []
    for classified_wine in classified_wines:
        training_set.append(_convert_to_list(classified_wine['wine']))
        training_set_classes.append(classified_wine['wine_class'])
    return array(training_set), array(training_set_classes)

def _create_classifier():
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

def predict_class(wine):
    wine_list = array(_convert_to_list(wine)).reshape(1, -1)
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
