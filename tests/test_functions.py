# -*- coding: utf-8 -*-

import os

from servalx import functions

from .config import EXAMPLES
from .res import APK


def test_can_flatten_and_unflatten_dict():
    inputx = {0: {"a": "a"}, 1: {"b": "b"}}
    output = functions.flatten(inputx)
    resput = functions.unflatten(output)
    expect = [{"a": "a", "ID": 0}, {"b": "b", "ID": 1}]

    assert output == expect  # flatten
    assert inputx == resput  # unflatten
    assert inputx != output  # immutability


def test_can_compute_sha256():
    with open(os.path.join(EXAMPLES, "a.apk"), "r") as r:
        assert functions.compute_sha256(r.read()) == APK.ID
