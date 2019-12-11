# -*- coding: utf-8 -*-
"""Client for Androzoo API (internal service)."""

import io
import os

import requests
from requests.compat import urljoin

from servalx import environ, validators

# CONSTANTS

API_URL = "https://androzoo.uni.lu/api/"

META_COLUMNS = [
    "sha256",
    "sha1",
    "md5",
    "dex_date",
    "apk_size",
    "pkg_name",
    "vercode",
    "vt_detection",
    "vt_scan_date",
    "dex_size",
    "markets",
]

# ERRORS


class AndrozooError(Exception):
    pass


class NotFound(AndrozooError):
    pass


class NotAuthorized(AndrozooError):
    pass


class NotAllowed(AndrozooError):
    """Related to HTTP method."""

    pass


class ServerError(AndrozooError):
    pass


class UnknownHTTPCode(AndrozooError):
    pass


class InvalidSHA256(AndrozooError):
    pass


# CLASSES


class AndrozooAPI(object):
    PING_URI = "ping"
    UPLOAD_URI = "upload"
    DOWNLOAD_URI = "download"
    IS_PRESENT_URI = "is_present"

    def __init__(self, key, url=API_URL):
        self.key = key
        self.url = url


# HELPERS


def handle_http_errors(response, **kwargs):
    """Raise an exception based on the HTTP status code."""
    code = response.status_code

    if code == 200:
        return None

    msg = dict(kwargs, code=code)

    if code in {400, 403, 500}:
        doc = response.json()
        msg["error"] = doc.get("error")

    if code == 400:
        raise AndrozooError(msg)
    elif code == 403:
        raise NotAuthorized(msg)
    elif code == 404:
        raise NotFound(msg)
    elif code == 405:
        raise NotAllowed(msg)
    elif code == 500:
        raise ServerError(msg)
    else:
        raise UnknownHTTPCode(msg)


# FUNCTIONS


def ping(api):
    """Check if the server is alive."""
    url = urljoin(api.url, api.PING_URI)
    params = {"apikey": api.key}

    response = requests.get(url, params=params)
    handle_http_errors(response)
    doc = response.json()

    return doc.get("status") == "ok"


def is_present(api, sha256):
    """Check if an APK is present on Androzoo."""
    if not validators.is_sha256(sha256):
        raise InvalidSHA256()

    url = urljoin(api.url, api.IS_PRESENT_URI)
    params = {"apikey": api.key, "sha256": sha256}

    response = requests.get(url, params=params)
    handle_http_errors(response)
    doc = response.json()

    return doc.get("present")


def local_download(api, sha256):
    """Open an APK file from a local directory."""
    if not validators.is_sha256(sha256):
        raise InvalidSHA256()

    d1, d2 = sha256[0:2], sha256[2:4]
    path = os.path.join(environ.ANDROZOO_APIDIR, d1, d2, sha256.upper())

    if not os.path.exists(path):
        raise NotFound("APK file does not exist locally at: {}".format(path))

    return open(path, "rb")


def remote_download(api, sha256):
    """Stream an APK and wrap it in a BytesIO."""
    if not validators.is_sha256(sha256):
        raise InvalidSHA256()

    url = urljoin(api.url, api.DOWNLOAD_URI)
    params = {"apikey": api.key, "sha256": sha256}

    response = requests.get(url, params=params)
    handle_http_errors(response, sha256=sha256)
    doc = response.content

    return io.BytesIO(doc)


download = local_download if environ.SUPPORT_ANDROZOO_LOCAL else remote_download


def upload(api, file, market="unknown"):
    """Upload an APK and return its sha256 if the operation succeed."""
    url = urljoin(api.url, api.UPLOAD_URI)
    data = {"market": market, "filename": "file"}
    params = {"apikey": api.key}
    files = {"file": file}

    response = requests.post(url, params=params, data=data, files=files)
    handle_http_errors(response)
    doc = response.json()

    return doc.get("sha256").lower()
