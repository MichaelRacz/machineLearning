from app.api.restplus import flask_app, api
from app.api.nearest_neighbor_classification_endpoint import nearest_neighbor_ns
from app.api.specification_endpoint import specification_ns
import common.app.wine_db as database
from app.api.circuit_breaker import nearest_neighbor_circuit_breaker

if __name__ == '__main__':
    database.initialize()
    nearest_neighbor_circuit_breaker.open()
    api.add_namespace(nearest_neighbor_ns)
    api.add_namespace(specification_ns)
    flask_app.run(host='0.0.0.0', port=80)
