from typing import Literal, cast, overload

from imxInsights.utils.singleton import SingletonMeta

VersionType = (
    Literal["1.2.4"]
    | Literal["5.0.0"]
    | Literal["10.0.0"]
    | Literal["11.0.0"]
    | Literal["12.0.0"]
)


def get_valid_version(version: str) -> VersionType:
    valid_versions = {"1.2.4", "5.0.0", "10.0.0", "11.0.0", "12.0.0"}
    if version not in valid_versions:
        raise ValueError(f"Invalid version: {version}")  # noqa: TRY003
    return cast(VersionType, version)


class Configuration(metaclass=SingletonMeta):
    """
    Configuration class using SingletonMeta to ensure a single instance.

    Info:
        The class maintains a mapping between IMX versions and their respective
        object type extension classes. The `get_object_type_to_extend_config` method
        fetches the appropriate class based on the provided IMX version and returns
        a dictionary of its non-callable attributes.
    """

    @staticmethod
    @overload
    def get_object_type_to_extend_config(
        imx_version: Literal["1.2.4"],
    ) -> "ObjectTypeToExtendImx1": ...

    @staticmethod
    @overload
    def get_object_type_to_extend_config(
        imx_version: Literal["5.0.0"],
    ) -> "ObjectTypeToExtendImx5": ...

    @staticmethod
    @overload
    def get_object_type_to_extend_config(
        imx_version: Literal["10.0.0"],
    ) -> "ObjectTypeToExtendImx10": ...

    @staticmethod
    @overload
    def get_object_type_to_extend_config(
        imx_version: Literal["12.0.0"],
    ) -> "ObjectTypeToExtendImx12": ...

    @staticmethod
    @overload
    def get_object_type_to_extend_config(
        imx_version: Literal["11.0.0"],
    ) -> "ObjectTypeToExtendImx11": ...

    @staticmethod
    def get_object_type_to_extend_config(imx_version: str):
        """
        Retrieves the object type extensions for a specific IMX version.

        Args:
            imx_version: The IMX version string.

        Returns:
            (ObjectTypeToExtendImx1 | ObjectTypeToExtendImx5 | ObjectTypeToExtendImx10 | ObjectTypeToExtendImx11 | ObjectTypeToExtendImx12): depending on imx version

        """
        version_map = {
            "1.2.4": ObjectTypeToExtendImx1,
            "5.0.0": ObjectTypeToExtendImx5,
            "10.0.0": ObjectTypeToExtendImx10,
            "11.0.0": ObjectTypeToExtendImx11,
            "12.0.0": ObjectTypeToExtendImx12,
        }

        object_type_class = version_map.get(imx_version)

        if object_type_class is None:
            return None
        return object_type_class
        # return {
        #     attr: getattr(object_type_class, attr)
        #     for attr in dir(object_type_class)
        #     if not callable(getattr(object_type_class, attr))
        #     and not attr.startswith("__")
        # }


class ObjectTypeToExtendImx1:
    """
    Contains object type extensions specific to IMX version 1.2.4.

    Attributes:
        MicroNode: Attributes for MicroNode objects: ["@junctionRef"].
        MicroLink: Attributes for MicroLink objects: ["@railConnectionRef"].
        FlankProtectionConfiguration: Attributes for FlankProtectionConfiguration objects: ["@switchMechanismRef", "@position"].
    """

    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: list[str] = ["@railConnectionRef"]
    FlankProtectionConfiguration: list[str] = ["@switchMechanismRef", "@position"]


