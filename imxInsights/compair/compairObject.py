from typing import Any, cast

from imxInsights.compair.compairField import ImxFieldCompair
from imxInsights.compair.compairStatusEnum import (
    CompairStatus,
    check_status_changed_deleted_or_created,
)

# import pandas as pd


def highlight_changes(value):
    color = ""
    if value == CompairStatus.NOT_PRESENT:
        color = "color: azure;"
    elif value in [CompairStatus.INITIAL_PRESENT, CompairStatus.NOT_CHANGED]:
        color = "border: 1px solid gray;"
    elif value == CompairStatus.CHANGED:
        color = "border: 3px solid green;"
    elif value == CompairStatus.CREATED:
        color = "border: 3px solid red;"
    elif value == CompairStatus.DELETED:
        color = "border: 3px solid blue;"

    return color


class ImxComparedObject:
    """
    Represents a compared object with fields and statuses.

    Attributes:
        fields: A list of ImxFieldCompair objects representing the fields.
        global_status: The global status of the compared object.
        container_status: The status of each container.

    Args:
        diff_data_dict: A dictionary containing the diff data.
        container_order: The order of containers, if tuple of dict the dict represents {'id': 'alias'}.
    """

    def __init__(
        self,
        diff_data_dict: dict[str, list[tuple[str, Any]]],
        container_order: tuple[str, ...] | tuple[dict[str, str], ...],
    ):
        # todo: make sure we can use a names container from the init of the compair,
        self._data: dict[str, list[tuple[str, Any]]] = diff_data_dict

        if all(isinstance(item, str) for item in container_order):
            # todo: try to remove the case, make sure we can handle aliases
            container_order = cast(tuple[str, ...], container_order)
            self._container_order: tuple[str, ...] = container_order
            self._container_aliases: tuple[str, ...] = tuple()

        elif all(isinstance(item, dict) for item in container_order):
            # todo: try to remove the case, make sure we can handle aliases
            container_order = cast(tuple[dict[str, str], ...], container_order)
            values, keys = [], []
            for dictionary in container_order:
                for key, value in dictionary.items():
                    keys.append(key)
                    values.append(value)
            self._container_order = tuple(keys)
            self._container_aliases = tuple(values)
        else:
            raise ValueError(  # noqa TRY003
                "container_order must be a tuple of strings or a tuple of dictionaries"
            )

        self.fields: list[ImxFieldCompair] = []
        self.global_status: CompairStatus = CompairStatus.NOT_CHANGED
        self.container_status: tuple[tuple[int, str, CompairStatus], ...] = tuple()

        self._post_init()

    def _post_init(self):
        self._set_compair_fields()
        self._determinate_global_change_status()
        self._determinate_container_change_status()

    @property
    def container_aliases(self) -> dict[str, str]:
        """
        Get the container aliases as a dict key=order, value is alias.

        Returns:
            A dictionary mapping container order to their aliases.
        """
        return dict(zip(self._container_order, self._container_aliases))

    def _set_compair_fields(self):
        for key, value in self._data.items():
            self.fields.append(ImxFieldCompair(key, value))

    def _determinate_global_change_status(self):
        status = [item.global_status for item in self.fields]
        if CompairStatus.CHANGED in status:
            self.global_status = CompairStatus.CHANGED

    def _determinate_container_change_status(self):
        container_status_list: dict[str, list] = {
            container: [] for container in self._container_order
        }
        for field_ in self.fields:
            for item in field_.values:
                container_status_list[item.container_id].append(item.status)

        self.container_status = tuple(
            (idx, value[0], check_status_changed_deleted_or_created(value[1]))
            for idx, value in enumerate(container_status_list.items())
        )

    # def apply_highlight(s):
    #     return [highlight_changes(val) for val in s]

    # def align_left_index(s):
    #     return ["text-align: left;" if s.name == "" else "" for _ in s]

    # def as_pandas_df(self):
    #     """
    #     Convert the compared object to a pandas DataFrame with styled HTML output.
    #
    #     !!! Warning
    #         In development!
    #
    #     Returns:
    #         None
    #     """
    #
    #     # columns = self._container_order
    #
    #     _: dict = {}
    #     _2: dict = {}
    #     for item in self.fields:
    #         _[item.name] = {}
    #         _2[item.name] = {}
    #         for item2 in item.values:
    #             _[item.name][item2.container_id] = item2.value
    #             _2[item.name][item2.container_id] = item2.status
    #     # df_values = pd.DataFrame.from_dict(_, orient="index")
    #     # df_changes = pd.DataFrame.from_dict(_2, orient="index")
    #     # styled_df = df_values.style.apply(
    #     #     lambda x: df_changes.applymap(highlight_changes), axis=None
    #     # )
    #     #
    #     # styled_df = df_values.style.apply(apply_highlight, axis=None)
    #
    #     df_values = pd.DataFrame.from_dict(_, orient="index")
    #     df_changes = pd.DataFrame.from_dict(_2, orient="index")
    #     styled_df = df_values.style.apply(
    #         lambda x: df_changes.applymap(highlight_changes),  # type: ignore
    #         axis=None,  # type: ignore
    #     )
    #
    #     styled_df.set_table_styles(
    #         [
    #             {"selector": ".row_heading", "props": [("text-align", "left")]},
    #             {"selector": "td", "props": [("font-family", "Roboto")]},
    #         ]
    #     )
    #
    #     html_table = styled_df.to_html()
    #     custom_css = """
    #     <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    #     <style>
    #         table {
    #             font-family: 'Roboto', sans-serif;
    #             font-size: 14px;
    #             border-collapse: collapse;
    #             width: 100%;
    #         }
    #         table, th, td {
    #             border: 1px solid black;
    #         }
    #         th, td {
    #             padding: 8px;
    #             text-align: left;
    #         }
    #     </style>
    #     """
    #     html_content = custom_css + html_table
    #     with open("styled_dataframe.html", "w") as f:
    #         f.write(html_content)
    #
    #     # https://devsnap.me/css-tables
    #
    #     print()
