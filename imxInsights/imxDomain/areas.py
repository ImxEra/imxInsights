from dataclasses import dataclass

from lxml import etree as ET
from shapely import Polygon

from imxInsights.utils.shapley_helpers import GmlShapleyFactory


@dataclass
class Areas:
    name: str
    coordinates: str
    shapely: Polygon

    @staticmethod
    def from_element(element: ET.Element) -> "Areas":
        coordinates = element.find(".//{http://www.opengis.net/gml}coordinates").text
        return Areas(
            name=element.tag,
            coordinates=coordinates,
            shapely=GmlShapleyFactory.gml_polygon_to_shapely(coordinates),
        )
