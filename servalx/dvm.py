# -*- coding: utf-8 -*-
"""Object representing an Android (O)DEX file (DVM)."""

from androguard.core.androconf import is_android_raw
from androguard.core.bytecodes import dvm as AndroDVM

# ERRORS


class DVMError(Exception):
    pass


class InvalidDVM(DVMError):
    pass


# CLASSES


class DVM(object):
    def __init__(self, dex):
        """Create an APK object from a dex object."""
        filetype = is_android_raw(dex)

        if filetype not in ["DEX", "ODEX"]:
            raise InvalidDVM("Not a valid filetype: {0}".format(filetype))

        self.filetype = filetype
        self._dvm = AndroDVM.DalvikVMFormat(dex)


def is_debug(dvm):
    """Check a DVM has a debug flag set."""
    return isinstance(dvm._dvm.debug, AndroDVM.DebugInfoItem)


def xformat(dvm):
    """Return the format of a DVM object."""
    return dvm._dvm.get_format_type()
