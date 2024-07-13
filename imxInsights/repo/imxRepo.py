import tempfile
import uuid
import zipfile
from pathlib import Path

from imxInsights.repo.tree.imxObjectTree import ObjectTree


class ImxRepo:
    """
    Represents an IMX container.

    Args:
        imx_file_path: The path to the IMX container or IMX File.

    Attributes:
        container_id: UUID4 of the container
        tree: object tree of all objects in  the IMX container or IMX File.
        path: Path of the IMX container or IMX File.
    """

    def __init__(self, imx_file_path: Path | str):
        # todo: imx_file_path should be only Path
        self.container_id: str = str(uuid.uuid4())
        self.tree: ObjectTree = ObjectTree()

        if zipfile.is_zipfile(imx_file_path):
            imx_file_path = self._parse_zip_container(imx_file_path)
        elif isinstance(imx_file_path, str):
            imx_file_path = Path(imx_file_path)
        self.path: Path = (
            imx_file_path if isinstance(imx_file_path, Path) else Path(imx_file_path)
        )

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
