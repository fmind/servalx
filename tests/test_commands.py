# -*- coding: utf-8 -*-

import pytest
from servalx import commands


@pytest.fixture()
def armfile():
    from .config import EXAMPLES
    import os

    return os.path.join(EXAMPLES, "a.arm")


@pytest.fixture()
def natfile():
    from .config import EXAMPLES
    import os

    return os.path.join(EXAMPLES, "a.so")


@pytest.fixture()
def certfile():
    from .config import EXAMPLES
    import os

    return os.path.join(EXAMPLES, "a.rsa")


def test_can_complete_commands():
    cmds = commands.complete()

    # rough estimation
    assert len(cmds) > 1000
    assert all(isinstance(x, str) for x in cmds)


# def test_can_extract_strings_from_arm_files(armfile):
#     with open(armfile, 'r') as f:
#         strings = commands.arm_strings(f)

#     assert len(strings) == 72
#     assert all(isinstance(s, str) for s in strings)


def test_can_extract_strings_from_any_files(natfile):
    with open(natfile, "r") as f:
        strings = commands.strings(f)

    assert len(strings) == 4569
    assert all(isinstance(s, str) for s in strings)


def test_can_extract_x509_from_cert_file(certfile):
    with open(certfile, "r") as f:
        x509 = commands.keytool(f)

    assert x509 == {
        "version": "3",
        "signature_algorithm_name": "SHA1withRSA",
        "subject_public_key_algorithm": "2048-bit RSA key",
        "serial_number": "35346161623162613a31343539376666373437383a2d38303030",
        "sha1": "81:46:2B:D5:79:84:4D:E0:77:6F:90:05:82:09:3B:E2:1A:76:C4:6E",
        "sha256": "37:FE:73:1F:31:95:EF:BA:E5:84:CD:F7:D2:AD:3A:AD:58:B5:6A:1D:9D:53:85:F3:91:10:F0:BC:73:D7:FB:C1",
        "valid_from": "Thu Apr 24 10:27:52 CEST 2014 until: Mon Apr 25 10:27:52 CEST 2039",
        "owner": 'CN="STUDIO Arcana Co., Ltd.", OU="STUDIO Arcana Co., Ltd.", O="STUDIO Arcana Co., Ltd.", C=JP',
        "issuer": 'CN="STUDIO Arcana Co., Ltd.", OU="STUDIO Arcana Co., Ltd.", O="STUDIO Arcana Co., Ltd.", C=JP',
    }
