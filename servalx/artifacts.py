# -*- coding: utf-8 -*-
"""Extract artifact from APK information."""

import os
from collections import defaultdict

from servalx import manifest, package

_intnone = lambda x: int(x) if x is not None else None
_lownone = lambda x: x.lower() if x is not None else None


def from_dex(doc):
    """Index artifacts from dex."""
    entries = defaultdict(set)

    entries["source.debug"].add(doc.get("debug", False))
    entries["source.format"].add(_lownone(doc.get("format")))

    for x in doc.get("strings", []):
        if x is not None and len(x) <= 1000:
            entries["source.string"].add(x.lower())

    for x in doc.get("invokes", []):
        entries["source.invoke"].add(_lownone(x))

    for ID, field in doc.get("fields", {}).items():
        entries["source.field.path"].add(_lownone(ID))
        entries["source.field.name"].add(_lownone(field.get("name")))

    for ID, class_ in doc.get("classes", {}).items():
        pack, name = package.split_class(ID)

        entries["source.class.path"].add(_lownone(ID))
        entries["source.class.name"].add(_lownone(name))
        entries["source.class.package"].add(_lownone(pack))

        for inter_ in class_.get("inter", []):
            entries["source.class.inter"].add(_lownone(inter_))

        for super_ in class_.get("super", []):
            entries["source.class.super"].add(_lownone(super_))

    for ID, method in doc.get("methods", {}).items():
        entries["source.method.path"].add(_lownone(ID))
        entries["source.method.name"].add(_lownone(method.get("name")))
        entries["source.method.code"].add(_lownone(method.get("sha256")))

    return dict(entries)


def from_manifest(doc):
    """Index artifacts from manifest."""
    entries = defaultdict(set)

    for el in manifest.flatten(doc):
        tag, text, attrs = el["tag"], el["text"], el["attrs"]

        tag, text, attrs = (
            tag.lower(),
            text.lower(),
            {k.lower(): v.lower() for k, v in attrs.items()},
        )

        if tag == "action":
            entries["manifest.action"].add(attrs.get("name"))
        elif tag == "activity":
            entries["manifest.activity"].add(attrs.get("name"))
        elif tag == "service":
            entries["manifest.service"].add(attrs.get("name"))
        elif tag == "provider":
            entries["manifest.provider"].add(attrs.get("name"))
        elif tag == "receiver":
            entries["manifest.receiver"].add(attrs.get("name"))
        elif tag == "category":
            entries["manifest.category"].add(attrs.get("name"))
        elif tag == "manifest":
            entries["manifest.vername"].add(attrs.get("versionname"))
            entries["manifest.vercode"].add(_intnone(attrs.get("versioncode")))
        elif tag == "meta-data":
            entries["manifest.metakey"].add(attrs.get("name"))
            entries["manifest.metaval"].add(attrs.get("value"))
        elif tag == "instrumentation":
            entries["manifest.instrumentation"].add(attrs.get("name"))
        elif tag == "uses-sdk":
            entries["manifest.minsdk"].add(_intnone(attrs.get("minsdkversion")))
            entries["manifest.maxsdk"].add(_intnone(attrs.get("maxsdkversion")))
            entries["manifest.tarsdk"].add(_intnone(attrs.get("targetsdkversion")))
        elif tag == "uses-library":
            entries["manifest.library"].add(attrs.get("name"))
        elif tag == "uses-feature":
            entries["manifest.feature"].add(attrs.get("name"))
        elif (
            tag == "permission"
            or tag == "uses-permission"
            or tag == "uses-permission-sdk-23"
        ):
            entries["manifest.permission"].add(attrs.get("name"))
        elif tag == "permission-group":
            entries["manifest.permgroup"].add(attrs.get("name"))
        elif tag == "permission-tree":
            entries["manifest.permtree"].add(attrs.get("name"))

    return dict(entries)


def from_fileinfos(doc):
    """Index artifacts from fileinfos."""
    entries = defaultdict(set)

    for path, info in doc.items():
        name = os.path.basename(path) if path is not None else None

        entries["file.name"].add(_lownone(name))
        entries["file.path"].add(_lownone(path))
        entries["file.sha256"].add(_lownone(info.get("sha256")))

    return dict(entries)


def from_resources(doc):
    """Index artifacts from resources."""
    entries = defaultdict(set)

    for pkg, langs in doc.items():
        entries["resource.package"].add(_lownone(pkg))

        for lang, cats in langs.items():
            entries["resource.language"].add(_lownone(lang))

            for cat, key, val in cats.get("public", []):
                entries["resource.entry"].add(_lownone(key))

            for key, val in cats.get("string", []):
                entries["resource.entry"].add(_lownone(key))
                entries["resource.string"].add(_lownone(val))

    return dict(entries)


def from_certificate(doc):
    """Index artifacts from certificate."""
    entries = defaultdict(set)

    entries["certificate.owner"].add(_lownone(doc.get("owner")))
    entries["certificate.issuer"].add(_lownone(doc.get("issuer")))
    entries["certificate.signature"].add(_lownone(doc.get("sha256")))

    return dict(entries)


def from_metas(doc):
    """Index artifacts from metas."""
    entries = defaultdict(set)

    entries["meta.md5"].add(_lownone(doc.get("md5")))
    entries["meta.sha1"].add(_lownone(doc.get("sha1")))
    entries["meta.sha256"].add(_lownone(doc.get("sha256")))
    entries["meta.vt.date"].add(_lownone(doc.get("vt", {}).get("date")))
    entries["meta.vt.score"].add(_intnone(doc.get("vt", {}).get("score")))
    entries["meta.apk.size"].add(_intnone(doc.get("apk", {}).get("size")))
    entries["meta.dex.date"].add(_lownone(doc.get("dex", {}).get("date")))
    entries["meta.dex.size"].add(_intnone(doc.get("dex", {}).get("size")))
    entries["meta.pkg.name"].add(_lownone(doc.get("pkg", {}).get("name")))
    entries["meta.pkg.code"].add(_intnone(doc.get("pkg", {}).get("code")))
    entries["meta.market"].update(map(_lownone, doc.get("markets", "").split("|")))

    return dict(entries)


def from_labels(doc):
    """Index artifacts from labels."""
    entries = defaultdict(set)

    entries["label.type"].add(_lownone(doc.get("type", {}).get("proposed")))
    entries["label.family"].add(_lownone(doc.get("family", {}).get("proposed")))

    return dict(entries)


def from_apkinfos(doc):
    """Index artifacts from apkinfos"""
    entries = dict()
    entries.update(from_dex(doc["dex"]))
    entries.update(from_manifest(doc["manifest"]))
    entries.update(from_fileinfos(doc["fileinfos"]))
    entries.update(from_resources(doc["resources"]))
    entries.update(from_certificate(doc["certificate"]))

    return entries
