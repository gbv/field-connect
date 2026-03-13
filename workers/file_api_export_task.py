from pathlib import Path
from qgis.core import QgsTask
from PyQt5.QtCore import pyqtSignal


class FileApiExportTask(QgsTask):
    progress_text = pyqtSignal(str)
    export_finished = pyqtSignal(object)

    def __init__(
        self,
        description,
        file_api,
        file_export_paths,
        category,
        read_creators_from_metadata,
        raster_count,
        worldfile_count,
    ):
        super().__init__(description, QgsTask.CanCancel)

        self.file_api = file_api
        self.file_export_paths = file_export_paths
        self.category = category
        self.read_creators_from_metadata = read_creators_from_metadata
        self.raster_count = raster_count
        self.worldfile_count = worldfile_count

        self.result = None
        self.messages = None

    def run(self):
        total = len(self.file_export_paths)

        for i, path in enumerate(self.file_export_paths):

            if self.isCanceled():
                return False

            self.progress_text.emit(Path(path).name)

            progress = int((i + 1) / total * 100)
            self.setProgress(progress)

        resp = self.file_api.post_images(
            self.file_export_paths,
            self.category,
            self.read_creators_from_metadata,
        )

        result = resp.json()
        self.result = result

        return True

    def finished(self, result):
        if result:
            self.export_finished.emit(self.result)
        else:
            self.export_finished.emit(None)
