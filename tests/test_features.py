# -*- coding: utf-8 -*-

import json
from numbers import Number

import pytest

from servalx import features

from .res import APK, DVM, FEATS


@pytest.fixture()
def apkinfos():
    from .config import EXAMPLES
    import glob
    import os

    return glob.iglob(os.path.join(EXAMPLES, "apkinfos", "*.json"))


def test_can_find_package_from_apkinfos():
    package = features.find_package(APK.APKINFOS)

    assert package == APK.PACKAGE == "air.jp.co.studio.arcana.regwoosh"


def test_can_compute_features_from_debug():
    doc = features.from_debug(DVM.DEBUG)

    assert doc == FEATS.DEBUG


def test_can_compute_features_from_header():
    doc = features.from_header(DVM.HEADER)

    assert doc == FEATS.HEADER


def test_can_compute_features_from_fields():
    doc = features.from_fields(DVM.FIELDS)

    assert doc == FEATS.FIELDS


def test_can_compute_features_from_methods():
    doc = features.from_methods(DVM.METHODS)

    assert doc == FEATS.METHODS


def test_can_compute_features_from_classes():
    doc = features.from_classes(DVM.CLASSES)

    assert doc == FEATS.CLASSES


def test_can_compute_features_from_invokes():
    doc = features.from_invokes(DVM.INVOKES, APK.PACKAGE)

    assert doc == FEATS.INVOKES


def test_can_compute_features_from_strings():
    doc = features.from_strings(DVM.STRINGS)

    assert doc == FEATS.STRINGS


def test_can_compute_features_from_dex():
    doc = features.from_dex(DVM.DVMINFOS, APK.PACKAGE)

    assert doc == FEATS.DEX
    assert all(isinstance(k, str) for k in doc.keys())
    assert all(isinstance(v, Number) for v in doc.values())


def test_can_compute_features_from_files():
    doc = features.from_files(APK.FILES)

    assert doc == FEATS.FILESINFOS


def test_can_compute_features_from_manifest():
    doc = features.from_manifest(APK.MANIFEST)

    assert doc == FEATS.MANIFEST


def test_can_compute_features_from_certificate():
    doc = features.from_certificate(APK.CERTIFICATE, APK.DEX_DATE)

    assert doc == FEATS.CERTIFICATE


def test_can_compute_from_apkinfos():
    doc = features.from_apkinfos(APK.APKINFOS)

    assert doc == FEATS.APKFEATS
    assert all(isinstance(k, str) for k in doc.keys())
    assert all(isinstance(v, Number) for v in doc.values())


def test_can_compute_on_more_apkinfos(apkinfos):
    for path in apkinfos:
        with open(path, "r") as reader:
            infos = json.load(reader)
            feats = features.from_apkinfos(infos)

            assert feats is not None
