import hashlib
import json
from pathlib import Path
from typing import Any


def hash_sha256(path: Path):
    """
    Calculate the SHA-256 hash sum of a file located at the specified path.

    This function takes a `Path` object representing the path to a file and
    calculates the SHA-256 hash sum of the file's contents. It returns the
    hash sum as a hexadecimal string.

    Args:
        path (Path): The path to the file for which the SHA-256 hash sum
            should be calculated.

    Returns:
        str: A hexadecimal string representing the SHA-256 hash sum of the file.

    Note:
        This function reads the entire contents of the file into memory
        to calculate the hash sum. For large files, this may consume a
        significant amount of memory. Make sure to handle large files
        appropriately when using this function.

    """
    return f"{hashlib.sha256(path.read_bytes()).hexdigest()}"


def hash_dict_ignor_nested(dictionary: dict) -> str:
    """
    Compute the SHA-1 hash of the dictionary's non-nested values.

    This function takes a dictionary as input and computes the SHA-1 hash of its
    content, excluding nested dictionaries. It extracts non-dictionary values
    from the input dictionary and creates a new dictionary containing only those
    values. Then, it sorts the keys of the new dictionary and computes the SHA-1
    hash of the resulting JSON-encoded string.

    Args:
        dictionary (Dict): The dictionary whose content should be hashed.

    Returns:
        str: A hexadecimal string representing the SHA-1 hash of the non-nested
             values in the dictionary.

    Note:
        This function excludes nested dictionaries when computing the hash,
        focusing only on non-dictionary values. If the input dictionary contains
        nested dictionaries, their content will not be included in the hash.
    """
    new_dict = {}
    for key, value in dictionary.items():
        if not isinstance(value, dict):
            new_dict[key] = value

    hash_object = hashlib.sha1(json.dumps(new_dict, sort_keys=True).encode())
    return hash_object.hexdigest()


def flatten_dict(
    data_dict: dict[str, dict | str | list],
    skip_key: str | None = "@puic",
    prefix="",
    sep=".",
) -> dict[str, str]:
    def _custom_sorting(key_, remaining_: list[dict]):
        mapping = {
            "RailConnectionInfo": "@railConnectionRef",
            "Announcement": "@installationRef",
        }
        if key_ in mapping.keys():
            return sorted(remaining_, key=lambda x: x[mapping[key_]])
        else:
            return sorted(remaining_, key=hash_dict_ignor_nested)

    result: dict[str, str] = {}

    # Skip root node if this is a recursive call and key is found
    if prefix and skip_key in data_dict:
        return result

    for key, value in data_dict.items():
        if not isinstance(value, list) and not isinstance(value, dict):
            result[f"{prefix}{key}"] = value
            continue

        new_prefix = f"{prefix}{key}{sep}"

        if (
            isinstance(value, list)
            and len(value) > 0
            and not isinstance(value[0], dict)
        ):
            # add index and add to current.
            for i, child in enumerate(value):
                result[f"{new_prefix}{i}"] = child
            continue

        # Multiple children -> list of dicts. Convert single dict to list with dict.
        if isinstance(value, dict):
            value = [value]

        assert len(value) > 0 and isinstance(value[0], dict)

        # Filter children with skip_key.
        remaining = list[dict]() if skip_key is not None else value
        if skip_key is not None:
            for child in value:
                if skip_key in child:
                    continue
                remaining.append(child)

        # Add index for each child if >1 and recurse, order can be changed in xml, so sort before indexing..
        if len(remaining) > 1:
            # sorting is done on a specified key.
            # if no key is present make hash of attributes, if no attributes hash first node attributes...
            remaining = _custom_sorting(key, remaining)

        for i, child in enumerate(remaining):
            child_prefix = f"{new_prefix}{i}{sep}" if len(remaining) > 1 else new_prefix
            flattened = flatten_dict(
                child, skip_key=skip_key, prefix=child_prefix, sep=sep
            )
            result = result | flattened

    return result


# def parse_to_nested_dict(flat_dict):
#     nested_dict = {}
#
#     for key, value in flat_dict.items():
#         parts = key.split(".")
#         d = nested_dict
#
#         for i, part in enumerate(parts[:-1]):
#             if part.isdigit():  # if part is a digit, treat it as a list index
#                 part = int(part)
#                 if not isinstance(d, list):
#                     # Convert d to a list if it is not already a list
#                     temp = d
#                     d = [None] * (part + 1)
#                     if isinstance(temp, dict):
#                         for k, v in temp.items():
#                             if k.isdigit():
#                                 d[int(k)] = v
#                             else:
#                                 d.append({k: v})
#                 while len(d) <= part:
#                     d.append({})
#                 if not isinstance(d[part], dict):
#                     d[part] = {}
#                 d = d[part]
#             else:
#                 if part not in d:
#                     d[part] = {}
#                 d = d[part]
#
#         final_part = parts[-1]
#         if final_part.isdigit():
#             final_part = int(final_part)
#             if not isinstance(d, list):
#                 d = [None] * (final_part + 1)
#             while len(d) <= final_part:
#                 d.append(None)
#             d[final_part] = value
#         else:
#             d[final_part] = value
#
#     return nested_dict


def parse_to_nested_dict(input_dict: dict[str, Any]) -> dict[str | int, Any]:
    result: dict[str | int, Any] = {}

    for key, value in input_dict.items():
        parts = key.split(".")
        d = result

        for part in parts[:-1]:
            if part.isdigit():
                part = str(part)
            if isinstance(d, list):
                d.append({})
                d = d[-1]
            if part not in d:
                d[part] = {}
            d = d[part]

        last_part = parts[-1]
        if last_part.isdigit():
            last_part = str(last_part)

        if isinstance(d, list):
            d.append(value)
        else:
            d[last_part] = value

    return result
