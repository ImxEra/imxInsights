import uuid
from pathlib import Path
from lxml import etree as ET

from imxInsights.utils.xmlFile import XmlFile


class ImxFile:
    """
    Represents an IMX file.

    Attributes:
        container_id (str | None): The ID of the container.
        _xml_file (XmlFile): The XML file.
        imx_version (str): The IMX version.
    """

    def __init__(self, imx_file_path: Path, container_id: str = str(uuid.uuid4())):
        """
        Initializes an ImxFile object.

        Args:
            imx_file_path (Path): The path to the IMX file.
        """
        self._xml_file = XmlFile(imx_file_path)
        self.container_id = container_id
        self.imx_version: str = self._xml_file.root.find("[@imxVersion]").attrib[
            "imxVersion"
        ]

    @property
    def file_hash(self) -> str:
        """
        Gets the hash of the file.

        Returns:
            str: The file hash.
        """
        return self._xml_file.file_hash

    @property
    def path(self) -> Path:
        return self._xml_file.path

    @property
    def path_str(self) -> str:
        """
        Gets the absolute path of the file.

        Returns:
            str: The file path.
        """
        return str(self._xml_file.path.absolute())

    @property
    def tag(self) -> str:
        """
        Gets the tag of the XML root element.

        Returns:
            str: The tag name.
        """
        return self._xml_file.tag

    @property
    def root(self) -> ET.ElementTree:
        """
        Gets the root element of the XML file.

        Returns:
            ET.ElementTree: The root element.
        """
        return self._xml_file.root
