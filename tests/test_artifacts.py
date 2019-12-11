# -*- coding: utf-8 -*-

from servalx import artifacts

from .res import APK, ARTIFACTS, LABEL, METAS


def is_valid(arts):
    return all(isinstance(k, str) and isinstance(v, set) for k, v in arts.items())


def test_can_index_from_metas():
    arts = artifacts.from_metas(METAS.DATABASE)

    assert is_valid(arts)
    assert arts == ARTIFACTS.META


def test_can_index_from_labels():
    arts = artifacts.from_labels(LABEL.EUPHONY)

    assert is_valid(arts)
    assert arts == ARTIFACTS.LABEL


def test_can_index_from_apkinfos():
    arts = artifacts.from_apkinfos(APK.APKINFOS)

    assert is_valid(arts)
    assert arts == ARTIFACTS.APK


def test_can_index_from_dex():
    arts = artifacts.from_dex(APK.APKINFOS["dex"])

    assert is_valid(arts)
    assert arts == ARTIFACTS.SOURCE


def test_can_index_manifest():
    arts = artifacts.from_manifest(APK.APKINFOS["manifest"])

    assert is_valid(arts)
    assert arts == ARTIFACTS.MANIFEST


def test_can_index_fileinfos():
    arts = artifacts.from_fileinfos(APK.APKINFOS["fileinfos"])

    assert is_valid(arts)
    assert arts == ARTIFACTS.FILE


def test_can_index_resources():
    arts = artifacts.from_resources(APK.APKINFOS["resources"])

    assert is_valid(arts)
    assert arts == ARTIFACTS.RESOURCE


def test_can_index_certificate():
    arts = artifacts.from_certificate(APK.APKINFOS["certificate"])

    assert is_valid(arts)
    assert arts == ARTIFACTS.CERTIFICATE
