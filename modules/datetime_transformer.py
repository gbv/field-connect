import re
from qgis.PyQt.QtCore import QDateTime


class DateTimeTransformer:
    FORMAT = "dd.MM.yyyy HH:mm"

    _re = re.compile(r"^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}$")

    def __init__(self, source_tz, target_tz):
        self.source_tz = source_tz
        self.target_tz = target_tz

    def can_transform(self, value: str) -> bool:
        return bool(self._re.match(value))

    def transform(self, value: str) -> str:
        dt = QDateTime.fromString(value, self.FORMAT)
        if not dt.isValid():
            return value  # fail safe

        dt.setTimeZone(self.source_tz)
        dt = dt.toTimeZone(self.target_tz)

        return dt.toString(self.FORMAT)
