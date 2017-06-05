from app.endpoints.api import flask_app, api
from app.endpoints.wines import wines_ns
from app.endpoints.specification import specification_ns
import app.wine_domain.model as domain_model

if __name__ == '__main__':
    domain_model.initialize()
    api.add_namespace(wines_ns)
    api.add_namespace(specification_ns)
    flask_app.run(host='0.0.0.0', port=80)
