from app.api.restplus import flask_app, api
from app.api.wines_endpoint import wines_ns
from app.api.specification_endpoint import specification_ns
import common.app.wine_db as database
from app.api.circuit_breaker import wines_circuit_breaker
import app.wine_domain.wines as wines

if __name__ == '__main__':
    try:
        database.initialize()
        wines_circuit_breaker.open()
        api.add_namespace(wines_ns)
        api.add_namespace(specification_ns)
        wines.init()
        flask_app.run(host='0.0.0.0', port=80)
    finally:
        wines.exit()
