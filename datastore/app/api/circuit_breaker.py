from threading import Lock

class CircuitBreaker:
    def __init__(self, max_requests):
        self.max_requests = max_requests
        self.open_requests = 0
        self.lock = Lock()
        self.close('Service not initialized.', 503)

    def open(self):
        self.lock.acquire()
        try:
            self.is_open = True
            self.reason = None
            self.status_code = None
        finally:
            self.lock.release()

    def close(self, reason, status_code):
        self.lock.acquire()
        try:
            self.is_open = False
            self.reason = reason
            self.status_code = status_code
        finally:
            self.lock.release()

    def decorate(self, f):
        def decorated_circuit_breaker_f(*args, **kwargs):
            can_execute = False
            self.lock.acquire()
            try:
                can_execute = self.is_open and self.open_requests < self.max_requests
                if can_execute:
                    self.open_requests += 1
            finally:
                self.lock.release()
            if can_execute:
                try:
                    return f(*args, **kwargs)
                finally:
                    self.lock.acquire()
                    try:
                        self.open_requests -= 1
                    finally:
                        self.lock.release()
            else:
                if self.is_open is False :
                    return {'error_message': self.reason}, self.status_code
                else:
                    return {'error_message': 'Too many requests.'}, 429
        decorated_circuit_breaker_f.__wrapped__ = f
        return decorated_circuit_breaker_f

# TODO make configurable
wines_circuit_breaker = CircuitBreaker(20)
