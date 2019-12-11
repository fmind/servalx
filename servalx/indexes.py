# -*- coding: utf-8 -*-
"""Extract indexes from APK information.

DEPRECATED: replaced by the 'artifacts' module."""

import os

from servalx import manifest, package

identity = lambda x: x
lower = lambda x: x.lower()
upper = lambda x: x.upper()
lastof_pkg = lambda x: x.split(".")[-1]


def _setitem(doc, pre, key, on_key=identity):
    """Set an index key to True in a dictionnary."""
    if not key:
        return False

    doc[u"{}::{}".format(pre, on_key(key))] = True

    return True


def from_dex_debug(debug):
    """Extract information from a dex debug."""
    doc = dict()

    _setitem(doc, "dex::debug", debug)

    return doc


def from_dex_format(format):
    """Extract information from a dex format."""
    doc = dict()

    _setitem(doc, "dex::format", format, on_key=lower)

    return doc


def from_dex_header(header):
    """Extract information from a dex header."""
    doc = dict()

    _setitem(doc, "dex::magic", header.get("magic"))

    return doc


def from_dex_fields(fields):
    """Extract information from dex fields."""
    doc = dict()

    for infos in fields.values():
        pkg, class_ = package.split_class(infos.get("class"))

        _setitem(doc, "dex::package", pkg)
        _setitem(doc, "dex::class", class_)
        _setitem(doc, "dex::field", infos.get("name"))

    return doc


def from_dex_strings(strings):
    """Extract information from dex strings."""
    doc = dict()

    for string in strings.keys():
        _setitem(doc, "dex::string", string, on_key=lower)

    return doc


def from_dex_methods(methods):
    """Extract information from dex methods."""
    doc = dict()

    for infos in methods.values():
        pkg, class_ = package.split_class(infos.get("class"))

        _setitem(doc, "dex::package", pkg)
        _setitem(doc, "dex::class", class_)
        _setitem(doc, "dex::method", infos.get("name"))
        _setitem(doc, "dex::code", infos.get("sha256"), on_key=lower)

    return doc


def from_dex_classes(classes):
    """Extract information from dex classes."""
    doc = dict()

    for class_, infos in classes.items():
        pkg, name = package.split_class(class_)
        _setitem(doc, "dex::package", pkg)
        _setitem(doc, "dex::class", name)

        pkg, name = package.split_class(infos.get("super"))
        _setitem(doc, "dex::super-package", pkg)
        _setitem(doc, "dex::super-class", name)

    return doc


def from_dex_invokes(invokes):
    """Extract information from dex invokes."""
    doc = dict()

    for invoke in invokes.keys():
        pkg_class, method = package.split_invoke(invoke)

        # example: builting types [I->clone()...
        if pkg_class is None or method is None:
            continue

        method = method.split("(", 1)[0]
        _setitem(doc, "dex::invoke", u"{}->{}".format(pkg_class, method))

    return doc


def from_dex(dex):
    """Extract information from a dex document."""
    doc = dict()

    doc.update(from_dex_debug(dex["debug"]))
    doc.update(from_dex_format(dex["format"]))
    doc.update(from_dex_header(dex["header"]))
    doc.update(from_dex_fields(dex["fields"]))
    doc.update(from_dex_strings(dex["strings"]))
    doc.update(from_dex_methods(dex["methods"]))
    doc.update(from_dex_classes(dex["classes"]))
    doc.update(from_dex_invokes(dex["invokes"]))

    return doc


