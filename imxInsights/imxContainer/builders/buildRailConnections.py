from typing import Callable, List

from shapely import LineString, Point
from shapely.ops import linemerge

from imxInsights.exceptions import exception_handler
from imxInsights.exceptions.imxExceptions import (
    ImxRailConnectionRefNotPresent,
    ImxException,
    ImxTopologyExtensionNotPresent,
    ImxRailConnectionMultiLinestring,
)
from imxInsights.imxContainer.builders.buildExceptions import BuildExceptions
from imxInsights.imxContainer.tree.imxTreeObject import ImxObject
from imxInsights.utils.shapley_helpers import reverse_line


def build_rail_connections(
    get_by_types: Callable[[List[str]], List[ImxObject]],
    find: Callable[[str], ImxObject],
    exceptions: BuildExceptions,
):
    rail_connections = get_by_types(["RailConnection"])
    for rail_connection in rail_connections:
        if "trackRef" in rail_connection.element.attrib:
            track_ref = rail_connection.element.attrib["trackRef"]
        else:
            track_ref = None

        if "passageRefs" in rail_connection.element.attrib:
            passage_refs = rail_connection.element.attrib["passageRefs"].split(" ")
        else:
            passage_refs = []

        if len(passage_refs) == 0:
            passage_refs = rail_connection.element.findall(".//{*}PassageRefs")
            if len(passage_refs) == 0:
                passage_refs = []
            else:
                if passage_refs[0].text is None:
                    passage_refs = []
                elif " " in passage_refs[0].text:
                    passage_refs = passage_refs[0].text.split(" ")
                else:
                    passage_refs = [passage_refs[0].text]

        geometries = []
        if len(passage_refs) != 0:
            for passage_ref in passage_refs:
                passage_obj = find(passage_ref)
                if passage_obj is None:
                    exceptions.add(
                        ImxRailConnectionRefNotPresent(
                            msg=f"Passage {passage_ref} of rail_connection {rail_connection.puic} not present"
                        ), rail_connection.puic
                    )

                else:
                    geometries.append(passage_obj.geographic_location.shapely)

        if track_ref is not None:
            track_obj = find(track_ref)

            if track_obj is None:
                exceptions.add(
                    ImxRailConnectionRefNotPresent(
                        msg=f"Track {track_ref} of rail_connection {rail_connection.puic} not present"
                    ), rail_connection.puic
                )

            else:
                geometries.append(track_obj.geographic_location.shapely)

        if len(geometries) != 0:
            line_geometry = linemerge(geometries)
            if not isinstance(line_geometry, LineString):
                exceptions.add(
                    ImxRailConnectionRefNotPresent(
                        msg=f"RailConnection {rail_connection.puic} merge geometries results does not result in a single LineString"
                    ), rail_connection.puic
                )

            from_node_ref = rail_connection.properties.get(
                'extension_MicroLink.FromMicroNode.@nodeRef'
            )

            from_junction = find(from_node_ref)
            if from_junction is None:
                exceptions.add(
                    ImxRailConnectionRefNotPresent(
                        msg=f"RailConnection {rail_connection.puic} missing FromMicroNode"
                    ), rail_connection.puic
                )

            to_node_ref = rail_connection.properties.get(
                'extension_MicroLink.ToMicroNode.@nodeRef'
            )
            to_junction = find(to_node_ref)
            if to_junction is None:
                exceptions.add(
                    ImxRailConnectionRefNotPresent(
                        msg=f"RailConnection {rail_connection.puic} missing ToMicroNode"
                    ), rail_connection.puic
                )

            if from_junction is not None and to_junction is not None:
                first_coord_distance_from_from_node = Point(
                    line_geometry.coords[0]
                ).distance(from_junction.geographic_location.shapely)
                first_coord_distance_from_to_node = Point(
                    line_geometry.coords[0]
                ).distance(to_junction.geographic_location.shapely)

                if (
                    first_coord_distance_from_to_node
                    < first_coord_distance_from_from_node
                ):
                    line_geometry = reverse_line(line_geometry)

            rail_connection.geometry = line_geometry
