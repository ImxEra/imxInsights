from dataclasses import dataclass, field
from typing import Optional

from lxml import etree as ET
from shapely import Point, LineString, Polygon

from imxInsights.utils.shapley_helpers import GmlShapleyFactory


@dataclass
class ImxGeographicLocation:
    """
    Represents the geographic location of an object.

    Attributes:
        _element (ET.Element): The XML element containing the geographic location data.
        shapely (Point | LineString | Polygon): The geographic shape.
        azimuth (float | None): The azimuth angle, if available.
        data_acquisition_method (str | None): The data acquisition method, if available.
        accuracy (float | None): The accuracy of the geographic location, if available.
        srs_name (str | None): The spatial reference system name, if available.
    """

    _element: ET.Element
    shapely: Point | LineString | Polygon = field(init=False)
    azimuth: float | None = field(init=False)
    data_acquisition_method: str | None = field(init=False)
    accuracy: float | None = field(init=False)
    srs_name: str | None = field(init=False)

    @staticmethod
    def from_element(element: ET.Element) -> Optional['ImxGeographicLocation']:
        """
        Creates an ImxGeographicLocation instance from an XML element.

        Args:
            element (ET.Element): The XML element containing the geographic location data.

        Returns:
            ImxGeographicLocation: An instance of ImxGeographicLocation.
        """
        location_node = element.find(
            ".//{http://www.prorail.nl/IMSpoor}GeographicLocation"
        )
        if element.tag == "{http://www.prorail.nl/IMSpoor}ObservedLocation":
            location_node = element

        if location_node is None:
            return None

        self = ImxGeographicLocation(location_node)

        self.shapely = GmlShapleyFactory.shapley(location_node)
        self.data_acquisition_method = location_node.attrib.get("dataAcquisitionMethod")
        self.accuracy = float(location_node.attrib.get("accuracy", 0.0))
        self.azimuth = float(location_node.attrib.get("azimuth", 0.0))

        point_element = location_node.find(".//*[@srsName]")
        self.srs_name = (
            point_element.attrib.get("srsName") if point_element is not None else None
        )

        return self
