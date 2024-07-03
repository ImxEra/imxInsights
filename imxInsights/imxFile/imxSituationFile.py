from pathlib import Path

from imxInsights.imxFile.imxFile import ImxFile


class ImxSituationFile(ImxFile):
    def __init__(self, imx_file_path: Path):
        super().__init__(imx_file_path)
