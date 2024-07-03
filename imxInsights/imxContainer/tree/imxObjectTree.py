from collections import defaultdict
from itertools import chain
from typing import Iterable, Optional
from lxml import etree as ET

from imxInsights.exceptions import exception_handler
from imxInsights.exceptions.imxExceptions import (
    ImxDuplicatedPuicsInContainer,
    ImxException,
)
from imxInsights.imxContainer.builders.addRefs import add_refs
from imxInsights.imxContainer.builders.buildExceptions import BuildExceptions
from imxInsights.imxFile.imxFile import ImxFile
from imxInsights.imxContainer.tree.imxTreeObject import ImxObject

from imxInsights.imxContainer.builders.extendObjects import extend_objects
from imxInsights.imxContainer.builders.addChildren import add_children
from imxInsights.imxContainer.builders.buildRailConnections import (
    build_rail_connections,
)


class ObjectTree:
    def __init__(self):
        # todo: not private for easy debug, should be private, objects should return stuff
        self.tree_dict: defaultdict[str, list[ImxObject]] = defaultdict()
        self._keys: frozenset[str] = frozenset()
        self.build_extensions: BuildExceptions = BuildExceptions()

    @property
    def keys(self) -> frozenset[str]:
        return self._keys

    def update_keys(self) -> None:
        self._keys = frozenset[str]((key for key in self.tree_dict.keys()))

    def add_imx_element(
        self, element: ET.Element, imx_file: ImxFile, container_id: str
    ):
        tree_to_add = self._create_tree_dict(
            ImxObject.lookup_tree_from_element(element, imx_file), container_id
        )
        self._validate_and_build(tree_to_add, imx_file, element)

    def add_imx_file(self, imx_file: ImxFile, container_id: str) -> None:
        tree_to_add = self._create_tree_dict(
            ImxObject.lookup_tree_from_imx_file(imx_file), container_id
        )
        self._validate_and_build(tree_to_add, imx_file)

    def _validate_and_build(
        self,
        tree_to_add: defaultdict[str, list[ImxObject]],
        imx_file: ImxFile,
        element: Optional[ET.Element] = None,
    ):
        # container should contain unique puic objects, multiContainer will be matched on puic
        duplicates = [k for (k, v) in tree_to_add.items() if len(v) > 1]
        if len(duplicates) != 0:
            for puic in duplicates:
                self.build_extensions.add(ImxDuplicatedPuicsInContainer(), puic)

        for key, value in tree_to_add.items():
            if key not in self._keys:
                self.tree_dict[key] = value
            else:
                for item in value:
                    self.tree_dict[key].append(item)

        self.update_keys()

        extend_objects(self.tree_dict, self.build_extensions, imx_file, element)
        add_children(self.tree_dict, self.find)
        build_rail_connections(self.get_by_types, self.find, self.build_extensions)

        # todo: link ref and refs
        # add_refs(self.objects(), self.find, self.build_extensions)

        # todo: generate graph geometry
        # todo: classify area

    def get_by_types(self, object_types: list[str]) -> list[ImxObject]:
        return [
            item[0] for item in self.tree_dict.values() if item[0].tag in object_types
        ]

    def objects(self) -> Iterable[ImxObject]:
        duplicates = self.duplicates()
        if len(duplicates) != 0:
            raise ImxDuplicatedPuicsInContainer(data=duplicates)
        return chain(*self.tree_dict.values())

    def duplicates(self) -> list[str]:
        return [k for (k, v) in self.tree_dict.items() if len(v) > 1]

    def find(self, key: str | ImxObject) -> ImxObject | None:
        if isinstance(key, ImxObject):
            key = key.puic

        if key not in self._keys:
            return None

        match = self.tree_dict[key]
        assert len(match) == 1, f"KeyError, multiple results for {key}"
        return match[0]

    @staticmethod
    def _create_tree_dict(
        objects: Iterable[ImxObject], container_id: str
    ) -> defaultdict[str, list[ImxObject]]:
        result = defaultdict[str, list[ImxObject]](list)

        for o in objects:
            o.container_id = container_id
            result[o.puic].append(o)
        duplicated = [o for o in objects if len(result[o.puic]) != 1]
        assert (
            len(duplicated) == 0
        ), f"KeyError, multiple results for {[item.puic for item in duplicated]}"
        return result
