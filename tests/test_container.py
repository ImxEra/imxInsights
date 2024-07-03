from imxInsights import ImxSituationsContainer, Imx12Container, ImxMultiContainer
import time


# def test_load_124():
#     imx_124 = ImxSituationsContainer(r"C:\Users\marti\Downloads\O_R-481800_000_100029_DO_2024-05-31T08_56_59Z.xml")
#
#
# def test_load_500():
#     imx_500 = ImxSituationsContainer(r"C:\Users\marti\OneDrive - ProRail BV\ENL\TVP1\RVTO 3.0\ENL_4.7_HL_10_001 v3.0 RVTO ENL Fase EDL HL\Bijlage 16 - IMX\IMX\O_O_D-003122_ERTMS Noordelijke lijnen TVP01 Leeu_01_2024-04-12T08_20_28Z.xml")
#
#
# def test_load_1000():
#     imx_1000 = ImxSituationsContainer(r"C:\Users\marti\PycharmProjects\testMultiFiles\sample_data\set_3\Thales_Modelstation3_imx10.xml")
#
#
# def test_load_1100():
#     imx_1100 = ImxSituationsContainer(r"C:\Users\marti\PycharmProjects\testMultiFiles\sample_data\set_3\Thales_Modelstation3_imx11.xml")


def test_load_1200_dir():
    imx_1200_from_dir = Imx12Container(
        r"C:\Users\marti\PycharmProjects\testMultiFiles\sample_data\set_1"
    )
    print()


# def test_load_1200_zip():
#     imx_1200_from_zip = Imx12Container(
#         r"C:\Users\marti\PycharmProjects\testMultiFiles\sample_data\set 1 as zip.zip"
#     )
#
