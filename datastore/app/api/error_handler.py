from app.wine_domain.database import UnknownRecordError
from app.api.logger import logger
import uuid
from datetime import datetime
from werkzeug.exceptions import HTTPException
import traceback

def handle_errors(function_name):
    def _handle_errors_decorator(f):
        def error_handling_f(*args, **kwargs):
            request_id = uuid.uuid4().hex
            try:
                logger.info("{} begin call '{}', request id: {}".format(str(datetime.now()), function_name, request_id))
                result = f(*args, **kwargs)
                logger.info("{} end call '{}', request id: {}".format(str(datetime.now()), function_name, request_id))
                return result
            except HTTPException as error:
                logger.error("{} failed call '{}' (framework validation), request id: {}, error message: {}"
                    .format(str(datetime.now()), function_name, request_id, repr(error)))
                raise
            except Exception as error:
                detailed_message = '{}: {}'.format(repr(error), traceback.format_tb(error.__traceback__))
                logger.error("{} failed call '{}', request id: {}, error message: {}"
                    .format(str(datetime.now()), function_name, request_id, detailed_message))
                status_code = 404 if type(error) is UnknownRecordError else 500
                return {'error_message': str(error)}, status_code
        error_handling_f.__wrapped__ = f
        return error_handling_f
    return _handle_errors_decorator
