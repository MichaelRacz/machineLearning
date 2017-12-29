from classification_contract.wine_test_data.wine_data import wine_data
from classification_contract.assertions import assert_classified_wine_structure

def get_classified_wine():
    classified_wine = _extract_classified_wine(wine_data[-1])
    assert_classified_wine_structure(classified_wine)
    return classified_wine

def split_wine_data():
    training_set = []
    test_set = []
    for record in wine_data:
        classified_wine = _extract_classified_wine(record)
        if random() < 0.7:
            training_set.append(classified_wine)
        else:
            test_set.append(classified_wine)
    return training_set, test_set

def _extract_classified_wine(record):
    wine = _extract_wine(record)
    wine_class = str(record[0])
    return {
        'wine': wine,
        'wine_class': wine_class}

def _extract_wine(record):
    record_without_class = record[1:]
    return _create_wine(*record_without_class)

def _create_wine(alcohol,
    malic_acid,
    ash,
    alcalinity_of_ash,
    magnesium,
    total_phenols,
    flavanoids,
    nonflavanoid_phenols,
    proanthocyanins,
    color_intensity,
    hue,
    odxxx_of_diluted_wines,
    proline):
    return {
        'alcohol': alcohol,
        'malic_acid': malic_acid,
        'ash': ash,
        'alcalinity_of_ash': alcalinity_of_ash,
        'magnesium':  magnesium,
        'total_phenols': total_phenols,
        'flavanoids': flavanoids,
        'nonflavanoid_phenols': nonflavanoid_phenols,
        'proanthocyanins': proanthocyanins,
        'color_intensity': color_intensity,
        'hue': hue,
        'odxxx_of_diluted_wines': odxxx_of_diluted_wines,
        'proline': proline}
