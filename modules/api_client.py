from qgis.core import Qgis
from requests import Session, exceptions
from requests.models import Response
from urllib.parse import urlparse, urlunparse
from ..utils.helpers import safe_get
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..field_connect_dockwidget import FieldConnectDockWidget


class ApiClient:
    def __init__(self, password, plugin: "FieldConnectDockWidget", base_url='http://localhost:3000'):
        self.plugin = plugin
        self.session = Session()
        self.session.auth = ('', password)
        self.baseUrl = base_url.rstrip('/')
        self.connected = False

    def build_url(self, path, port):
        parsed = urlparse(f'{self.baseUrl}{path}')
        netloc = f'{parsed.hostname}:{port}'
        # append port to hostname since _replace doesnt support port replacement
        new_parsed = parsed._replace(netloc=netloc)
        return urlunparse(new_parsed)

    def get(self, path='', params={}, port=3000):
        try:
            url = self.build_url(path, port)
            resp: Response = self.session.get(url, params=params)
            return self._handle_response(resp)
        except exceptions.ConnectionError:
            self.plugin.mB.pushCritical(self.plugin.plugin_name, self.plugin.labels['CONNECTION_REFUSED'])
            return None
        except exceptions.Timeout:
            self.plugin.mB.pushCritical(self.plugin.plugin_name, self.plugin.labels['CONNECTION_REFUSED'])
            return None
        except exceptions.RequestException as e:
            self.plugin.mB.pushCritical(self.plugin.plugin_name, str(e))
            return None

    def post(self, path='', params={}, port=3000, headers={}, data={}):
        try:
            url = self.build_url(path, port)
            resp: Response = self.session.post(url, params=params, headers=headers, data=data)
            return self._handle_response(resp)
        except exceptions.RequestException as e:
            self.plugin.mB.pushCritical(self.plugin.plugin_name, str(e))
            return None

    def set_connected(self, connected: bool):
        self.connected = connected

    def disconnect(self):
        self.session = Session()
        self.set_connected(False)

    def is_connection_active_and_valid(self, active_project):
        """
        Check if connection is still active and the project has not changed
        """
        r = self.get('/info')
        if not r:
            self.plugin.set_connection_enabled(False)
            self.plugin.field_disconnect()
            self.plugin.mB.pushWarning(self.plugin.plugin_name, self.plugin.labels['CONNECTION_LOST'])
            return False
        if active_project != safe_get(r.json(), 'activeProject', default=False):
            self.plugin.set_connection_enabled(False)
            self.plugin.field_disconnect()
            self.plugin.mB.pushCritical(self.plugin.plugin_name, self.plugin.labels['ACTIVE_PROJECT_CHANGED'])
            return False
        return True

    def _handle_response(self, r: Response):
        # print(r.url)
        # print(r.reason)
        # python 3.10+
        # match r.status_code:
        #     case 200:
        #         return r
        #     case 400:
        #         # print(r.text)
        #         self.plugin.mB.pushWarning(self.plugin.plugin_name, self.plugin.labels['BAD_REQUEST'] + f': {r.text}')
        #         return None
        #     case 401:
        #         self.plugin.setConnectionEnabled(False)
        #         self.plugin.fieldDisconnect()
        #         self.plugin.mB.pushWarning(self.plugin.plugin_name, self.plugin.labels['CONNECTION_UNAUTHORIZED'] + f': {r.reason}')
        #         return None
        #     case _:
        #         self.plugin.setConnectionEnabled(False)
        #         self.plugin.fieldDisconnect()
        #         self.plugin.mB.pushMessage(': '.join([self.plugin.plugin_name, self.plugin.labels['REQUEST_FAILED'], r.reason]), Qgis.Warning, 5)
        #         return None
        if r.status_code == 200:
            return r
        elif r.status_code == 400:
            r = r.json()
            error = safe_get(r, 'error')
            import_errors = safe_get(r, 'importErrors')
            self.plugin.mB.pushWarning(self.plugin.plugin_name, error + (': ' + '; '.join(str(e) for e in import_errors) if import_errors else ""))
            return None
        elif r.status_code == 401:
            self.plugin.set_connection_enabled(False)
            self.plugin.field_disconnect()
            self.plugin.mB.pushWarning(self.plugin.plugin_name, self.plugin.labels['CONNECTION_UNAUTHORIZED'])
            return None
        else:
            self.plugin.set_connection_enabled(False)
            self.plugin.field_disconnect()
            self.plugin.mB.pushMessage(': '.join([self.plugin.plugin_name, self.plugin.labels['REQUEST_FAILED'], r.reason]), Qgis.Warning, 5)
            return None
