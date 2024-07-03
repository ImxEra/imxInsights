from pathlib import Path

from imxInsights.imxContainer.imxConainer import ImxContainer
from imxInsights.imxContainer.imx12.imx12ContainerMetadata import (
    Imx12ContainerMetadata,
)
from imxInsights.imxFile.imx12File import Imx12Files
from loguru import logger


class Imx12Container(ImxContainer):
    def __init__(self, imx_container: Path | str):
        """
        Represents an IMX12 container.

        Args:
            imx_container (Path or str): Path to the IMX12 container.
        """
        logger.info(f"processing {Path(imx_container).name}")
        super().__init__(imx_container)

        if not self.path.is_dir():
            raise ValueError("container is not a valid directory, zip or path string")

        self.files: Imx12Files = Imx12Files.from_container(
            container_path=self.path, container_id=self.container_id
        )

        self._populate_project_metadata()
        self._populate_tree()
        self.tree.build_extensions.handle_all()
        logger.success(f"finished processing {Path(imx_container).name}")

    def _populate_project_metadata(self):
        """
        Populate project metadata from the signaling design file.
        """
        self.project_metadata = Imx12ContainerMetadata.from_element(
            self.files.signaling_design.root
        )

    def _populate_tree(self):
        """
        Populate the tree with IMX files.
        """
        self.tree.add_imx_file(self.files.signaling_design, self.container_id)

        for petal in [
            "furniture",
            "train_control",
            "management_areas",
            "installation_design",
            "network_configuration",
            "schema_layout",
            "railway_electrification",
            "bgt",
            "observations",
        ]:
            imx_file = getattr(self.files, petal)
            if imx_file is not None:
                self.tree.add_imx_file(imx_file, self.container_id)
