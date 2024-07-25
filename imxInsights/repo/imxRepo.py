import tempfile
import uuid
import zipfile
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from imxInsights.domain.imxObject import ImxObject
from imxInsights.exceptions import ImxException
from imxInsights.repo.tree.imxObjectTree import ObjectTree


class ImxRepo:
    """
    Represents an IMX container.

    Args:
        imx_file_path: The path to the IMX container or IMX File.

    Attributes:
        container_id: UUID4 of the container
        path: Path of the IMX container or IMX File.
    """

    # todo: maybe we should inheritance from the tree so we dont need to duplicated the methods

    def __init__(self, imx_file_path: Path | str):
        # todo: imx_file_path should be only Path
        self.container_id: str = str(uuid.uuid4())
        self._tree: ObjectTree = ObjectTree()

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

    def get_all(self) -> Iterable[ImxObject]:
        """
        Retrieves all objects in the tree.

        Returns:
            Iterable[ImxObject]: An iterable of all ImxObjects.

        """

        return self._tree.get_all()

    def find(self, key: str | ImxObject) -> ImxObject | None:
        """
        Finds an object in the tree by its key or ImxObject.

        Args:
            key (str | ImxObject): The key or ImxObject to find.

        Returns:
            ImxObject | None: The found ImxObject, or None if not found.
        """
        return self._tree.find(key)

    def get_types(self) -> list[str]:
        """
        Retrieves all unique object types in the tree.

        Returns:
            list[str]: A list of all unique object types.
        """
        return self._tree.get_all_types()

    def get_by_types(self, object_types: list[str]) -> list[ImxObject]:
        """
        Retrieves objects of specified types from the tree.

        Args:
            object_types (list[str]): The list of object types to retrieve.

        Returns:
            list[ImxObject]: The list of matching ImxObjects.
        """
        return self._tree.get_by_types(object_types)

    def get_all_paths(self) -> list[str]:
        """
        Retrieves all unique object paths in the tree.

        Returns:
            list[str]: A list of all unique object paths.
        """
        return self._tree.get_all_paths()

    def get_by_paths(self, object_paths: list[str]) -> list[ImxObject]:
        """
        Retrieves objects of specified paths from the tree.

        Args:
            object_paths (list[str]): The list of object paths to retrieve.

        Returns:
            list[ImxObject]: The list of matching ImxObjects.
        """
        return self._tree.get_by_path(object_paths)

    def get_keys(self) -> list[str]:
        """
        Returns the set of keys currently in the tree dictionary.

        Returns:
            frozenset[str]: The set of keys in the tree dictionary.
        """
        return list(self._tree.keys)

    def get_build_exceptions(self) -> defaultdict[str, list[ImxException]]:
        """
        todo: make docs
        """
        return self._tree.build_extensions.exceptions
