import pytest

from imxInsights import ImxContainer, ImxSingleFile


@pytest.mark.slow
def test_imx_parse_project_v124(imx_v124_project_instance):
    imx = imx_v124_project_instance
    assert imx.file.imx_version == "1.2.4", "imx version should be 1.2.4"


@pytest.mark.slow
def test_imx_parse_project_v500(imx_v500_project_instance):
    imx = imx_v500_project_instance
    assert imx.file.imx_version == "5.0.0", "imx version should be 5.0.0"




def test_load_500():
    imx_500 = ImxSingleFile(
        r"C:\Users\marti\OneDrive - ProRail BV\ENL\TVP1\RVTO 3.0\ENL_4.7_HL_10_001 v3.0 RVTO ENL Fase EDL HL\Bijlage 16 - IMX\IMX\O_O_D-003122_ERTMS Noordelijke lijnen TVP01 Leeu_01_2024-04-12T08_20_28Z.xml"
    )
    assert imx_500 is not None, "Should be object"


# def test_load_1000():
#     imx_1000 = ImxSituationsContainer(r"C:\Users\marti\PycharmProjects\testMultiFiles\sample_data\set_3\Thales_Modelstation3_imx10.xml")


# def test_load_1100():
#     imx_1100 = ImxSituationsContainer(r"C:\Users\marti\PycharmProjects\testMultiFiles\sample_data\set_3\Thales_Modelstation3_imx11.xml")


def test_load_1200_dir():
    imx_1200_from_dir = ImxContainer(
        r"C:\Users\marti\PycharmProjects\testMultiFiles\sample_data\set_1"
    )
    assert imx_1200_from_dir is not None, "Should be object"
    print()


def test_load_1200_zip():
    imx_1200_from_zip = ImxContainer(
        r"C:\Users\marti\PycharmProjects\testMultiFiles\sample_data\set 1 as zip.zip"
    )
    assert imx_1200_from_zip is not None, "Should be object"
    print()
