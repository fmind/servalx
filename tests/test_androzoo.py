# -*- coding: utf-8 -*-

import pytest

from servalx import androzoo, environ

from .res import APK


@pytest.fixture()
def api():
    return androzoo.AndrozooAPI(environ.ANDROZOO_APIKEY, environ.ANDROZOO_APIURL)


@pytest.fixture()
def apk():
    from .config import EXAMPLES
    import os

    return os.path.join(EXAMPLES, "a.apk")


def test_can_ping(api):
    assert androzoo.ping(api) is True


def test_can_is_present(api):
    assert androzoo.is_present(api, APK.ID) is True
    assert androzoo.is_present(api, APK.NO) is False


def test_can_download_locally_if_present(api):
    if environ.SUPPORT_ANDROZOO_LOCAL:
        assert len(androzoo.local_download(api, APK.ID).read()) == 669965


def test_can_download_remotely_if_present(api):
    assert len(androzoo.remote_download(api, APK.ID).read()) == 669965


def test_cannot_download_if_invalid_sha256(api):
    with pytest.raises(androzoo.AndrozooError) as error:
        androzoo.remote_download(api, "00000")
        assert APK.NO in str(error)
        assert "invalid sha256" in str(error)


def test_cannot_download_if_invalid_apikey(api):
    with pytest.raises(androzoo.AndrozooError) as error:
        api.key = "000000000000000000"
        androzoo.remote_download(api, APK.ID)
        assert APK.NO in str(error)
        assert "invalid apikey" in str(error)


def test_cannot_download_if_not_present(api):
    with pytest.raises(androzoo.NotFound) as not_found:
        androzoo.remote_download(api, APK.NO)
        assert APK.NO in str(not_found)


def test_cannot_download_if_not_authorized(api):
    with pytest.raises(androzoo.NotAuthorized) as not_authorized:
        api.key = "0000000000000000000000000000000000000000000000000000000000000000"
        androzoo.remote_download(api, APK.ID)
        assert APK.NO in str(not_authorized)


def test_can_upload_from_file_handler(api, apk):
    sha256 = androzoo.upload(api, open(apk, "rb"))

    assert sha256 == APK.ID
