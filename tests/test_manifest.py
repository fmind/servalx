# -*- coding: utf-8 -*-

from StringIO import StringIO

import pytest

from servalx import manifest as Manifest

from .res import MANIFEST


def test_can_isomorph_valid_manifest_file():
    xmlfile = StringIO(MANIFEST.XML)  # mock

    assert Manifest.isomorph(xmlfile) == MANIFEST.DOC


def test_cannot_isomorph_invalid_manifest_file():
    xmlfile = StringIO(MANIFEST.INVALID_ROOT)  # mock

    with pytest.raises(Manifest.InvalidManifestFile) as error:
        Manifest.isomorph(xmlfile)

    assert "droid" in str(error)
    assert "Root tag should be manifest" in str(error)


def test_can_flatten_manifest_document():
    assert Manifest.flatten(MANIFEST.DOC) == MANIFEST.FLAT
