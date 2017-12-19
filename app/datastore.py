from app.api.restplus import flask_app, api
from app.api.wines_endpoint import wines_ns
from app.api.specification_endpoint import specification_ns
import common.app.wine_db as database
from app.wine_domain.distributed_log import DistributedLogContext
from app.api.circuit_breaker import wines_circuit_breaker

if __name__ == '__main__':
    try:
        database.initialize()
        wines_circuit_breaker.open()
        api.add_namespace(wines_ns)
        api.add_namespace(specification_ns)
        flask_app.run(host='0.0.0.0', port=80)
    finally:
        DistributedLogContext.free_log()
