# -*- coding: utf-8 -*-

import pytest

from servalx import environ, virustotal


@pytest.fixture()
def api():
    return virustotal.VirusTotalAPI(environ.VIRUSTOTAL_APIKEY)


@pytest.fixture()
def apk():
    from .config import EXAMPLES
    import os

    return os.path.join(EXAMPLES, "a.apk")


# The following methods have been disabled
# due to an API error: InsufficientPrivileges

# def test_can_submit_file_scan(api, apk):
#     with open(apk) as f:
#         report = virustotal.file_scan(api, f)

#         assert frozenset(report.keys()) == virustotal.SCAN_RESPONSE_SET

# def test_can_submit_file_rescan_if_exist(api):
#     sig = '00000439a3ffa123c3f9bc45e5e821351b1a5c276871b36447ab80c74261f354'

#     report = virustotal.file_rescan(api, sig)
#     assert frozenset(report.keys()) == virustotal.RESCAN_RESPONSE_SET

# def test_cannot_submit_file_rescan_if_absent(api):
#     sig = '0000000000000000000000000000000000000000000000000000000000000000'

#     with pytest.raises(virustotal.ItemDoesNotExist) as invalid:
#         virustotal.file_rescan(api, sig)
#         assert sig in str(invalid)

# def test_can_submit_file_report_if_exist(api):
#     sig = '00000439a3ffa123c3f9bc45e5e821351b1a5c276871b36447ab80c74261f354'

#     report = virustotal.file_report(api, sig)
#     assert frozenset(report.keys()) == virustotal.REPORT_RESPONSE_SET

# def test_cannot_submit_file_report_if_absent(api):
#     sig = '0000000000000000000000000000000000000000000000000000000000000000'

#     with pytest.raises(virustotal.ItemDoesNotExist) as invalid:
#         virustotal.file_report(api, sig)
#         assert sig in str(invalid)
