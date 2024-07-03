from dataclasses import dataclass, field
from datetime import datetime

from lxml import etree as ET

from imxInsights.exceptions import exception_handler
from imxInsights.exceptions.imxExceptions import ImxDuplicatedPuicsInContainer
from imxInsights.imxDomain.areas import Areas
from imxInsights.imxDomain.imxEnums import (
    Imx12ProjectDisciplineEnum,
    Imx12DataExchangePhaseEnum,
)


@dataclass
class Imx12ContainerMetadata:
    """
    Represents metadata associated with an IMX12 container.
    """

    external_project_reference: str | None = field(init=False)
    project_name: str | None = field(init=False)
    project_discipline: Imx12ProjectDisciplineEnum | None = field(init=False)
    data_exchange_phase: Imx12DataExchangePhaseEnum | None = field(init=False)
    created_date: datetime | None = field(init=False)
    planned_delivery_date: datetime | None = field(init=False)
    areas: Areas | None = field(init=False)

    @staticmethod
    def from_element(element: ET.Element) -> "Imx12ContainerMetadata":
        """
        Creates an instance of Imx12ContainerMetadata from an XML element.

        Args:
            element (ElementTree.Element): The XML element containing project metadata.

        Returns:
            Imx12ContainerMetadata: An instance of Imx12ContainerMetadata populated with data from the XML element.
        """
        self = Imx12ContainerMetadata()
        project_metadata_element = element.find(
            ".//{http://www.prorail.nl/IMSpoor}ProjectMetadata"
        )
        if project_metadata_element is not None:
            self.external_project_reference = project_metadata_element.get(
                "externalProjectReference", None
            )
            self.project_name = project_metadata_element.get("projectName", None)

            project_discipline = project_metadata_element.get("projectDiscipline", None)
            if project_discipline is not None:
                self.project_discipline = Imx12ProjectDisciplineEnum.from_string(
                    project_discipline
                )

            data_exchange_phase = project_metadata_element.get(
                "dataExchangePhase", None
            )
            if data_exchange_phase is not None:
                self.data_exchange_phase = Imx12DataExchangePhaseEnum.from_string(
                    data_exchange_phase
                )
            self.created_date = project_metadata_element.get("createdDate", None)
            self.planned_delivery_date = project_metadata_element.get(
                "plannedDeliveryDate", None
            )
            return self

        else:
            exception = ImxDuplicatedPuicsInContainer("ProjectMetadata not present")
            exception_handler.handle_exception(exception)
