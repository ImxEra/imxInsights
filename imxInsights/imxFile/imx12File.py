from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from imxInsights.imxFile.imxFile import ImxFile
from imxInsights.imxFile.imx12FileReference import Imx12FileReference


class Imx12File(ImxFile):
    def __init__(self, imx_file_path: Path, container_id: str | None):
        super().__init__(imx_file_path, container_id)

    @property
    def previous_version(self) -> list[Imx12FileReference]:
        """
        Gets the previous version file reference, if available.

        Returns:
            Optional[FileReference]: The previous version file reference or None if not available.
        """
        prev_version_node = self.root.find(
            ".//{http://www.prorail.nl/IMSpoor}PreviousVersion"
        )
        return (
            Imx12FileReference.from_element(prev_version_node)
            if prev_version_node
            else []
        )


class ImxDesignCoreFile(Imx12File):
    def __init__(self, imx_file_path: Path, container_id: str | None):
        super().__init__(imx_file_path, container_id)

    @property
    def reference_date(self) -> str | None:
        element = self.root.find("[@referenceDate]")
        return element.attrib["referenceDate"] if element is not None else None

    @property
    def perspective_date(self) -> str | None:
        element = self.root.find("[@perspectiveDate]")
        return element.attrib["perspectiveDate"] if element is not None else None


class ImxDesignPetalFile(Imx12File):
    def __init__(self, imx_file_path: Path, container_id: str | None):
        super().__init__(imx_file_path, container_id)

    @property
    def base_reference(self) -> Imx12FileReference | None:
        """
        Gets the base reference file reference, if available.

        Returns:
            Optional[FileReference]: The base reference file reference or None if not available.
        """
        base_ref_node = self.root.find(
            ".//{http://www.prorail.nl/IMSpoor}BaseReference"
        )
        if base_ref_node is not None:
            return Imx12FileReference.from_element(base_ref_node)
        return None


@dataclass
class Imx12Files:
    manifest: ImxFile = field(default=None)
    signaling_design: ImxDesignCoreFile = field(default=None)
    furniture: ImxDesignPetalFile | None = field(default=None)
    train_control: ImxDesignPetalFile | None = field(default=None)
    management_areas: ImxDesignPetalFile | None = field(default=None)
    installation_design: ImxDesignPetalFile | None = field(default=None)
    network_configuration: ImxDesignPetalFile | None = field(default=None)
    schema_layout: ImxDesignPetalFile | None = field(default=None)
    railway_electrification: ImxDesignPetalFile | None = field(default=None)
    bgt: ImxDesignPetalFile | None = field(default=None)
    observations: ImxDesignPetalFile | None = field(default=None)
    additional_files: list[any] = field(default_factory=list)

    @classmethod
    def from_container(cls, container_path: Path, container_id: str):
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
                    raise ValueError(
                        f"Imx version {imx_file.imx_version} not supported"
                    )

                attr_name = tag_to_attr.get(imx_file.tag)
                if attr_name == "signaling_design":
                    imx_file = ImxDesignCoreFile(file_path, container_id)
                elif attr_name and attr_name != "manifest":
                    imx_file = ImxDesignPetalFile(file_path, container_id)

                if attr_name:
                    if getattr(self, attr_name) is not None:
                        raise ValueError(f"Multiple {attr_name} xml files")
                    setattr(self, attr_name, imx_file)
            else:
                self.additional_files.append(file_path)

        return self
