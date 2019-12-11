# -*- coding: utf-8 -*-
"""Manipulate and extract information from Android identifiers."""

import re

# CONSTANTS

CLASS_RE = re.compile(r"^\[?L(.+);$")
FIELD_RE = re.compile(r"^\[?L(.+?);->(.+)$")
METHOD_RE = re.compile(r"^\[?L(.+?);->(.+)$")
INVOKE_RE = re.compile(r"^\[?L(.+?);->(.+\(.*\).+)$")

SUPPORT_RE = re.compile(r"\[?\.support\.(v\d+\.)?")

# FUNCTIONS


def fold_support(package):
    """Remove support and version module from a package string."""
    if not package.startswith("android."):
        return package

    return re.sub(SUPPORT_RE, ".", package)


def split_class(ident):
    """"Split the package and the name of a class from an identifier."""
    matched = re.match(CLASS_RE, ident)

    if not matched:
        return None, None

    # separate package from class name
    splits = matched.group(1).rsplit("/", 1)

    if len(splits) == 2:
        return splits
    elif len(splits) == 1:
        # package is None
        return None, splits[0]
    else:
        return None, None


def split_field(ident):
    """"Split the package and the name of a field from an identifier."""
    matched = re.match(FIELD_RE, ident)

    return matched.groups() if matched else (None, None)


def split_method(ident):
    """"Split the package and the name of a method from an identifier."""
    matched = re.match(METHOD_RE, ident)

    return matched.groups() if matched else (None, None)


def split_invoke(ident):
    """"Split the package and signature of an invoke from an identifier."""
    matched = re.match(INVOKE_RE, ident)

    return matched.groups() if matched else (None, None)
