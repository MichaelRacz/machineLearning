from app.api.restplus import flask_app, api
from app.api.wines_endpoint import wines_ns
from app.api.specification_endpoint import specification_ns
import app.wine_domain.model as domain_model
from app.wine_domain.distributed_log import DistributedLogContext
from app.api.circuit_breaker import wines_circuit_breaker
from app.wine_domain.synchronization import synchronize_datastore

def _initialize():
    domain_model.initialize()
    synchronize_datastore()
    wines_circuit_breaker.open()
    api.add_namespace(wines_ns)
    api.add_namespace(specification_ns)

def _tear_down():
    DistributedLogContext.free_log()

if __name__ == '__main__':
    try:
        _initialize()
        flask_app.run(host='0.0.0.0', port=80)
    finally:
        _tear_down()
