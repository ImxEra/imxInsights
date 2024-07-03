from pathlib import Path
from lxml import etree as ET

from imxInsights.imxContainer.imxConainer import ImxContainer
from imxInsights.imxContainer.imxMultiContainer import ImxMultiContainer
from imxInsights.imxFile.imxSituationFile import ImxSituationFile
from loguru import logger


class ImxSituation(ImxContainer):
    """
    Represents a situation within an IMX container.

    Args:
        imx_container (Path or str): Path to the IMX container.
        situation (ElementTree.Element): The situation element.
        imx_file (ImxSituationFile): The IMX5 file associated with the situation.
    """

    def __init__(
        self,
        imx_container: Path | str,
        situation: ET.Element,
        imx_file: ImxSituationFile,
    ):
        super().__init__(imx_container)
        logger.info(f"processing {ET.QName(situation.tag).localname}")
        self.situation_type: str = situation.tag
        self._populate_tree(situation, imx_file)
        self.tree.build_extensions.handle_all()

    def _populate_tree(self, element: ET.Element, imx_file: ImxSituationFile):
        """
        Populates the tree with the given element and associated IMX5 file.

        Args:
            element (ElementTree.Element): The XML element to add to the tree.
            imx_file (ImxSituationFile): The associated IMX5 file.
        """
        self.tree.add_imx_element(element, imx_file, self.container_id)


class ImxSituationsContainer:
    def __init__(self, imx_container: Path | str):
        """
        Represents an IMX Situation container.

        Args:
            imx_container (Path or str): Path to the IMX container.
        """
        imx_container = Path(imx_container)
        logger.info(f"processing {imx_container.name}")
        self.file: ImxSituationFile = ImxSituationFile(imx_file_path=imx_container)
        self.situation: ImxSituation | None = None
        self.new_situation: ImxSituation | None = None
        self.initial_situation: ImxSituation | None = None
        # self.project_container: ImxMultiContainer | None = None

        logger.success(f"finished processing {self.file.path.name}")

        for situation_type, attribute_name in [
            ("Situation", "situation"),
            ("InitialSituation", "initial_situation"),
            ("NewSituation", "new_situation"),
        ]:
            situation = self.file.root.find(
                f".//{{http://www.prorail.nl/IMSpoor}}{situation_type}"
            )
            if situation is not None:
                imx_situation = ImxSituation(imx_container, situation, self.file)
                setattr(self, attribute_name, imx_situation)

        # if self.initial_situation is not None and self.new_situation is not None:
        #     self.project_container = ImxMultiContainer(
        #         [self.initial_situation, self.new_situation]
        #     )
