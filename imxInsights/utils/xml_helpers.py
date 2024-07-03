from lxml import etree as ET


def trim_tag(tag: ET._Element | str) -> str:
    if isinstance(tag, ET._Element):
        tag = str(tag.tag)
    return tag.split("}")[1] if "}" in tag else tag


def find_base_entity(elem: ET._Element) -> ET._Element:
    while elem is not None and "puic" not in elem.keys():
        elem = elem.getparent()
    if elem is None:
        raise ValueError
    return elem


def find_parent_entity(elem: ET._Element) -> ET._Element | None:
    assert "puic" in elem.keys(), "Element has no puic!"
    try:
        parent = find_base_entity(elem.getparent())
    except ValueError:
        return None

    return parent if trim_tag(parent.tag) != "Project" else None


def lxml_element_to_dict(
    node: ET.Element, attributes: object = True, children: object = True
) -> dict[str, dict | str | list]:
    """
    Convert lxml.etree node into a dict. adapted from https://gist.github.com/jacobian/795571.

    Args:
        node (ET.Element): the lxml.etree node to convert into a dict
        attributes (Optional[bool]): include the attributes of the node in the resulting dict, defaults to True
        children: (Optional[bool]): include the children

    Returns:
        ( dict[str, dict | str | list]): A dictionary representation of the lxml.etree node


    """
    result = dict[str, dict | str | list]()
    if attributes:
        for key, value in node.attrib.items():
            result[f"@{key}"] = value

    if not children:
        return result

    for element in node.iterchildren():
        key = trim_tag(element)

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = lxml_element_to_dict(element)

        if key in result:
            match = result[key]
            if isinstance(match, list):
                match.append(value)
            else:
                result[key] = [match, value]
        else:
            result[key] = value

    return result


def find_parent_with_tag(element: ET.Element, tags: list[str]) -> ET.Element:
    """Iterate through parents until a parent with a tag in `tags` is found."""
    current_element = element
    while current_element is not None:
        current_element = current_element.getparent()
        if current_element is not None and current_element.tag in tags:
            return current_element
    return None
