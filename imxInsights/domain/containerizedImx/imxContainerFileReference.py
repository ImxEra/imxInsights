from dataclasses import dataclass

from lxml.etree import _Element as Element


@dataclass
class ImxContainerFileReference:
    """
    Represents a file reference.

    Attributes:
        parentDocumentName (str): The name of the parent document.
        parentHashcode (str): The hashcode of the parent document.
    """

    parentDocumentName: str
    parentHashcode: str

    @staticmethod
    def from_element(element: Element) -> "ImxContainerFileReference":
        """
        Create a FileReference instance from an XML element.

        Args:
            element (ET.Element): The XML element containing the file reference data.

        Returns:
            ImxContainerFileReference: An instance of FileReference with data from the element.
        """

        return ImxContainerFileReference(
            parentDocumentName=element.get("parentDocumentName", ""),
            parentHashcode=element.get("parentHashcode", ""),
        )
