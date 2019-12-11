# -*- coding: utf-8 -*-

from .config import EXAMPLES
from servalx import validators
import os


def test_can_validate_sha256():
    valid = "0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa670"

    too_short = "0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa67"
    too_long = "0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa6700"

    bad_char = "0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa670x"
    bad_punct = "0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa670!"
    bad_blank = "0000003b455a6c7af837ef90f2eaffd856e3b5cf49f5e27191430328de2fa670 "

    assert validators.is_sha256(valid)
    assert validators.is_sha256(valid.upper())

    assert not validators.is_sha256(too_long)
    assert not validators.is_sha256(too_short)

    assert not validators.is_sha256(bad_char)
    assert not validators.is_sha256(bad_punct)
    assert not validators.is_sha256(bad_blank)


def test_can_validate_apk_buffer():
    assert validators.is_apk_file(os.path.join(EXAMPLES, "a.apk"))

    assert not validators.is_apk_file(os.path.join(EXAMPLES, "a.so"))
    assert not validators.is_apk_file(os.path.join(EXAMPLES, "a.rsa"))
    assert not validators.is_apk_file(os.path.join(EXAMPLES, "a.arm"))
