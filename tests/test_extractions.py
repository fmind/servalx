# -*- coding: utf-8 -*-

import json
import os

import pytest
from servalx import apk as Apk
from servalx import extractions

from .config import EXAMPLES
from .res import APK, DVM


@pytest.fixture()
def apk():
    return Apk.APK(os.path.join(EXAMPLES, "a.apk"), path=True)


def test_can_extract_debug(apk):
    debug = extractions.debug(apk)

    assert debug == DVM.DEBUG
    assert json.dumps(debug)


def test_can_extract_header(apk):
    header = extractions.header(apk)

    assert header == DVM.HEADER
    assert json.dumps(header)


def test_can_extract_fields(apk):
    fields = extractions.fields(apk)

    assert fields == DVM.FIELDS
    assert json.dumps(fields)


def test_can_extract_methods(apk):
    methods = extractions.methods(apk)

    assert methods == DVM.METHODS
    assert json.dumps(methods)


def test_can_extract_codes(apk):
    codes = extractions.codes(apk)

    # check all code objects contain these keys
    assert all("code" in c for c in codes.values())
    assert all("params" in c for c in codes.values())
    assert all("return" in c for c in codes.values())

    assert set(codes.keys()) == DVM.CODES
    assert json.dumps(codes)


def test_can_extract_classes(apk):
    classes = extractions.classes(apk)

    assert classes == DVM.CLASSES
    assert json.dumps(classes)


def test_can_extract_invokes(apk):
    invokes = extractions.invokes(apk)

    assert invokes == DVM.INVOKES
    assert json.dumps(invokes)


def test_can_extract_strings(apk):
    strings = extractions.strings(apk)

    assert strings == DVM.STRINGS
    assert json.dumps(strings)


def test_can_extract_dvm(apk):
    infos = extractions.dvm(apk)

    assert json.dumps(infos)
    assert frozenset(infos.keys()) == {
        "debug",
        "header",
        "fields",
        "methods",
        "classes",
        "invokes",
        "strings",
        "format",
    }


def test_can_extract_permissions(apk):
    assert extractions.permissions(apk) == APK.PERMISSIONS


def test_can_extract_files(apk):
    index = extractions.files(apk)

    assert index == APK.FILES
    assert json.dumps(index)

    with_dates = extractions.files_with_datetime(index)

    assert json.dumps(with_dates)
    # date format should be: 1900-01-01 01:01:01 (length: 19)
    assert all(len(x["datetime"]) == 19 for x in with_dates.values())


def test_can_extract_resources(apk):
    doc = extractions.resources(apk)

    assert doc == APK.RESOURCES
    assert json.dumps(doc)


# def test_can_extract_natives(apk):
#     natives = extractions.natives(apk)

#     assert natives == APK.NATIVES
#     assert json.dumps(natives)


def test_can_extract_manifest(apk):
    doc = extractions.manifest(apk)

    assert doc == APK.MANIFEST
    assert json.dumps(doc)


def test_can_extract_certificate(apk):
    certificate = extractions.certificate(apk)

    assert certificate == APK.CERTIFICATE
    assert json.dumps(certificate)

    with_range = extractions.certificate_with_daterange(certificate)

    assert json.dumps(with_range)
    assert with_range["valid_to"] == "2039-04-25 10:27:52"
    assert with_range["valid_from"] == "2014-04-24 10:27:52"


def test_can_extract_apk(apk):
    doc = extractions.apk(apk)

    assert json.dumps(doc)
    assert frozenset(doc.keys()) == {
        "VERSION",
        "dex",
        "sha256",
        # 'natives',
        "manifest",
        "fileinfos",
        "resources",
        "certificate",
    }
