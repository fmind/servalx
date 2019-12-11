# -*- coding: utf-8 -*-
"""Extract information from Android applications."""

import base64
import hashlib
from collections import Counter
from datetime import datetime

from androguard.core.bytecodes import dvm as AndroDVM

import servalx.apk as Apk
import servalx.dvm as Dvm
from servalx import android, commands, functions
from servalx import manifest as Manifest
from servalx import resources as Resources

CERT_DATE_FORMAT = "%a %b %d %H:%M:%S %Z %Y"


def debug(apk):
    """Extract the debug flag from an APK object."""
    return Dvm.is_debug(apk.dvm)


def xformat(apk):
    """Extract format information from an APK object."""
    return Dvm.xformat(apk.dvm)


def header(apk):
    """Extract header information from an APK object."""
    header = apk.dvm._dvm.header

    return {
        "magic": header.magic,
        "checksum": header.checksum,
        "file_size": header.file_size,
        "signature": base64.b64encode(header.signature),
    }


def fields(apk):
    """Extract fields information from an APK object."""

    def make_id(f):
        return "{0}->{1}".format(f.class_name, f.name)

    def from_field(f):
        """Extract a field signature from an EncodedField object."""
        init_value = f.init_value.get_value() if f.init_value else None

        if isinstance(init_value, str):
            init_value = unicode(init_value, errors="replace")

        return {
            "name": f.name,
            "type": f.proto,
            "init": init_value,
            "class": f.class_name,
            "flags": f.access_flags,
        }

    # fields from classes contain more info than dvm.fields
    res = [f for cls in apk.dvm._dvm.classes.class_def for f in cls.get_fields()]

    return {make_id(f): from_field(f) for f in res}


def methods(apk, with_code=False):
    """Extract methods information from an APK object."""

    def make_id(m):
        return "{0}->{1}".format(m.class_name, m.name)

    def from_method(m):
        """Extract a method signature from an EncodedMethod object."""

        def ins_to_str(ins):
            """Convert an instruction to a string."""
            return "{0} {1}".format(ins.get_name(), ins.get_output())

        info = m.get_information()
        instrucs = list(m.get_instructions())
        instring = "\n".join(ins_to_str(ins) for ins in instrucs)

        doc = {
            "name": m.name,
            "class": m.class_name,
            "flags": m.access_flags,
            "return": info.get("return"),
            "nb_instructions": len(instrucs),
            "sha256": hashlib.sha256(instring).hexdigest(),
            "params": [t for _, t in info.get("params", [])],
        }

        if with_code:
            doc["code"] = instring

        return doc

    # methods from classes contain more info than dvm.methods
    res = [m for cls in apk.dvm._dvm.classes.class_def for m in cls.get_methods()]

    return {make_id(m): from_method(m) for m in res}


def codes(apk):
    """Extract code information from an APK object."""
    res = methods(apk, with_code=True)

    return {
        m["sha256"]: {"code": m["code"], "params": m["params"], "return": m["return"]}
        for m in res.values()
    }


def invokes(apk):
    """Extract invokes information from an APK object."""
    res = list()

    # many nested levels ...
    for code in apk.dvm._dvm.codes.code:
        for ins in code.code.get_instructions():
            try:
                if ins.get_kind() == AndroDVM.KIND_METH:
                    res.append(ins.get_translated_kind())
            except Exception:
                pass

    return dict(Counter(res))


def classes(apk):
    """Extract classes information from an APK object."""

    def make_id(c):
        return c.name

    def from_class(c):
        """Extract a class signature from a ClassDefItem object."""
        return {"super": c.sname, "inter": c.interfaces, "flags": c.access_flags}

    # class list is contained in class_def
    res = apk.dvm._dvm.classes.class_def

    return {make_id(c): from_class(c) for c in res}


def strings(apk):
    """Extract strings information from an APK object."""
    res = (s.data for s in apk.dvm._dvm.strings)

    return dict(Counter(res))


def dvm(apk):
    """Extract all DVM information from an APK object."""

    return {
        "debug": debug(apk),
        "header": header(apk),
        "format": xformat(apk),
        "fields": fields(apk),
        "methods": methods(apk),
        "classes": classes(apk),
        "invokes": invokes(apk),
        "strings": strings(apk),
    }


def files(apk):
    """Extract information from files."""

    def make_id(apkfile):
        file, info, magic = apkfile

        return info.filename

    def from_apkfile(apkfile):
        file, info, magic = apkfile
        buffer = file.read()

        return {
            "magic": magic,
            "datetime": info.date_time,
            "filesize": info.file_size,
            "origname": info.orig_filename,
            "sha256": functions.compute_sha256(buffer),
        }

    # use generator comprehension to work
    res = (f for f in Apk.find_files(apk, with_magic=True))

    return {make_id(f): from_apkfile(f) for f in res}


def files_with_datetime(files):
    """Convert datetime arrays to strings."""

    def to_string(array):
        try:
            return str(datetime(*array))
        except ValueError:
            return ""

    newfiles = {}

    for file, info in files.items():
        info = info.copy()  # prevent mutation
        info["datetime"] = to_string(info["datetime"])

        newfiles[file] = info

    return newfiles


# def natives(apk):
#     """Extract information from native files."""

#     def make_id(apkfile):
#         file, info, magic = apkfile

#         return info.filename

#     def from_apkfile(apkfile):
#         file, info, magic = apkfile

#         if 'arm' in magic.lower():
#             return {'strings': commands.arm_strings(file)}
#         else:
#             return {'strings': commands.strings(file)}

#     # use generator comprehension to work
#     res = (f for f in Apk.find_natives(apk))

#     return {make_id(f): from_apkfile(f) for f in res}


def resources(apk):
    """Extract information from the resources"""
    resfile = Apk.find_resources(apk)

    return Resources.isomorph(resfile)


def manifest(apk):
    """Extract information from the AndroidManifest file."""
    manifestfile, _ = Apk.find_manifest(apk)

    return Manifest.isomorph(manifestfile)


def certificate(apk):
    """Extract information from the developer certificate."""
    certfile, _ = Apk.find_certificate(apk)

    return commands.keytool(certfile)


def certificate_with_daterange(cert):
    """Convert validity date to a proper range."""
    if "valid_from" not in cert:
        return cert

    date = cert["valid_from"]

    if " until: " not in date:
        return cert

    newcert = cert.copy()

    try:
        dfr, dto = date.split(" until: ")
        newcert["valid_to"] = str(datetime.strptime(dto, CERT_DATE_FORMAT))
        newcert["valid_from"] = str(datetime.strptime(dfr, CERT_DATE_FORMAT))

        return newcert
    except ValueError:
        return cert


def permissions(apk):
    """Extract permissions requiered by the application."""

    def _iter(elem, result):
        searched = ["permission", "uses-permission"]

        for child in elem["_children"]:
            if child["tag"] in searched:
                for key in child["attrs"]:
                    if key == "name":
                        name = child["attrs"][key].split(".")[-1]
                        if name.upper() in android.PERMISSIONS:
                            result[name] = "safe"
                        elif name.upper() in android.DANGEROUS:
                            result[name] = "unsafe"
                        else:
                            result[name] = "unidentified"
            _iter(child, result)
        return result

    return _iter(manifest(apk), {})


def apk(apk):
    """Extract all information from an APK object with indices."""

    return {
        "VERSION": 2,
        "dex": dvm(apk),
        "sha256": Apk.compute_sha256(apk),
        "fileinfos": files(apk),
        "resources": resources(apk),
        # 'natives': natives(apk), # too verbose
        "manifest": manifest(apk),
        "certificate": certificate(apk),
    }
