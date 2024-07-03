from copy import deepcopy
from imxInsights.imxContainer.imx12.imx12Container import Imx12Container
from imxInsights.imxContainer.imxConainer import ImxContainer
from imxInsights.imxContainer.tree.imxObjectTree import ObjectTree
from imxInsights.imxContainer.tree.imxMulitObjectTree import MultiObjectTree


# todo: make sure merged is a deep deep copy of init


class ImxMultiContainer:
    """
    Represents a collection of ImxContainers.

    Attributes:
        containers (list[Imx12Container]): A list of ImxContainers.
        tree (ObjectTree): An ObjectTree representing the merged structure of all containers.
    """

    def __init__(self, containers: list[ImxContainer], version_safe: bool = True):
        """
        Initialize MultiContainer with a list of ImxContainers.

        Args:
            containers (list[Imx12Container]): A list of ImxContainers.
        """
        if version_safe:
            # todo: check if all container are the same version
            pass

        # this will copy the element not the references
        containers = deepcopy(containers)
        self.containers = [item for item in containers]
        self.container_order: list[str] = [
            item.container_id for item in self.containers
        ]
        self.tree = MultiObjectTree()
        self._merge_containers(self.containers)

    @staticmethod
    def _merge_tree(source_tree, destination_tree):
        """
        Merge two tree structures.

        Args:
            source_tree: The source tree to merge.
            destination_tree: The destination tree to merge into.
        """
        for key, value in source_tree.items():
            if key in destination_tree:
                destination_tree[key].extend(value)
            else:
                destination_tree[key] = list(value)

    @staticmethod
    def _remove_tree(source_tree, destination_tree):
        """
        Remove items from a tree structure.

        Args:
            source_tree: The source tree containing items to remove.
            destination_tree: The destination tree to remove items from.
        """
        for key, value in source_tree.items():
            if key in destination_tree:
                destination_tree[key] = [
                    item for item in destination_tree[key] if item not in value
                ]

    def _merge_containers(self, containers: list[ImxContainer]):
        """
        Merge the tree structures of multiple containers.

        Args:
            containers (list[ImxContainer]): The list of containers to merge.
        """
        for container in containers:
            self._merge_tree(container.tree.tree_dict, self.tree.tree_dict)
            self._merge_tree(
                container.tree.build_extensions.exceptions, self.tree.build_extensions.exceptions
            )
        self.tree.update_keys()

    def add_container(self, container: ImxContainer):
        """
        Add an ImxContainer to the MultiContainer.

        Args:
            container (ImxContainer): The container to add.
        """
        container = deepcopy(container)
        self.containers.append(container)
        self._merge_tree(container.tree.tree_dict, self.tree.tree_dict)
        self._merge_tree(container.tree.build_extensions.exceptions, self.tree.build_extensions.exceptions)

    def remove_container(self, container: ImxContainer):
        """
        Remove an ImxContainer from the MultiContainer.

        Args:
            container (ImxContainer): The container to remove.
        """
        self.containers.remove(container)
        self._remove_tree(container.tree.tree_dict, self.tree.tree_dict)
        self._remove_tree(container.tree.build_extensions.exceptions, self.tree.build_extensions.exceptions)

    def _create_change_over_container_mapping(self):
        out = []
        for imx_obj in self.tree.objects():
            merged_dict = {}
            all_keys = set()
            for d in imx_obj:
                all_keys.update(d.properties.keys())

            for key in all_keys:
                merged_dict[key] = []
                for d in imx_obj:
                    merged_dict[key].append({d.container_id: d.properties.get(key)})

            tag_list = [{item.container_id: item.path} for item in imx_obj]
            merged_dict['tags'] = tag_list
            out.append(merged_dict)
        return out

    @staticmethod
    def _merge_changes_with_container_ids(values, container_step_mapping):
        result = []
        previous_value = None
        for entry in values:
            for container_id, value in entry.items():
                if value != previous_value:
                    if previous_value is not None:
                        result.append(f"{container_step_mapping[container_id]}-> {value}")
                    else:
                        result.append(f"{value}")
                    previous_value = value
        return " | ".join(result)

    def get_change_timeline(self, container_step_mapping: dict):
        input_dicts = self._create_change_over_container_mapping()
        out = []
        for imx_object in input_dicts:
            merged_dict = {}
            for key, value in imx_object.items():
                merged_dict[key] = self._merge_changes_with_container_ids(value, container_step_mapping)
            sorted_dict = {key: merged_dict[key] for key in sorted(merged_dict)}
            out.append(sorted_dict)
        return out
