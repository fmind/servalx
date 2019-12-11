# -*- coding: utf-8 -*-
"""Validator functions for the servalx project."""

import re

import magic

# CONSTANTS

SHA256_RE = re.compile(r"^[A-F0-9]{64}$", re.IGNORECASE)
APK_MAGICS = {"application/java-archive", "application/zip"}

# FUNCTIONS


def is_sha256(string):
    """Test a string is a valid sha256."""
    return SHA256_RE.match(string) is not None


def is_apk_file(apkfile):
    """Test a buffer is a valid APK/JAR file."""
    return magic.from_file(apkfile, mime=True) in APK_MAGICS


def is_apk_buffer(apkbuf):
    """Test a buffer is a valid APK/JAR file."""
    return magic.from_buffer(apkbuf, mime=True) in APK_MAGICS
