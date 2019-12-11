# -*- coding: utf-8 -*-

import pytest

from servalx import dvm as Dvm

from .res import DVM


@pytest.fixture()
def dvm():
    from servalx import apk as Apk
    from .config import EXAMPLES
    import os

    return Apk.APK(os.path.join(EXAMPLES, "a.apk"), path=True).dvm


def test_can_get_filetype(dvm):
    assert dvm.filetype == DVM.FORMAT


def test_can_test_is_debug(dvm):
    assert not Dvm.is_debug(dvm)


def test_can_get_dvm_format(dvm):
    assert Dvm.xformat(dvm) == "DEX"
