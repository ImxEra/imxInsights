import pytest

from imxInsights import ImxSingleFile, ImxContainer


@pytest.fixture(scope="module")
def imx_v124_project_instance(imx_v124_project_test_file_path) -> ImxSingleFile:
    return ImxSingleFile(imx_v124_project_test_file_path)


@pytest.fixture(scope="module")
def imx_v500_project_instance(imx_v500_project_test_file_path) -> ImxSingleFile:
    return ImxSingleFile(imx_v500_project_test_file_path)


@pytest.fixture(scope="module")
def imx_v1200_instance(imx_v1200_test_file_path) -> ImxContainer:
    return ImxContainer(imx_v1200_test_file_path)

