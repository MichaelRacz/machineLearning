from threading import Lock

class CircuitBreaker:
    def __init__(self, max_requests):
        self._max_requests = max_requests
        self._open_requests = 0
        self._lock = Lock()
        self.close('Service not initialized.', 503)

    def open(self):
        self._lock.acquire()
        try:
            self._is_open = True
            self._reason = None
            self._status_code = None
        finally:
            self._lock.release()

    def close(self, reason='Circuit breaker closed.', status_code=500):
        self._lock.acquire()
        try:
            self._is_open = False
            self._reason = reason
            self._status_code = status_code
        finally:
            self._lock.release()

    def decorate(self, f):
        def decorated_circuit_breaker_f(*args, **kwargs):
            can_execute = False
            self._lock.acquire()
            try:
                can_execute = self._is_open and self._open_requests < self._max_requests
                if can_execute:
                    self._open_requests += 1
            finally:
                self._lock.release()
            if can_execute:
                try:
                    return f(*args, **kwargs)
                finally:
                    self._lock.acquire()
                    try:
                        self._open_requests -= 1
                    finally:
                        self._lock.release()
            else:
                if self._is_open is False :
                    return {'error_message': self._reason}, self._status_code
                else:
                    return {'error_message': 'Too many requests.'}, 429
        decorated_circuit_breaker_f.__wrapped__ = f
        return decorated_circuit_breaker_f
