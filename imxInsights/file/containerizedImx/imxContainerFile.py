import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import dateparser

from imxInsights.file.containerizedImx.imxContainerFileReference import (
    ImxContainerFileReference,
)
from imxInsights.file.imxFile import ImxFile


class ImxContainerFile(ImxFile):
    """
    Represents a base class for IMX container files.

    Args:
        imx_file_path: The path to the IMX file.
        file_id: Optional file ID.

    Attributes:
        previous_version: Gets the previous version file reference, if available.

    """

    def __init__(self, imx_file_path: Path, file_id: str | None = None):
        super().__init__(imx_file_path, file_id or "")

    @property
    def previous_version(self) -> list[ImxContainerFileReference]:
        if self.root is None:
            return []

        prev_version_node = self.root.find(
            ".//{http://www.prorail.nl/IMSpoor}PreviousVersion"
        )
        return (
            [ImxContainerFileReference.from_element(prev_version_node)]
            if prev_version_node is not None
            else []
        )


class ImxDesignCoreFile(ImxContainerFile):
    """
    Represents an IMX design core file, extending ImxContainerFile.

    Args:
        imx_file_path: The path to the IMX file.
        file_id: Optional file ID.

    Attributes:
        reference_date:  Gets the reference date attribute from the XML root element.
        perspective_date: Gets the perspective date attribute from the XML root element.

    """

    def __init__(self, imx_file_path: Path, file_id: str | None):
        super().__init__(imx_file_path, file_id)

    def _parse_dates(self):
        pass

    @property
    def reference_date(self) -> datetime.datetime | None:
        if self.root is None:
            return None

        element = self.root.find("[@referenceDate]")

        return (
            dateparser.parse(element.attrib["referenceDate"])
            if element is not None
            else None
        )

    @property
    def perspective_date(self) -> datetime.datetime | None:
        if self.root is None:
            return None

        element = self.root.find("[@perspectiveDate]")
        return (
            dateparser.parse(element.attrib["perspectiveDate"])
            if element is not None
            else None
        )


class ImxDesignPetalFile(ImxContainerFile):
    """
    Represents an IMX design petal file, extending ImxContainerFile.

    Args:
        imx_file_path: The path to the IMX file.
        file_id: Optional file ID.

    Attributes:
        base_reference: Gets the base reference file reference, if available.

    """

    def __init__(self, imx_file_path: Path, file_id: str | None):
        super().__init__(imx_file_path, file_id)

    @property
    def base_reference(self) -> ImxContainerFileReference | None:
        if self.root is None:
            return None

        base_ref_node = self.root.find(
            ".//{http://www.prorail.nl/IMSpoor}BaseReference"
        )
        if base_ref_node is not None:
            return ImxContainerFileReference.from_element(base_ref_node)
        return None


@dataclass
class ImxContainerFiles:
    """
    A data class representing a collection of IMX container files.

    ??? info
        This class holds references to various IMX design files and additional files
        that might be included in an IMX container.

    Attributes:
        manifest : The manifest file.
        signaling_design: The signaling design file.
        furniture: The furniture file.
        train_control: The train control file.
        management_areas: The management areas file.
        installation_design: The installation design file.
        network_configuration: The network configuration file.
        schema_layout: The schema layout file.
        railway_electrification: The railway electrification file.
        bgt: The BGT file.
        observations: The observations file.
        additional_files: A list of additional files.
    """

    manifest: ImxFile | None = None
    signaling_design: ImxDesignCoreFile | None = None
    furniture: ImxDesignPetalFile | None = None
    train_control: ImxDesignPetalFile | None = None
    management_areas: ImxDesignPetalFile | None = None
    installation_design: ImxDesignPetalFile | None = None
    network_configuration: ImxDesignPetalFile | None = None
    schema_layout: ImxDesignPetalFile | None = None
    railway_electrification: ImxDesignPetalFile | None = None
    bgt: ImxDesignPetalFile | None = None
    observations: ImxDesignPetalFile | None = None
    additional_files: list[Any] = field(default_factory=list)

    @classmethod
    def from_container(
        cls, container_path: Path, container_id: str
    ) -> "ImxContainerFiles":
        """
        Creates an ImxContainerFiles instance from a container zip.

        ??? info
            This method extracts relevant IMX files from a given container directory,
            categorizes them based on their tags, and assigns them to the appropriate
            attributes of an ImxContainerFiles instance.

        Args:
            container_path (Path): The path to the container zip.
            container_id (str): The container UUID4.

        Returns:
            ImxContainerFiles: An instance populated with files found in the container directory.

        Raises:
            ValueError: If an unsupported Imx version is encountered or if multiple XML files of the same type are found.
        """
        self = cls()

        tag_to_attr = {
            "{http://www.prorail.nl/IMSpoor}SignalingDesign": "signaling_design",
            "{http://www.prorail.nl/IMSpoor}Manifest": "manifest",
            "{http://www.prorail.nl/IMSpoor}Furniture": "furniture",
            "{http://www.prorail.nl/IMSpoor}TrainControl": "train_control",
            "{http://www.prorail.nl/IMSpoor}ManagementAreas": "management_areas",
            "{http://www.prorail.nl/IMSpoor}InstallationDesign": "installation_design",
            "{http://www.prorail.nl/IMSpoor}NetworkConfiguration": "network_configuration",
            "{http://www.prorail.nl/IMSpoor}SchemaLayout": "schema_layout",
            "{http://www.prorail.nl/IMSpoor}RailwayElectrification": "railway_electrification",
            "{http://www.prorail.nl/IMSpoor}Bgt": "bgt",
            "{http://www.prorail.nl/IMSpoor}Observations": "observations",
        }

        for file_path in container_path.glob("*"):
            if file_path.is_file() and file_path.suffix == ".xml":
                imx_file = ImxFile(file_path, container_id)
                if imx_file.imx_version != "12.0.0":
                    raise ValueError(  # noqa: TRY003
                        f"Imx version {imx_file.imx_version} not supported"
                    )

                attr_name = tag_to_attr.get(imx_file.tag)
                if attr_name == "signaling_design":
                    imx_file = ImxDesignCoreFile(file_path, container_id)
                elif attr_name and attr_name != "manifest":
                    imx_file = ImxDesignPetalFile(file_path, container_id)

                if attr_name:
                    if getattr(self, attr_name) is not None:
                        raise ValueError(f"Multiple {attr_name} xml files")  # noqa: TRY003
                    setattr(self, attr_name, imx_file)
            else:
                self.additional_files.append(file_path)

        return self
