# -*- coding: utf-8 -*-

import os

import pytest

from servalx import apk as Apk
from servalx import resources

from .res import RESOURCES


@pytest.fixture()
def resfile():
    from .config import EXAMPLES

    apk = Apk.APK(os.path.join(EXAMPLES, "a.apk"), path=True)

    return Apk.find_resources(apk)


def test_can_isomorph_resources_file(resfile):
    assert resources.isomorph(resfile) == RESOURCES.DOC
