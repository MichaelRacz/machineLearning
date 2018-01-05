# machineLearning
Some machine learning related micro services. The services are implemented in Python3 and feature functional style.
- wines service: Datastore for wine records that are used for initializing classification service
- svc service: Wine classification service based on the _SVC_ algorithm
- nearest neighbor service: Wine classification service based on _Nearest Neighbor_ algorithm
## Some used technologies:
- Flask
- Flask-Restplus
- SQLAlchemy
- NumPy, SciPy, scikit-learn
- Kafka
- Behave
- Nosetests
## Structure
- classification_contract: Consumer driven contract defining the interaction between the datastore and the classification services
- common: Some service independent utilities
- nearest_neighbor: _Nearest Neighbor_ classification service
- svc: _SVC_ classification service
- test: test infrastructure
- wines: Wines datastore service
## Notes
Due to major refactorings, _Docker_ and _Docker Compose_ files are currently broken.
