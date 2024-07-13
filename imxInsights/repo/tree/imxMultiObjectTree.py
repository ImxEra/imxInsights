from collections.abc import Iterable

from imxInsights.domain.imxObject import ImxObject
from imxInsights.repo.tree.imxObjectTree import ObjectTree


class MultiObjectTree(ObjectTree):
    """
    Represents a tree structure of multiple ImxObject lists.

    Inherits from ObjectTree.

    Attributes:
        Inherits attributes from ObjectTree.
    """

    def __init__(self):
        super().__init__()

    def objects(self) -> Iterable[list[ImxObject]]:  # type: ignore
        """
        Get an iterable of all ImxObjects in the tree.

        Returns:
            Iterable[ImxObject]: An iterable of all ImxObjects in the tree.
        """
        return list(self.tree_dict.values())

    def find(self, key: str | ImxObject) -> list[ImxObject]:  # type: ignore
        """
        Find an ImxObject by key or by another ImxObject.

        Args:
            key (Union[str, ImxObject]): The key or ImxObject to search for.

        Returns:
            Optional[ImxObject]: The found ImxObject, or None if not found.
        """
        if isinstance(key, ImxObject):
            key = key.puic

        if key not in self._keys:
            return []

        match = self.tree_dict[key]
        return match
