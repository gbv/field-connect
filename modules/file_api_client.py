import json
from pathlib import Path

from .exceptions import ApiBadRequestError, ImageNotFoundError
from .api_client import ApiClient


class FileApiClient:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.supported_image_formats = ["jpg", "tif", "png"]
        # <first letter of extension> + <last letter of extension> + "w"
        self.worldfile_ext = {
            fmt: f"{fmt[0]}{fmt[2]}w" for fmt in self.supported_image_formats if len(fmt) > 2
        }

    def get_image_data(self, identifier):
        try:
            r = self.api_client.get(f"/fileExport/image/{identifier}")
        except ApiBadRequestError as e:
            message = str(e)

            image_not_found_messages = [
                "ENOENT",
                "Could not find image",
                "No original image file found",
            ]
            # continue if image missing or identifier not found
            if any(m in message for m in image_not_found_messages):
                raise ImageNotFoundError(message)

            raise

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

    def worldfile_candidates(self, path: Path):
        """Generate a list of path candidates to look for a worldfile

        Args:
            path (Path): A Path object pointing to an image file

        Returns:
            list: A list of possible worldfile paths to check for
        """
        suffix = path.suffix.lower().lstrip(".")

        candidates = set()

        if suffix in self.supported_image_formats:
            candidates.add(f".{self.worldfile_ext[suffix]}")

        # common alternatives
        candidates.update(
            {
                ".wld",
                f".{suffix}w",  # e.g. .jpgw, .tifw
            }
        )

        return [path.with_suffix(ext) for ext in candidates]
