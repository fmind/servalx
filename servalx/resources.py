# -*- coding: utf-8 -*-
"""Extract information from resources files."""

from copy import deepcopy

# FUNCTIONS


def isomorph(resfile):
    """Return the content of the resources file as a dict."""
    assert resfile.analyzed

    values = deepcopy(resfile.values)

    # change the key of default lang to ASCII
    for package, languages in values.items():
        for lang in languages.keys():
            if lang == "\x00\x00":
                languages["DEFAULT"] = languages.pop(lang)

    return values
