from app.endpoints.restplus import flask_app, api
from app.api.wines_endpoint import wines_ns
from app.api.specification_endpoint import specification_ns
import app.wine_domain.model as domain_model
from app.wine_domain.distributed_log import DistributedLogContext

if __name__ == '__main__':
    try:
        domain_model.initialize()
        api.add_namespace(wines_ns)
        api.add_namespace(specification_ns)
        flask_app.run(host='0.0.0.0', port=80)
    finally:
        DistributedLogContext.free_log()
