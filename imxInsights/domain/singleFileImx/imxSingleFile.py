from pathlib import Path

from loguru import logger
from lxml.etree import QName
from lxml.etree import _Element as Element

from imxInsights.domain.imxFile import ImxFile
from imxInsights.repo.imxRepo import ImxRepo


class ImxSingleFile:
    """
    Represents an IMX file that contains project situations or just a situation.

    Args:
        imx_file_path: Path to the IMX container.

    Attributes:
        file: The IMX file.
        situation: The IMX Situation.
        new_situation: The IMX NewSituation.
        initial_situation: The IMX InitialSituation.

    """

    def __init__(self, imx_file_path: Path | str):
        imx_file_path = Path(imx_file_path)
        logger.info(f"processing {imx_file_path.name}")

        self.file: ImxFile = ImxFile(imx_file_path=imx_file_path)
        self.situation: ImxSituation | None = None
        self.new_situation: ImxSituation | None = None
        self.initial_situation: ImxSituation | None = None

        for situation_type, attribute_name in [
            ("Situation", "situation"),
            ("InitialSituation", "initial_situation"),
            ("NewSituation", "new_situation"),
        ]:
            if self.file.root is not None:
                situation = self.file.root.find(
                    f".//{{http://www.prorail.nl/IMSpoor}}{situation_type}"
                )
                if situation is not None:
                    imx_situation = ImxSituation(imx_file_path, situation, self.file)
                    setattr(self, attribute_name, imx_situation)

        logger.success(f"finished processing {self.file.path.name}")


class ImxSituation(ImxRepo):
    """
    Represents a IMX Situation.

    Attributes:
        situation_type: imx situation Type

    """

    def __init__(
        self,
        imx_file_path: Path,
        situation_element: Element,
        imx_file: ImxFile,
    ):
        super().__init__(imx_file_path)
        logger.info(f"processing {QName(situation_element.tag).localname}")
        # todo: make enum for imx type
        self.situation_type: str = situation_element.tag
        self._populate_tree(situation_element, imx_file)
        self._tree.build_extensions.handle_all()

    def _populate_tree(self, element: Element, imx_file: ImxFile):
        """
        Populates the tree with the given element and associated IMX5 file.

        Args:
            element (ElementTree.Element): The XML element to add to the tree.
            imx_file (ImxSituationFile): The associated IMX5 file.
        """
        self._tree.add_imx_element(element, imx_file, self.container_id)