def from_manifest(manifest_doc):
    """Extract information from a manifest document."""
    # vars
    doc = dict()

    # REVIEW MANIFEST INFORMATION

    for e in manifest.flatten(manifest_doc):
        tag, attrs = e["tag"], e["attrs"]

        if tag == "manifest":
            _setitem(doc, "manifest::package", attrs.get("package"))
            _setitem(doc, "manifest::versioncode", attrs.get("versioncode"))
            _setitem(doc, "manifest::shareduserid", attrs.get("shareduserid"))
        elif tag == "activity":
            _setitem(doc, "manifest::activity", attrs.get("name"), on_key=lastof_pkg)
            _setitem(doc, "manifest::process", attrs.get("process"), on_key=lastof_pkg)
        elif tag == "service":
            _setitem(doc, "manifest::service", attrs.get("name"), on_key=lastof_pkg)
            _setitem(doc, "manifest::process", attrs.get("process"), on_key=lastof_pkg)
        elif tag == "receiver":
            _setitem(doc, "manifest::receiver", attrs.get("name"), on_key=lastof_pkg)
            _setitem(doc, "manifest::process", attrs.get("process"), on_key=lastof_pkg)
        elif tag == "provider":
            _setitem(doc, "manifest::provider", attrs.get("name"), on_key=lastof_pkg)
            _setitem(doc, "manifest::process", attrs.get("process"), on_key=lastof_pkg)
        elif tag == "action":
            _setitem(
                doc, "manifest::intent-filter", attrs.get("name"), on_key=lastof_pkg
            )
        elif tag == "category":
            _setitem(
                doc, "manifest::intent-category", attrs.get("name"), on_key=lastof_pkg
            )
        elif tag == "data":
            _setitem(doc, "manifest::data-scheme", attrs.get("scheme"))
            _setitem(doc, "manifest::data-host", attrs.get("host"))
            _setitem(doc, "manifest::data-port", attrs.get("port"))
            _setitem(doc, "manifest::data-path", attrs.get("path"))
            _setitem(doc, "manifest::data-pattern", attrs.get("pathpattern"))
            _setitem(doc, "manifest::data-prefix", attrs.get("pathprefix"))
            _setitem(doc, "manifest::data-mime", attrs.get("mimetype"))
        elif tag == "meta-data":
            _setitem(doc, "manifest::meta-key", attrs.get("name"))
            _setitem(doc, "manifest::meta-value", attrs.get("value"))
        elif tag == "activity-alias":
            _setitem(
                doc, "manifest::activity-alias", attrs.get("name"), on_key=lastof_pkg
            )
        elif tag == "permission":
            _setitem(doc, "manifest::permission", attrs.get("name"))
            _setitem(doc, "manifest::protection", attrs.get("protectionlevel"))
        elif tag == "instrumentation":
            _setitem(doc, "manifest::instrumentation", attrs.get("name"))
        elif tag == "uses-library":
            _setitem(doc, "manifest::uses-library", attrs.get("name"))
        elif tag == "uses-feature":
            _setitem(doc, "manifest::uses-feature", attrs.get("name"))
        elif tag == "uses-permission":
            _setitem(doc, "manifest::uses-permission", attrs.get("name"))
        elif tag == "permission-tree":
            _setitem(doc, "manifest::permission-tree", attrs.get("name"))
        elif tag == "permission-group":
            _setitem(doc, "manifest::permission-group", attrs.get("name"))
        elif tag == "application":
            _setitem(doc, "manifest::app::allow", attrs.get("package"))
            _setitem(
                doc,
                "manifest::app::allowtaskreparenting",
                attrs.get("allowtaskreparenting"),
            )
            _setitem(doc, "manifest::app::allowbackup", attrs.get("allowbackup"))
            _setitem(
                doc,
                "manifest::app::backupinforeground",
                attrs.get("backupinforeground"),
            )
            _setitem(doc, "manifest::app::debuggable", attrs.get("debuggable"))
            _setitem(
                doc, "manifest::app::directbootaware", attrs.get("directbootaware")
            )
            _setitem(doc, "manifest::app::enabled", attrs.get("enabled"))
            _setitem(
                doc, "manifest::app::extractnativelibs", attrs.get("extractnativelibs")
            )
            _setitem(doc, "manifest::app::fullbackuponly", attrs.get("fullbackuponly"))
            _setitem(doc, "manifest::app::hascode", attrs.get("hascode"))
            _setitem(
                doc,
                "manifest::app::hardwareaccelerated",
                attrs.get("hardwareaccelerated"),
            )
            _setitem(doc, "manifest::app::isgame", attrs.get("isgame"))
            _setitem(
                doc, "manifest::app::killafterrestore", attrs.get("killafterrestore")
            )
            _setitem(doc, "manifest::app::name", attrs.get("name"))
            _setitem(doc, "manifest::app::persistent", attrs.get("persistent"))
            _setitem(doc, "manifest::app::process", attrs.get("process"))
            _setitem(
                doc, "manifest::app::restoreanyversion", attrs.get("restoreanyversion")
            )
            _setitem(
                doc,
                "manifest::app::requiredaccounttype",
                attrs.get("requiredaccounttype"),
            )
            _setitem(
                doc,
                "manifest::app::resizeableactivity",
                attrs.get("resizeableactivity"),
            )
            _setitem(
                doc,
                "manifest::app::restrictedaccounttype",
                attrs.get("restrictedaccounttype"),
            )
            _setitem(doc, "manifest::app::supportsrtl", attrs.get("supportsrtl"))
            _setitem(doc, "manifest::app::testonly", attrs.get("testonly"))
            _setitem(
                doc,
                "manifest::app::usescleartexttraffic",
                attrs.get("usescleartexttraffic"),
            )
            _setitem(doc, "manifest::app::vmsafemode", attrs.get("vmsafemode"))

    return doc


def from_files(files):
    """Extract file names and signatures from files documents."""
    doc = dict()

    for path, infos in files.items():
        _setitem(doc, "file::name", os.path.basename(path), on_key=lower)
        _setitem(doc, "file::signature", infos.get("sha256"), on_key=lower)

    return doc


def from_resources(resources):
    """Extract strings from the resource documents."""
    doc = dict()

    for pkg, locales in resources.items():
        for local, res in locales.items():
            strings = res.get("string", [])

            for key, val in strings:
                _setitem(doc, "resource::string", val, on_key=lower)

    return doc


def from_certificate(certificate):
    """Extract information from a certificate document."""
    doc = dict()

    for key, val in certificate.items():
        _setitem(doc, u"certificate::{}".format(key), val, on_key=lower)

    return doc


def from_apkinfos(apkinfos):
    """Convert an apkinfos document to an index map."""
    doc = {"VERSION": 1, "sha256": apkinfos["sha256"].lower()}

    doc.update(from_dex(apkinfos["dex"]))
    doc.update(from_manifest(apkinfos["manifest"]))
    doc.update(from_files(apkinfos["fileinfos"]))
    doc.update(from_resources(apkinfos["resources"]))
    doc.update(from_certificate(apkinfos["certificate"]))

    return doc
