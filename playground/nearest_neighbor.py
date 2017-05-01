from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing
from load_wine import load_wine
import classification

# TODO: move to constants
n_jobs = 4
pre_dispatch = '10000*n_jobs'

def create_k_nearest_neighbor_classifier(training_set, training_set_classes, score):
    common_parameters = {
        'n_neighbors': range(2, 30),
        'weights': ['uniform', 'distance'], #+ [lambda distances: get_weights(distances, weights) for weights in cartesian(len(training_set))],
        'algorithm': ['ball_tree', 'kd_tree', 'brute']}

    hyper_parameter_grid = [
        {**common_parameters, **{'metric': ['manhattan', 'euclidean', 'chebyshev']}},
        {**common_parameters, **{'metric': ['minkowski'], 'p': [3, 4]}}]

    #TODO: Score and remaining metrics

    classifier = GridSearchCV(neighbors.KNeighborsClassifier(), hyper_parameter_grid, scoring=score,
        n_jobs=n_jobs, pre_dispatch=pre_dispatch, cv=5)

    classification.fit_classifier(classifier, training_set, training_set_classes)
    return classifier

weight_values = [0.0, 1.0]

def cartesian(n):
    if n == 1:
        return [[weight] for weight in weight_values]
    else:
        return [[weight] + product for weight in weight_values for product in cartesian(n-1)]

def get_weights(distances, weights):
    return weights

scores = [
    'accuracy',
    'f1_micro', 'f1_macro', 'f1_weighted',
    'neg_log_loss',
    'precision_micro', 'precision_macro', 'precision_weighted',
    'recall_micro', 'recall_macro', 'recall_weighted']
    # 'f1', 'average_precision', 'recall_samples', 'recall', 'f1_samples',
    # 'roc_auc', 'precision', 'precision_samples'

# scores = ['accuracy', 'recall_macro', 'precision_micro', 'recall_micro', 'precision_weighted']
scores = ['accuracy']
#scores = []

if __name__ == '__main__':
    statistics = {}
    for score in scores:
        print('\n\nSCORE: {}\n\n'.format(score))
        success_rates = []
        for i in range(0,5):
            try:
                training_set, training_set_classes, test_set, test_set_classes = load_wine()
                scaler = preprocessing.StandardScaler().fit(training_set)
                #scaler = preprocessing.Normalizer().fit(training_set)
                training_set = scaler.transform(training_set)
                classifier = create_k_nearest_neighbor_classifier(training_set, training_set_classes, score)
                test_set = scaler.transform(test_set)
                success_rates.append(classification.classify(classifier, test_set, test_set_classes))
            except:
                success_rates.append('X')
        statistics[score] = success_rates
    print('\n\nSTATISTICS:\n\n')
    for key, value in statistics.items():
        print('{}: {}'.format(key, value))

# TODO: Scaler, Normalizer in anderen algorithmen
