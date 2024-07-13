import pytest

from tests.helpers import sample_path


@pytest.fixture(scope="module")
def imx_v124_project_test_file_path() -> str:
    return sample_path("124/20221018_V18_A_Hengelo_Zutphen_Wintersw_71_SK0240_Arcadis.xml")


@pytest.fixture(scope="module")
def imx_v500_project_test_file_path() -> str:
    # todo: change imx 500 file to one without duplicated dummies
    return sample_path("500/U_concept ENL 4b_000__RVTO_20240212_compleet_concept_imx500.xml")


@pytest.fixture(scope="module")
def imx_v1200_test_zip_file_path() -> str:
    return sample_path("1200/set 1 as zip.zip")
