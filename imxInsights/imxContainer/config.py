from imxInsights.utils.singleton import SingletonMeta


class ObjectTypeToExtendImx1:
    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: list[str] = ["@railConnectionRef"]
    FlankProtectionConfiguration: list[str] = ["@switchMechanismRef", "@position"]


class ObjectTypeToExtendImx5:
    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: set[str] = ["@implementationObjectRef"]
    ConditionNotification: set[str] = ["@objectRef"]
    ErtmsLevelCrossing: set[str] = ["@levelCrossingRef"]
    ErtmsSignal: set[str] = ["@signalRef"]
    ErtmsBaliseGroup: set[str] = ["@baliseGroupRef"]
    ErtmsRoute: set[str] = ["@signalingRouteRef"]


class ObjectTypeToExtendImx10:
    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: list[str] = ["@implementationObjectRef"]
    ConditionNotification: set[str] = ["@objectRef"]
    ErtmsLevelCrossing: set[str] = ["@levelCrossingRef"]
    ErtmsSignal: set[str] = ["@signalRef"]
    ErtmsBaliseGroup: set[str] = ["@baliseGroupRef"]
    ErtmsRoute: set[str] = ["@functionalRouteRef"]
    FlankProtectionConfiguration: list[str] = ["@switchMechanismRef", "@switchPosition"]


class ObjectTypeToExtendImx11:
    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: set[str] = ["@implementationObjectRef"]
    ConditionNotification: set[str] = ["@objectRef"]
    ErtmsLevelCrossing: set[str] = ["@levelCrossingRef"]
    ErtmsSignal: set[str] = ["@signalRef"]
    ErtmsBaliseGroup: set[str] = ["@baliseGroupRef"]
    ErtmsRoute: set[str] = ["@functionalRouteRef"]


class ObjectTypeToExtendImx12:
    MicroNode: list[str] = ["@junctionRef"]
    MicroLink: set[str] = ["@implementationObjectRef"]
    ConditionNotification: set[str] = ["@objectRef"]
    ErtmsLevelCrossing: set[str] = ["@levelCrossingRef"]
    ErtmsSignal: set[str] = ["@signalRef"]
    ErtmsBaliseGroup: set[str] = ["@baliseGroupRef"]
    ErtmsRoute: set[str] = ["@functionalRouteRef"]
    ObservedLocation: set[str] = ["@objectRef"]


class Configuration(metaclass=SingletonMeta):
    @staticmethod
    def get_object_type_to_extend_config(imx_version: str):
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

        return {
            attr: getattr(object_type_class, attr)
            for attr in dir(object_type_class)
            if not callable(getattr(object_type_class, attr))
            and not attr.startswith("__")
        }
