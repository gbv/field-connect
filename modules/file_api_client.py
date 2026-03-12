import json
from .api_client import ApiClient


class FileApiClient:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.worldfile_ext = {
            "jpg": "jgw",
            "tif": "tfw",
            "png": "pgw",
        }

    def get_image_data(self, identifier):
        r = self.api_client.get(f"/fileExport/image/{identifier}")
        content_type, ext = r.headers["Content-Type"].split("/")
        if ext == "jpeg":
            ext = "jpg"
        if ext == "tiff":
            ext = "tif"
        if content_type != "image":
            return None, None
        image = r.content
        return image, ext

    def get_worldfile_data(self, identifier, image_ext=""):
        r = self.api_client.get(f"/fileExport/worldFile/{identifier}")
        worldfile = r.text
        if not worldfile:
            return None, None
        ext = self.worldfile_ext.get(image_ext, "wld")
        return worldfile, ext

    def post_images(
        self, file_paths: list[str] = [""], category="Image", read_creators_from_metadata=False
    ) -> tuple:
        data = {
            "filePaths": file_paths,
            "category": category,
            "readCreatorsFromMetadata": read_creators_from_metadata,
        }

        payload = json.dumps(data)

        r = self.api_client.post(
            "/fileImport", headers={"Content-Type": "application/json"}, data=payload
        )
        return r
