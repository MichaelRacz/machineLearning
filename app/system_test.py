from features.steps.classification_steps import _split_wine_data, _convert_record, _extract_wine
import requests

datastore_url = 'http://datastore/v1/wines'
svc_url = 'http://datastore/v1/wines/classification/svc'

training_set, test_set = _split_wine_data()

# headers={'content-type':'application/json'

def fill_datastore():
    for record in training_set:
        classified_wine = _convert_record(record)
        request = requests.post(datastore_url, data=classified_wine)
        print('Posted classified_wine, status_code: {}'.format(request.status_code))

def classify_svc():
    for record in test_set:
        wine = _extract_wine(record)
        request = requests.post(svc_url, data=wine)
        print('Expecting class {}, response: {}'.format(wine[0], request.text))

if __name__ == '__main__':
    fill_datastore()
