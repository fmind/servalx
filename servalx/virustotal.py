# -*- coding: utf-8 -*-
"""Client for VirusTotal API (external service)."""

import requests
from requests.compat import urljoin

# CONSTANTS

API_URL = "https://www.virustotal.com/vtapi/v2/"

FORMAT_SCAN_DATE = "%Y-%m-%d %H:%M:%S"

SCAN_RESPONSE_SET = frozenset(
    [
        "md5",
        "permalink",
        "resource",
        "response_code",
        "scan_id",
        "sha1",
        "sha256",
        "verbose_msg",
    ]
)

RESCAN_RESPONSE_SET = frozenset(
    ["permalink", "resource", "response_code", "scan_id", "sha256"]
)

REPORT_RESPONSE_SET = frozenset(
    [
        "md5",
        "permalink",
        "positives",
        "resource",
        "response_code",
        "scan_date",
        "scan_id",
        "scans",
        "sha1",
        "sha256",
        "total",
        "verbose_msg",
    ]
)

# ERRORS


class VTError(Exception):
    pass


class InvalidStatusCode(VTError):
    pass


class APILimitExceeded(InvalidStatusCode):
    pass


class FileSizeLimitExceeded(InvalidStatusCode):
    pass


class InsufficientPrivileges(InvalidStatusCode):
    pass


class InvalidResponseCode(VTError):
    pass


class ItemDoesNotExist(InvalidResponseCode):
    pass


class ItemIsCurrentlyQueued(InvalidResponseCode):
    pass


# HELPERS


def handle_http_errors(response, **kwargs):
    code = response.status_code
    msg = dict(kwargs, code=code)

    if code == 200:
        return None
    elif code == 204:
        raise APILimitExceeded(msg)
    elif code == 403:
        raise InsufficientPrivileges(msg)
    elif code == 413:
        raise FileSizeLimitExceeded(msg)
    else:
        raise InvalidStatusCode(msg)


def handle_api_errors(doc, **kwargs):
    error = doc.get("verbose_msg")
    code = doc.get("response_code")
    msg = dict(kwargs, code=code, error=error)

    if code == 1:
        return None
    elif code == 0:
        raise ItemDoesNotExist(msg)
    elif code == -2:
        raise ItemIsCurrentlyQueued(msg)
    else:
        raise InvalidResponseCode(msg)


# FUNCTIONS


class VirusTotalAPI(object):
    FILE_SCAN_URI = "file/scan"
    FILE_RESCAN_URI = "file/rescan"
    FILE_REPORT_URI = "file/report"

    def __init__(self, key, url=API_URL):
        self.key = key
        self.url = url


def file_scan(api, file_):
    """Send a scan request for a file."""
    params = {"apikey": api.key}
    files = {"file": ("file", file_)}
    url = urljoin(api.url, api.FILE_SCAN_URI)

    response = requests.post(url, files=files, params=params)
    context = {"request": api.FILE_SCAN_URI}
    handle_http_errors(response, **context)

    doc = response.json()
    handle_api_errors(doc, **context)

    return doc


def file_rescan(api, sha256):
    """Send a rescan request for a file."""
    headers = {"Accept-Encoding": "gzip, deflate"}
    params = {"apikey": api.key, "resource": sha256}
    url = urljoin(api.url, api.FILE_RESCAN_URI)

    response = requests.post(url, headers=headers, params=params)
    context = {"request": api.FILE_SCAN_URI, "sha256": sha256}
    handle_http_errors(response, **context)

    doc = response.json()
    handle_api_errors(doc, **context)

    return doc


def file_report(api, sha256):
    """Retrieve a report request for a file."""
    url = urljoin(api.url, api.FILE_REPORT_URI)
    headers = {"Accept-Encoding": "gzip, deflate"}
    params = {"apikey": api.key, "resource": sha256}

    response = requests.post(url, params=params, headers=headers)
    context = {"request": api.FILE_SCAN_URI, "sha256": sha256}
    handle_http_errors(response, **context)

    doc = response.json()
    handle_api_errors(doc, **context)

    return doc
