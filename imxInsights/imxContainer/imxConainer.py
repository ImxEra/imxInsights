import tempfile
import uuid
import zipfile
from pathlib import Path

from imxInsights.imxContainer.tree.imxObjectTree import ObjectTree


class ImxContainer:
    """Represents an IMX container."""

    def __init__(self, imx_container: Path | str):
        """
        Initializes the ImxContainer.

        Args:
            imx_container (Union[Path, str]): The path to the IMX container.
        """
        self.container_id: str = str(uuid.uuid4())
        self.tree: ObjectTree = ObjectTree()

        if zipfile.is_zipfile(imx_container):
            imx_container = self._parse_zip_container(imx_container)
        elif isinstance(imx_container, str):
            imx_container = Path(imx_container)
        self.path: Path = imx_container

        self.rail_connections: list = []
        self.track_assets: list = []

    @staticmethod
    def _parse_zip_container(imx_container_as_zip: str | Path):
        """
        Parse the IMX container if it's a zip file.

        Args:
            imx_container_as_zip (Union[str, Path]): The path to the IMX container as a zip file.

        Returns:
            Path: The extracted directory path of the zip container.
        """
        with tempfile.TemporaryDirectory(delete=False) as temp_dir:
            temp_path = Path(temp_dir)
            with zipfile.ZipFile(imx_container_as_zip, "r") as zip_ref:
                zip_ref.extractall(temp_path)
            return temp_path
