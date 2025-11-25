from qgis.core import Qgis
from requests import Session, exceptions
from requests.models import Response
from urllib.parse import urlparse, urlunparse
from ..utils.helpers import safe_get
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..field_connect_dockwidget import FieldConnectDockWidget

class ApiClient:
    def __init__(self, password, plugin: "FieldConnectDockWidget", baseUrl='http://localhost:3000'):
        self.plugin = plugin
        self.session = Session()
        self.session.auth = ('', password)
        self.baseUrl = baseUrl.rstrip('/')
        self.connected = False

    def buildUrl(self, path, port):
        parsed = urlparse(f'{self.baseUrl}{path}')
        netloc = f'{parsed.hostname}:{port}'
        # append port to hostname since _replace doesnt support port replacement
        newParsed = parsed._replace(netloc=netloc)
        return urlunparse(newParsed)

    def get(self, path='', params={}, port=3000):
        try:
            url = self.buildUrl(path, port)
            resp: Response = self.session.get(url, params=params)
            return self._handle_response(resp)
        except exceptions.RequestException as e:
            self.plugin.mB.pushCritical(self.plugin.plugin_name, str(e))
            return None

    def post(self, path='', params={}, port=3000, headers={}, data={}):
        try:
            url = self.buildUrl(path, port)
            resp: Response = self.session.post(url, params=params, headers=headers, data=data)
            return self._handle_response(resp)
        except exceptions.RequestException as e:
            self.plugin.mB.pushCritical(self.plugin.plugin_name, str(e))
            return None

    def setConnected(self, connected: bool):
        self.connected = connected

    def disconnect(self):
        self.session = Session()
        self.setConnected(False)

    def isConnectionActive(self):
        """
        Check if connection is still active and disconnect if not
        """
        r = self.get('/info')
        if not r:
            self.plugin.setConnectionEnabled(False)
            self.plugin.fieldDisconnect()
            self.plugin.mB.pushWarning(self.plugin.plugin_name, self.plugin.labels['CONNECTION_LOST'])
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
            importErrors = safe_get(r, 'importErrors')
            self.plugin.mB.pushWarning(self.plugin.plugin_name, error + (': ' + '; '.join(str(e) for e in importErrors) if importErrors else ""))
            return None
        elif r.status_code == 401:
            self.plugin.setConnectionEnabled(False)
            self.plugin.fieldDisconnect()
            self.plugin.mB.pushWarning(self.plugin.plugin_name, self.plugin.labels['CONNECTION_UNAUTHORIZED'] + f': {r.reason}')
            return None
        else:
            self.plugin.setConnectionEnabled(False)
            self.plugin.fieldDisconnect()
            self.plugin.mB.pushMessage(': '.join([self.plugin.plugin_name, self.plugin.labels['REQUEST_FAILED'], r.reason]), Qgis.Warning, 5)
            return None
