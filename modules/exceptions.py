class ApiError(Exception):
    """Base class for all API errors."""

    pass


class ApiConnectionError(ApiError):
    pass


class ApiTimeoutError(ApiError):
    pass


class ApiUnauthorizedError(ApiError):
    pass


class ApiBadRequestError(ApiError):
    def __init__(self, message: str, import_errors=None):
        super().__init__(message)
        self.import_errors = import_errors or []


class ApiRequestFailedError(ApiError):
    def __init__(self, status_code: int, reason: str):
        super().__init__(f"{status_code}: {reason}")
        self.status_code = status_code
        self.reason = reason
