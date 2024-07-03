from imxInsights.exceptions import exception_handler
from imxInsights.exceptions.imxExceptions import ImxDuplicatedPuicsInContainer
from typing import Dict, List, Callable, Any


def add_children(tree_dict: Dict[str, List[Any]], find: Callable[[str], Any]) -> None:
    """
    Add children to each object in the tree.

    Args:
        tree_dict (Dict[str, List[Any]]): The tree dictionary containing lists of objects.
        find (Callable[[str], Any]): A function to find an object by its key.

    Raises:
        ImxDuplicatedPuicsInContainer: If duplicate PUICs are found in a list of objects.
    """
    for value in tree_dict.values():
        value = value[0]

        elements_with_puic = value.element.xpath(".//*[@puic]")
        children = []
        for element in elements_with_puic:
            element_puic = element.get("puic")
            if value.puic != element_puic:
                children.append(find(element_puic))
        value.children = children
