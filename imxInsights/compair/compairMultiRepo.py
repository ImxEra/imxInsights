from typing import Any

from imxInsights.compair.compairObject import ImxComparedObject


class ImxCompareMultiRepo:
    """
    A class to handle multi-repository comparisons of IMX objects.

    Attributes:
        values (dict[str, ImxComparedObject]): A dictionary holding compared objects.
    """

    def __init__(self):
        self.values: dict[str, ImxComparedObject] = {}

    @staticmethod
    def _is_priority_field(field):
        return field in ("@name", "@puic")

    @staticmethod
    def _get_all_properties_keys(imx_obj, add_extension_objects: bool = True):
        all_keys = set()
        for d in imx_obj:
            all_keys.update(d.properties.keys())
            all_keys.update(
                d.extension_properties.keys()
            ) if add_extension_objects else None
        return sorted(all_keys)

    def _sort_priority_keys(self, all_keys):
        priority_keys = [field for field in all_keys if self._is_priority_field(field)]
        non_priority_keys = [
            field for field in all_keys if not self._is_priority_field(field)
        ]
        return priority_keys + non_priority_keys

    @staticmethod
    def _get_container_properties(imx_obj):
        return {d.container_id: d.properties for d in imx_obj}

    @staticmethod
    def _get_container_extention_properties(imx_obj):
        return {d.container_id: d.extension_properties for d in imx_obj}

    @staticmethod
    def _get_merged_properties(
        container_properties: dict[str, dict], extension_properties: dict[str, dict]
    ):
        properties = {}
        for key, value in container_properties.items():
            properties[key] = value | extension_properties[key]
        return properties

    @staticmethod
    def _populate_diff(all_keys, container_properties, container_order):
        merged_dict: dict[str, list] = {key: [] for key in all_keys}
        for key in all_keys:
            for container_id in container_order:
                if container_id in container_properties:
                    value = container_properties[container_id].get(key, None)
                else:
                    value = None
                merged_dict[key].append((container_id, value))
        return merged_dict

    def _create_change_over_container_mapping(
        self, tree, container_order
    ) -> dict[str, ImxComparedObject]:
        out = {}
        for imx_obj in tree.get_all():
            sorted_keys = self._sort_priority_keys(
                self._get_all_properties_keys(imx_obj)
            )
            properties = self._get_merged_properties(
                self._get_container_properties(imx_obj),
                self._get_container_extention_properties(imx_obj),
            )
            merged_dict = self._populate_diff(sorted_keys, properties, container_order)

            container_dict: dict[str, Any] = {item: None for item in container_order}
            for item in imx_obj:
                container_dict[item.container_id] = item.tag
            merged_dict["tags"] = list(container_dict.items())
            tester = ImxComparedObject(merged_dict, container_order)

            # tester2 = tester.as_pandas_df()
            out[imx_obj[0].puic] = tester

        return out

    @classmethod
    def from_multi_repo(cls, tree, container_order):
        self = cls()
        self.values = self._create_change_over_container_mapping(tree, container_order)
        return self
