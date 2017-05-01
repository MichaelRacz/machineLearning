def fit_classifier(classifier, training_set, training_set_classes):
    classifier.fit(training_set, training_set_classes)
    print('best params: {}'.format(classifier.best_params_))

def classify(classifier, test_set, test_set_classes):
    correct_predictions = 0;
    for i in range(0, len(test_set)):
        predicted_class = classifier.predict([test_set[i]])[0]
        if (predicted_class == test_set_classes[i]):
            correct_predictions += 1
    success_rate = correct_predictions / len(test_set)
    print('success rate: {}'.format(success_rate))
    return success_rate
