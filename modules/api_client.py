from requests import Session, exceptions
from requests.models import Response
from urllib.parse import urlparse, urlunparse
from ..utils.helpers import safe_get

from .exceptions import (
    ApiConnectionError,
    ApiTimeoutError,
    ApiUnauthorizedError,
    ApiBadRequestError,
    ApiRequestFailedError,
)


class ApiClient:
    def __init__(self, password: str, base_url: str = "http://localhost:3000"):
        self.session = Session()
        self.session.auth = ("", password)
        self.base_url = base_url.rstrip("/")
        self.connected = False

    def build_url(self, path: str, port: int):
        parsed = urlparse(f"{self.base_url}{path}")
        netloc = f"{parsed.hostname}:{port}"
        new_parsed = parsed._replace(netloc=netloc)
        return urlunparse(new_parsed)

    def get(self, path: str = "", params=None, port: int = 3000):
        params = params or {}
        try:
            url = self.build_url(path, port)
            resp: Response = self.session.get(url, params=params)
            return self._handle_response(resp)

        except exceptions.ConnectionError as e:
            raise ApiConnectionError("Connection refused") from e

        except exceptions.Timeout as e:
            raise ApiTimeoutError("Connection timed out") from e

        except exceptions.RequestException as e:
            raise ApiRequestFailedError(-1, str(e)) from e

    def post(self, path: str = "", params=None, port: int = 3000, headers=None, data=None):
        params = params or {}
        headers = headers or {}
        data = data or {}

        try:
            url = self.build_url(path, port)
            resp: Response = self.session.post(url, params=params, headers=headers, data=data)
            return self._handle_response(resp)

        except exceptions.ConnectionError as e:
            raise ApiConnectionError("Connection refused") from e

        except exceptions.Timeout as e:
            raise ApiTimeoutError("Connection timed out") from e

        except exceptions.RequestException as e:
            raise ApiRequestFailedError(-1, str(e)) from e

    def disconnect(self):
        self.session = Session()
        self.connected = False

    def _handle_response(self, r: Response):

        if r.status_code == 200:
            return r

        elif r.status_code == 400:
            data = r.json()
            error = safe_get(data, "error")
            import_errors = safe_get(data, "importErrors")
            raise ApiBadRequestError(error, import_errors)

        elif r.status_code == 401:
            raise ApiUnauthorizedError("Unauthorized")

        else:
            raise ApiRequestFailedError(r.status_code, r.reason)
