# -*- coding: utf-8 -*-

from StringIO import StringIO

import pytest
import simplejson as json

from servalx import couch, environ

from .res import APK


@pytest.fixture()
def conn():
    print(environ.COUCH_ENDPOINT)
    return couch.Connection(environ.COUCH_ENDPOINT)


def test_can_perform_keys_request(conn):
    from itertools import islice

    generator = couch.keys(conn, conn.DB_APKINFOS)

    assert len(list(islice(generator, 10))) == 10
    assert len(list(islice(generator, 100))) == 100


def test_can_perform_head_request(conn):
    assert couch.head(conn, conn.DB_APKINFOS, APK.ID)
    assert not couch.head(conn, conn.DB_APKINFOS, APK.NO)


def test_can_perform_get_request(conn):
    assert set(couch.get(conn, conn.DB_APKINFOS, APK.ID)) == set(APK.APKINFOS)


def test_can_perform_raw_request(conn):
    actual = couch.raw(conn, conn.DB_APKINFOS, APK.ID)
    expect = couch.get(conn, conn.DB_APKINFOS, APK.ID, on_doc=couch.IDENTITY)

    assert json.loads(actual) == expect
    assert isinstance(actual, str)


def test_can_perform_rawall_request(conn):
    buffer = StringIO()
    keys = [APK.ID, APK.NO]
    chunks = couch.rawall(conn, conn.DB_APKINFOS, keys)
    expect = couch.get(conn, conn.DB_APKINFOS, APK.ID, on_doc=couch.IDENTITY)

    for chunk in chunks:
        buffer.write(chunk)

    res = json.loads(buffer.getvalue())
    d1, d2 = res["rows"]

    assert len(res["rows"]) == 2
    assert set(res.keys()) == {"rows", "total_rows"}

    assert d1["doc"] == expect
    assert d2 == {"error": "not_found", "key": APK.NO}
