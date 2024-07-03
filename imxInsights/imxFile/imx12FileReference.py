from dataclasses import dataclass

from lxml import etree as ET


@dataclass
class Imx12FileReference:
    """
    Represents a file reference.

    Attributes:
        parentDocumentName (str): The name of the parent document.
        parentHashcode (str): The hashcode of the parent document.
    """

    parentDocumentName: str
    parentHashcode: str

    @staticmethod
    def from_element(element: ET.Element) -> "Imx12FileReference":
        """
        Create a FileReference instance from an XML element.

        Args:
            element (ET.Element): The XML element containing the file reference data.

        Returns:
            Imx12FileReference: An instance of FileReference with data from the element.
        """

        return Imx12FileReference(
            parentDocumentName=element.get("parentDocumentName"),
            parentHashcode=element.get("parentHashcode"),
        )
