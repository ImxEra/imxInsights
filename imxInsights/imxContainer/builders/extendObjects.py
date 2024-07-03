from collections import defaultdict
from typing import Optional

from imxInsights.exceptions import ErrorLevelEnum, exception_handler
from imxInsights.exceptions.imxExceptions import ImxUnconnectedExtension
from imxInsights.imxContainer.builders.buildExceptions import BuildExceptions
from imxInsights.imxContainer.config import Configuration
from imxInsights.imxContainer.tree.imxTreeObject import ImxObject
from lxml import etree as ET

from imxInsights.imxFile.imxFile import ImxFile
from imxInsights.utils.helpers import flatten_dict


def extend_objects(
    tree_dict: defaultdict[str, list[ImxObject]],
    build_exceptions: BuildExceptions,
    imx_file: ImxFile,
    element: Optional[ET.Element],
    extent_property_dict: bool = True,
):
    def _extend_imx_object():
        extend = False
        imx_file_extension_obj = extension_object.imx_file
        if imx_file_extension_obj.file_hash == imx_object.imx_file.file_hash:
            extend = True
        elif (
            imx_file_extension_obj.base_reference.parentHashcode
            == imx_object.imx_file.file_hash
        ):
            extend = True
        else:
            build_exceptions.add(
                ImxUnconnectedExtension(
                    f"{imx_file_extension_obj.path} hash of base reference file is not valid, can not extend {imx_object.path} with puic {imx_object.puic}",
                    ErrorLevelEnum.WARNING
                ),
                puic_to_find,
            )

        if extend:
            imx_object.extend_imx_object(extension_object)
            if extent_property_dict:
                modified_extension_properties = {
                    f"extension_{extension_object.tag}." + key: value
                    for key, value in extension_object.properties.items()
                }
                imx_object.properties = flatten_dict(imx_object.properties | modified_extension_properties)

    # main methode
    version = imx_file.imx_version
    for object_type, ref_attr in Configuration.get_object_type_to_extend_config(
        version
    ).items():
        if element is None:
            objects = [
                ImxObject(element=element, imx_file=imx_file)
                for element in imx_file.root.findall(
                    f".//{{http://www.prorail.nl/IMSpoor}}{object_type}"
                )
            ]
        else:
            objects = [
                ImxObject(element=element, imx_file=imx_file)
                for element in element.findall(
                    f".//{{http://www.prorail.nl/IMSpoor}}{object_type}"
                )
            ]
        for extension_object in objects:
            puic_to_find = extension_object.properties[ref_attr[0]]
            if puic_to_find in tree_dict.keys():
                object_to_extend = tree_dict[puic_to_find]
                for imx_object in object_to_extend:
                    _extend_imx_object()
            else:
                build_exceptions.add(
                    ImxUnconnectedExtension(
                        f"{extension_object.path} reffed object with {puic_to_find} not present in dataset, can not extend object",
                        ErrorLevelEnum.WARNING
                    ),
                    puic_to_find,
                )
