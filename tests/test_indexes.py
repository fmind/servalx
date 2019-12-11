# -*- coding: utf-8 -*-

import pytest
import simplejson as json

from servalx import indexes

from .res import APK, INDEX


@pytest.fixture()
def apkinfos():
    from .config import EXAMPLES
    import glob
    import os

    return glob.iglob(os.path.join(EXAMPLES, "apkinfos", "*.json"))


def test_can_compute_indexes_from_dex():
    doc = indexes.from_dex(APK.DVMINFOS)

    assert doc == INDEX.DEX


def test_can_compute_indexes_from_fileinfos():
    doc = indexes.from_files(APK.FILES)

    assert doc == INDEX.FILES


def test_can_compute_indexes_from_manifest():
    doc = indexes.from_manifest(APK.MANIFEST)

    assert doc == INDEX.MANIFEST


def test_can_compute_indexes_from_resources():
    doc = indexes.from_resources(APK.RESOURCES)

    assert doc == INDEX.RESOURCES


def test_can_compute_indexes_from_certificate():
    doc = indexes.from_certificate(APK.CERTIFICATE)

    assert doc == INDEX.CERTIFICATE


def test_can_compute_indexes_from_apkinfos():
    doc = indexes.from_apkinfos(APK.APKINFOS)

    assert doc == INDEX.APKINDEX


def test_can_compute_on_more_apkinfos(apkinfos):
    for path in apkinfos:
        with open(path, "r") as reader:
            infos = json.load(reader)
            index = indexes.from_apkinfos(infos)

            assert index is not None
