# -*- coding: utf-8 -*-
"""Extract information from Manifest files."""

import xml.etree.cElementTree as ET
from collections import defaultdict
from copy import deepcopy

# ERRORS


class ManifestError(Exception):
    pass


class InvalidManifestFile(ManifestError):
    pass


# FUNCTIONS


def isomorph(xmlfile):
    """Convert a XML file to an isomorphic data structure."""
    elements = ET.iterparse(xmlfile, events=("start", "end"))

    def nsstrip(text):
        return text if "}" not in text else text.split("}")[1]

    def make_element(e):
        children = []
        tag = nsstrip(e.tag)
        text = e.text.strip() if e.text else ""
        attrs = {nsstrip(k).lower(): v.lower() for k, v in e.attrib.items()}
        return {"tag": tag, "text": text, "attrs": attrs, "_children": children}

    def parse_elements(iterator, current, parents):
        event, e = iterator.next()

        if event == "start":
            element = make_element(e)
            current["_children"].append(element)
            parents.append(current)
            return parse_elements(iterator, element, parents)
        elif event == "end" and len(parents) != 0:
            element = parents.pop()
            return parse_elements(iterator, element, parents)
        else:
            return current

    # create root element
    _, e = elements.next()
    root = make_element(e)
    tag = root["tag"].lower()

    if tag != "manifest":
        raise InvalidManifestFile("Root tag should be manifest, not: {0}".format(tag))

    return parse_elements(elements, root, [])


def flatten(doc):
    """Flatten a manifest document into a list of elements."""
    elements = list()
    nodes = [deepcopy(doc)]

    # depth-first search
    while len(nodes) != 0:
        n = nodes.pop()
        children = n.pop("_children")

        # HACK: fix a bug when isormoph() attrs key were not lower
        n["attrs"] = {k.lower(): v for k, v in n["attrs"].items()}

        elements.append(n)
        nodes.extend(children)

    return elements
