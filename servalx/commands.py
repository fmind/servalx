# -*- coding: utf-8 -*-
"""Interaction with operating system commands."""

import os
import re
import subprocess as Proc
from collections import Counter

from memoize import memoize

# ERRORS


class CommandError(Exception):
    pass


class KeytoolError(CommandError):
    pass


class StringsError(CommandError):
    pass


class ArmStringsError(CommandError):
    pass


# FUNCTIONS


@memoize
def complete():
    """List all UNIX commands under PATH."""
    paths = [p for p in os.environ["PATH"].split(":") if os.path.exists(p)]
    commands = {c for p in paths for c in os.listdir(p)}

    return commands


# def arm_strings(armfile):
#     """Extract strings from a native arm file."""
#     cmd = ["arm-linux-gnu-strings"]
#     proc = Proc.Popen(cmd, stdin=Proc.PIPE, stdout=Proc.PIPE)
#     out, err = proc.communicate(input=armfile.read())

#     if err is not None:
#         raise ArmStringsError(err)

#     return dict(Counter(out.splitlines()))


def strings(nativefile):
    """Extract strings from any native file (less precise)."""
    cmd = ["strings"]
    proc = Proc.Popen(cmd, stdin=Proc.PIPE, stdout=Proc.PIPE)
    out, err = proc.communicate(input=nativefile.read())

    if err is not None:
        raise StringsError(err)

    return dict(Counter(out.splitlines()))


def keytool(certfile, action="-printcert"):
    """Extract x509 information from a certificate file."""
    cmd = ["keytool", action]
    proc = Proc.Popen(cmd, stdin=Proc.PIPE, stdout=Proc.PIPE)
    out, err = proc.communicate(input=certfile.read())

    if err is not None:
        raise KeytoolError(err)

    x509 = dict()

    # minimalist parser for X509
    for line in out.splitlines():
        # ignore extensions
        if not line:
            break

        # only consider the first key
        key, val = line.split(":", 1)

        if key and val:
            key = key.strip().lower()
            key = re.sub(r"\s+", "_", key)
            x509[key] = val.strip()

    return x509
