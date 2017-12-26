from wines.app.database import engine
import json

def clear_database():
    engine.execute('DELETE FROM Wines')

def post_wine_record(context, classified_wine):
    return context.client.post(context.wines_ns,
        data=json.dumps(classified_wine),
        headers={'content-type':'application/json'})

def create_wine(alcohol = 0.0,
    malic_acid = 1.1,
    ash = 2.2,
    alcalinity_of_ash = 3.3,
    magnesium =  5,
    total_phenols = 6.6,
    flavanoids = 7.7,
    nonflavanoid_phenols = 8.8,
    proanthocyanins = 9.9,
    color_intensity = 10.1,
    hue = 11.1,
    odxxx_of_diluted_wines = 12.1,
    proline = 13):
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

def create_classified_wine(wine, wine_class):
    return {
        'wine': wine,
        'wine_class': wine_class}
