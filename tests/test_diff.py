test_data_container_order_list = (
    "container-1",
    "container-2",
    "container-3",
    "container-4",
    "container-5",
)

test_data_container_order_dict = (
    {"container-1": "A"},
    {"container-2": "B"},
    {"container-3": "C"},
    {"container-4": "D"},
    {"container-5": "E"},
)

test_data_fields = {
    "initial_present_changed_deleted_created__deleted_case": [
        ("container-1", "3A/B"),
        ("container-2", "3A/C"),
        ("container-3", None),
        ("container-4", "NewValue"),
        ("container-5", None),
    ],
    "not_changed_case": [
        ("container-1", "1"),
        ("container-2", "1"),
        ("container-3", "1"),
        ("container-4", "1"),
        ("container-5", "1"),
    ],
    "initial_present_deleted_3x_not_present_created_case": [
        ("container-1", "1:15"),
        ("container-2", None),
        ("container-3", None),
        ("container-4", None),
        ("container-5", "2:30"),
    ],
    "not_present_created_deleted_created_changed_case": [
        ("container-1", None),
        ("container-2", "True"),
        ("container-3", None),
        ("container-4", "False"),
        ("container-5", "True"),
    ],
    "initial_present_deleted_created_changed_deleted": [
        ("container-1", "60"),
        ("container-2", None),
        ("container-3", "60"),
        ("container-4", "90"),
        ("container-5", None),
    ],
    "not_present_created_deleted_created_deleted_case": [
        ("container-1", None),
        ("container-2", "NewlyCreated"),
        ("container-3", None),
        ("container-4", "Updated"),
        ("container-5", None),
    ],
    "initial_present_deleted_2x_not_present_created_case": [
        ("container-1", "Existing"),
        ("container-2", None),
        ("container-3", None),
        ("container-4", None),
        ("container-5", "Deleted"),
    ],
    "initial_present_updated_case": [
        ("container-1", "True"),
        ("container-2", "False"),
        ("container-3", "True"),
        ("container-4", "True"),
        ("container-5", "Updated"),
    ],
    "empty_case": [
        ("container-1", None),
        ("container-2", None),
        ("container-3", None),
        ("container-4", None),
        ("container-5", None),
    ],
}

# tester = ImxComparedObject(test_data_fields, test_data_container_order_dict)
# tester_df = tester.as_pandas_df()
# print()