class ObjectTypeToExtendImx5:
    """
    Contains object type extensions specific to IMX version 5.0.0.

    Attributes:
        MicroNode: Attributes for MicroNode objects.
        MicroLink: Attributes for MicroLink objects.
        ConditionNotification: Attributes for ConditionNotification objects.
        ErtmsLevelCrossing: Attributes for ErtmsLevelCrossing objects.
        ErtmsSignal: Attributes for ErtmsSignal objects.
        ErtmsBaliseGroup: Attributes for ErtmsBaliseGroup objects.
        ErtmsRoute: Attributes for ErtmsRoute objects.
    """

    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: list[str] = ["@implementationObjectRef"]
    ConditionNotification: list[str] = ["@objectRef"]
    ErtmsLevelCrossing: list[str] = ["@levelCrossingRef"]
    ErtmsSignal: list[str] = ["@signalRef"]
    ErtmsBaliseGroup: list[str] = ["@baliseGroupRef"]
    ErtmsRoute: list[str] = ["@signalingRouteRef"]


class ObjectTypeToExtendImx10:
    """
    Contains object type extensions specific to IMX version 10.0.0.

    Attributes:
        MicroNode: Attributes for MicroNode objects.
        MicroLink: Attributes for MicroLink objects.
        ConditionNotification: Attributes for ConditionNotification objects.
        ErtmsLevelCrossing: Attributes for ErtmsLevelCrossing objects.
        ErtmsSignal: Attributes for ErtmsSignal objects.
        ErtmsBaliseGroup: Attributes for ErtmsBaliseGroup objects.
        ErtmsRoute: Attributes for ErtmsRoute objects.
        FlankProtectionConfiguration: Attributes for FlankProtectionConfiguration objects.
    """

    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: list[str] = ["@implementationObjectRef"]
    ConditionNotification: list[str] = ["@objectRef"]
    ErtmsLevelCrossing: list[str] = ["@levelCrossingRef"]
    ErtmsSignal: list[str] = ["@signalRef"]
    ErtmsBaliseGroup: list[str] = ["@baliseGroupRef"]
    ErtmsRoute: list[str] = ["@functionalRouteRef"]
    FlankProtectionConfiguration: list[str] = ["@switchMechanismRef", "@switchPosition"]


class ObjectTypeToExtendImx11:
    """
    Contains object type extensions specific to IMX version 11.0.0.

    Attributes:
        MicroNode: Attributes for MicroNode objects.
        MicroLink: Attributes for MicroLink objects.
        ConditionNotification: Attributes for ConditionNotification objects.
        ErtmsLevelCrossing: Attributes for ErtmsLevelCrossing objects.
        ErtmsSignal: Attributes for ErtmsSignal objects.
        ErtmsBaliseGroup: Attributes for ErtmsBaliseGroup objects.
        ErtmsRoute: Attributes for ErtmsRoute objects.
    """

    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: list[str] = ["@implementationObjectRef"]
    ConditionNotification: list[str] = ["@objectRef"]
    ErtmsLevelCrossing: list[str] = ["@levelCrossingRef"]
    ErtmsSignal: list[str] = ["@signalRef"]
    ErtmsBaliseGroup: list[str] = ["@baliseGroupRef"]
    ErtmsRoute: list[str] = ["@functionalRouteRef"]


class ObjectTypeToExtendImx12:
    """
    Contains object type extensions specific to IMX version 12.0.0.

    Attributes:
        MicroNode: Attributes for MicroNode objects.
        MicroLink: Attributes for MicroLink objects.
        ConditionNotification: Attributes for ConditionNotification objects.
        ErtmsLevelCrossing: Attributes for ErtmsLevelCrossing objects.
        ErtmsSignal: Attributes for ErtmsSignal objects.
        ErtmsBaliseGroup: Attributes for ErtmsBaliseGroup objects.
        ErtmsRoute: Attributes for ErtmsRoute objects.
        ObservedLocation: Attributes for ObservedLocation objects.
    """

    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: list[str] = ["@implementationObjectRef"]
    ConditionNotification: list[str] = ["@objectRef"]
    ErtmsLevelCrossing: list[str] = ["@levelCrossingRef"]
    ErtmsSignal: list[str] = ["@signalRef"]
    ErtmsBaliseGroup: list[str] = ["@baliseGroupRef"]
    ErtmsRoute: list[str] = ["@functionalRouteRef"]
    ObservedLocation: list[str] = ["@objectRef"]
