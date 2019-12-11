# -*- coding: utf-8 -*-
"""Object representing an Android application (APK)."""

import re
from StringIO import StringIO

import magic as Magic
from androguard.core.bytecodes import apk as AndroAPK

from servalx import functions
from servalx.dvm import DVM

# CONSTS

ELF_MAGIC_PATTERN = re.compile(r"ELF", re.IGNORECASE)
CERT_FILE_PATTERN = re.compile(r"META-INF/\w+\.(RSA|DSA)", re.IGNORECASE)

# ERRORS


class APKError(Exception):
    pass


class InvalidAPK(APKError):
    pass


# CLASSES


class APK(object):
    def __init__(self, apkfile, path=False):
        """Create an object from an APK file.
        path=False: file content, path=True: file path."""
        self._apk = AndroAPK.APK(apkfile, raw=not path)
        self.dvm = DVM(self._apk.get_dex())


# FUNCTIONS


def find_files(apk, with_magic=False):
    """Find all the files contained in an APK object."""

    for name in apk._apk.zip.namelist():
        file = apk._apk.zip.open(name)
        info = apk._apk.zip.getinfo(name)

        if not with_magic:
            yield file, info
        else:
            magic = Magic.from_buffer(file.read(1024))
            # cannot use seek(0) on zip files
            # we have to re-open the file
            file = apk._apk.zip.open(name)
            yield file, info, magic


# def find_natives(apk):
#     """Find only native files contained in an APK object."""
#     for file, info, magic in find_files(apk, with_magic=True):
#         if ELF_MAGIC_PATTERN.match(magic):
#             yield file, info, magic


def find_manifest(apk):
    """Find the Android Manifest file in an APK object."""
    pattern = re.compile("AndroidManifest.xml", re.IGNORECASE)

    for file, info in find_files(apk):
        if pattern.match(info.filename):
            # we let androguard handle the parsing of the manifest: file -> axml
            buffer = StringIO(apk._apk.get_android_manifest_axml().get_buff())
            return buffer, info


def find_resources(apk):
    """Find Android Resources in an APK object."""
    res = apk._apk.get_android_resources()
    res._analyse()

    return res


def find_certificate(apk):
    """Find the developer certificate in an APK object."""
    for file, info in find_files(apk):
        if CERT_FILE_PATTERN.match(info.filename):
            return file, info


def compute_sha256(apk):
    """Compute the SHA256 of the APK object."""
    buffer = apk._apk.get_raw()

    return functions.compute_sha256(buffer)
