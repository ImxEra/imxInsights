import warnings
from typing import Optional, Iterable

from lxml import etree as ET
from shapely import GeometryCollection

from imxInsights.imxFile.imx12File import ImxDesignCoreFile, ImxDesignPetalFile
from imxInsights.imxFile.imxFile import ImxFile
from imxInsights.imxDomain.imxGeographicLocation import ImxGeographicLocation
from imxInsights.utils.helpers import flatten_dict, parse_to_nested_dict
from imxInsights.utils.xml_helpers import (
    find_parent_entity,
    lxml_element_to_dict,
    trim_tag,
    find_parent_with_tag,
)


class ImxObject:
    """
    Represents an object within an IMX file.
    """

    def __init__(
        self,
        element: ET.Element,
        imx_file: ImxFile,
        parent: Optional[ET.Element] = None,
    ):
        """
        Initializes an ImxObject.

        Args:
            element (ElementTree.Element): The XML element representing the object.
            imx_file (ImxFile): The IMX file associated with the object.
            parent (ElementTree.Element, optional): The parent XML element of the object. Defaults to None.
        """
        self._element: ET.Element = element
        self.imx_file: ImxFile | ImxDesignCoreFile | ImxDesignPetalFile = imx_file
        self.parent: Optional[ImxObject] = parent
        self.children: list["ImxObject"] = []
        self.imx_extensions: list["ImxObject"] = []
        self.geometry: GeometryCollection = GeometryCollection()
        self.properties: dict[str, str] = flatten_dict(lxml_element_to_dict(self._element))
        self.imx_situation: str = self._get_imx_situation()
        self.container_id: str | None = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: String representation of the object.
        """
        return f"<ImxObject {self.path} puic={self.puic} name='{self.name}'/>"

    def extend_imx_object(self, imx_extension_object: "ImxObject"):
        """
        Extends the current ImxObject with another ImxObject.

        Args:
            imx_extension_object (ImxObject): The ImxObject to extend with.
        """
        self.imx_extensions.append(imx_extension_object)

    @property
    def element(self) -> ET.Element:
        """
        Returns the XML element representing the object.

        Returns:
            ElementTree.Element: The XML element.
        """
        return self._element

    @property
    def tag(self) -> str:
        """
        Returns the tag of the XML element.

        Returns:
            str: The tag of the XML element.
        """
        return trim_tag(self._element.tag)

    @property
    def path(self) -> str:
        """
        Returns the path of the object within the XML structure.

        Returns:
            str: The path of the object.
        """
        tags = [parent.tag for parent in self._parents_generator()]
        tags.reverse()
        tags.append(self.tag)
        return ".".join(tags)

    @property
    def name(self) -> str:
        """
        Returns the name attribute of the XML element.

        Returns:
            str: The name attribute of the XML element.
        """
        return self._element.get("name", "")

    @property
    def puic(self) -> str:
        """
        Returns the puic attribute of the XML element.

        Returns:
            str: The puic attribute of the XML element.
        """
        return self._element.get("puic", "")

    @property
    def geographic_location(self) -> ImxGeographicLocation | None:
        """
        Returns the geographic location associated with the object.

        Returns:
            ImxGeographicLocation or None: The geographic location associated with the object.
        """
        return ImxGeographicLocation.from_element(self._element)

    def _get_imx_situation(self) -> str | None:
        """Retrieves the situation tag (pre imx 12.0) from the element.

        We cant use a property, copying will result in lost references.

        Returns:
            str | None: The situation or None if no matching is found.
        """
        namespace = "{http://www.prorail.nl/IMSpoor}"
        tags = [
            f"{namespace}Situation",
            f"{namespace}InitialSituation",
            f"{namespace}NewSituation",
        ]
        parent_element = find_parent_with_tag(self.element, tags)
        if parent_element is not None:
            return parent_element.tag.removeprefix(namespace)
        return None

    def _parents_generator(self) -> Iterable["ImxObject"]:
        """
        A generator that yields the parents of the object.

        Yields:
            ImxObject: The parent of the object.
        """
        parent = self.parent
        while True:
            if parent is None:
                break
            yield parent
            parent = parent.parent

    def can_compare(self, other: Optional["ImxObject"]) -> bool:
        """
        Checks if the object can be compared with another object.

        Args:
            other (ImxObject): The other ImxObject to compare with.

        Returns:
            bool: True if the objects can be compared, False otherwise.
        """
        if other is None:
            return True

        if other.puic != self.puic:
            return False

        if other.path != self.path:
            warnings.warn(
                f"Cant to compare {self.path} with {other.path}, tags do not match"
            )
            return False

        return True

    @staticmethod
    def _get_lookup_tree_from_element(entities: list[ET.Element], imx_file: ImxFile):
        """
        Generates a lookup tree from a list of XML entities.

        Args:
            entities (list[ElementTree.Element]): The list of XML entities.
            imx_file (ImxFile): The IMX file associated with the entities.

        Returns:
            list[ImxObject]: The lookup tree generated from the XML entities.
        """
        lookup = dict[ET.Element, ImxObject]()
        for entity in entities:
            parent = find_parent_entity(entity)

            if parent is not None:
                assert parent in lookup, "Expected parent in lookup"
                parent = lookup[parent]
            assert entity not in lookup

            lookup[entity] = ImxObject(parent=parent, element=entity, imx_file=imx_file)

        return list(lookup.values())

    @classmethod
    def lookup_tree_from_imx_file(cls, imx_file: ImxFile) -> list["ImxObject"]:
        """
        Generates a lookup tree from an IMX file.

        Args:
            imx_file (ImxFile): The IMX file.
            :param imx_file:

        Returns:
            list[ImxObject]: The lookup tree generated from the IMX file.
        """
        imx_key = "@puic"
        return cls._get_lookup_tree_from_element(
            imx_file.root.findall(f".//*[{imx_key}]"), imx_file
        )

    @classmethod
    def lookup_tree_from_element(
        cls, element: ET.Element, imx_file: ImxFile
    ) -> list["ImxObject"]:
        """
        Generates a lookup tree from a specific XML element within an IMX file.

        Args:
            element (ElementTree.Element): The XML element to start building the lookup tree from.
            imx_file (ImxFile): The IMX file associated with the XML element.

        Returns:
            list[ImxObject]: The lookup tree generated from the XML element.
        """
        imx_key = "@puic"
        return cls._get_lookup_tree_from_element(
            element.findall(f".//*[{imx_key}]"), imx_file
        )
