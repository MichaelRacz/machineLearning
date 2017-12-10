from app.api.restplus import flask_app, api
from app.api.nearest_neighbor_classification_endpoint import nearest_neighbor_ns
from app.api.specification_endpoint import specification_ns
import app.wine_domain.database as database
from app.wine_domain.distributed_log import DistributedLogContext
from app.api.circuit_breaker import nearest_neighbor_circuit_breaker
from app.wine_domain.synchronization import synchronize_datastore

if __name__ == '__main__':
    try:
        database.initialize()
        with synchronize_datastore():
            nearest_neighbor_circuit_breaker.open()
            api.add_namespace(nearest_neighbor_ns)
            api.add_namespace(specification_ns)
            flask_app.run(host='0.0.0.0', port=80)
    finally:
        DistributedLogContext.free_log()
