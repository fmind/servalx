# -*- coding: utf-8 -*-

import json

import pytest
from androguard.core.bytecodes.apk import ARSCParser

from servalx import apk as Apk

from .res import APK


@pytest.fixture()
def apk():
    from .config import EXAMPLES
    import os

    return Apk.APK(os.path.join(EXAMPLES, "a.apk"), path=True)


def test_can_find_files(apk):
    files = list(Apk.find_files(apk))

    assert len(files) == 22
    assert all(file and info for file, info in files)


# def test_can_find_natives(apk):
#     natives = list(Apk.find_natives(apk))

#     assert len(natives) == 1
#     fd, info, magic = natives[0]

#     assert fd is not None
#     assert info.filename == 'lib/armeabi-v7a/libNativeABI.so'
#     assert magic == 'ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV)'


def test_can_find_manifest(apk):
    fd, info = Apk.find_manifest(apk)

    assert fd is not None
    assert info.filename == "AndroidManifest.xml"


def test_can_find_resources(apk):
    res = Apk.find_resources(apk)

    assert isinstance(res, ARSCParser)
    assert res.analyzed


def test_can_find_certificate(apk):
    fd, info = Apk.find_certificate(apk)

    assert fd is not None
    assert info.filename == "META-INF/CERT.RSA"


def test_can_compute_sha256(apk):
    resources = Apk.compute_sha256(apk)

    assert resources == APK.ID
    assert json.dumps(resources)
