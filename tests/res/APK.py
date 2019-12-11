# -*- coding: utf-8 -*-

from datetime import datetime

from . import DVM

PACKAGE = "air.jp.co.studio.arcana.regwoosh"
DEX_DATE = datetime(2014, 5, 15, 19, 23, 12)
ID = "0000230ae0799eaa963f0ae5337a0e6e1ac32acf1fa4e3c5fa7783cbae2efe77"
NO = "0000000000000000000000000000000000000000000000000000000000000000"

DVMINFOS = DVM.DVMINFOS

CERTIFICATE = {
    "sha1": "81:46:2B:D5:79:84:4D:E0:77:6F:90:05:82:09:3B:E2:1A:76:C4:6E",
    "version": "3",
    "sha256": "37:FE:73:1F:31:95:EF:BA:E5:84:CD:F7:D2:AD:3A:AD:58:B5:6A:1D:9D:53:85:F3:91:10:F0:BC:73:D7:FB:C1",
    "valid_from": "Thu Apr 24 10:27:52 CEST 2014 until: Mon Apr 25 10:27:52 CEST 2039",
    "owner": 'CN="STUDIO Arcana Co., Ltd.", OU="STUDIO Arcana Co., Ltd.", O="STUDIO Arcana Co., Ltd.", C=JP',
    "serial_number": "35346161623162613a31343539376666373437383a2d38303030",
    "issuer": 'CN="STUDIO Arcana Co., Ltd.", OU="STUDIO Arcana Co., Ltd.", O="STUDIO Arcana Co., Ltd.", C=JP',
    "signature_algorithm_name": "SHA1withRSA",
    "subject_public_key_algorithm": "2048-bit RSA key",
    # 'md5':
    # 'FA:D2:63:1F:6B:EC:DD:F5:5B:92:BD:3E:94:1B:00:59',
}

FILES = {
    "resources.arsc": {
        "sha256": "735191e7635b28eabb961ab3e666ecbef562d6363a420dac835c3be730963657",
        "magic": "data",
        "filesize": 3012,
        "origname": "resources.arsc",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "res/drawable-ldpi/icon.png": {
        "sha256": "c30897a1755bcddbc9ce07c89ff136805c43680a24c29975fd3644a716e83868",
        "magic": "PNG image data, 36 x 36, 8-bit/color RGBA, non-interlaced",
        "filesize": 1645,
        "origname": "res/drawable-ldpi/icon.png",
        "datetime": (2014, 5, 15, 19, 23, 10),
    },
    "assets/Default.png": {
        "sha256": "1451806541d0959b0e6a550e9f95718937031ff710dd57b131474af9d9b8875b",
        "magic": "PNG image data, 340 x 480, 8-bit/color RGB, non-interlaced",
        "filesize": 68677,
        "origname": "assets/Default.png",
        "datetime": (2014, 3, 12, 15, 13, 28),
    },
    "META-INF/MANIFEST.MF": {
        "sha256": "df0ced7a918aa3649015a76e5b85756c1312b9efe0cb665ec4074799aebcb9e1",
        "magic": "ASCII text, with CRLF line terminators",
        "filesize": 1524,
        "origname": "META-INF/MANIFEST.MF",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "assets/sound/test02lowcut.mp3": {
        "sha256": "4a9cd203dde2813c5111c058c9e789d9c5be3d49cdd72ee0cb8cc361d9beef52",
        "magic": "Audio file with ID3 version 2.2.0",
        "filesize": 3377,
        "origname": "assets/sound/test02lowcut.mp3",
        "datetime": (2014, 4, 22, 16, 26, 18),
    },
    "lib/armeabi-v7a/libNativeABI.so": {
        "sha256": "0903dedd82f103a8396748634b2765962a938df93772713503d4b77182246d12",
        "magic": "ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV)",
        "filesize": 9560,
        "origname": "lib/armeabi-v7a/libNativeABI.so",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "res/raw/debuginfo": {
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "magic": "empty",
        "filesize": 0,
        "origname": "res/raw/debuginfo",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "res/drawable-mdpi/icon.png": {
        "sha256": "6e0d934f5d3e5f3da418ff2fa2573aab98ed175d88c4329c3d139c91a36b9cbf",
        "magic": "PNG image data, 48 x 48, 8-bit/color RGBA, non-interlaced",
        "filesize": 1986,
        "origname": "res/drawable-mdpi/icon.png",
        "datetime": (2014, 5, 15, 19, 23, 10),
    },
    "assets/RegWoosh.swf": {
        "sha256": "56b5cf0f71dcfef6c38cc18310f082af839aa3799a2dc3b051099c0d3cf95d4a",
        "magic": "Macromedia Flash data, version 17",
        "filesize": 374418,
        "origname": "assets/RegWoosh.swf",
        "datetime": (2014, 5, 15, 19, 23, 10),
    },
    "res/drawable/mp_warning_32x32_n.png": {
        "sha256": "93c948dade3ee6720ee848cbf551bd7c219c0178afe60df6d63a1f52ba9374c3",
        "magic": "PNG image data, 32 x 32, 8-bit gray+alpha, non-interlaced",
        "filesize": 991,
        "origname": "res/drawable/mp_warning_32x32_n.png",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "META-INF/CERT.RSA": {
        "sha256": "0fc4b18d5b5a482fabb7d9444b62e664d2431a1a333b415d3f7ef307cd1117f9",
        "magic": "data",
        "filesize": 1418,
        "origname": "META-INF/CERT.RSA",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "assets/icons/android/Icon-48.png": {
        "sha256": "6e0d934f5d3e5f3da418ff2fa2573aab98ed175d88c4329c3d139c91a36b9cbf",
        "magic": "PNG image data, 48 x 48, 8-bit/color RGBA, non-interlaced",
        "filesize": 1986,
        "origname": "assets/icons/android/Icon-48.png",
        "datetime": (2014, 3, 18, 17, 42, 58),
    },
    "res/drawable-hdpi/icon.png": {
        "sha256": "3fbd3ae53e22bd3f7c6ae6dffb253bd83328efed6e4a2f4f11da1d23ea688629",
        "magic": "PNG image data, 72 x 72, 8-bit/color RGBA, non-interlaced",
        "filesize": 2596,
        "origname": "res/drawable-hdpi/icon.png",
        "datetime": (2014, 5, 15, 19, 23, 10),
    },
    "assets/Default-568h@2x.png": {
        "sha256": "01460e0cb9a3f7387169bd6dfcc6776851f6e27c7b03c1eea94f8583881a4a8d",
        "magic": "PNG image data, 640 x 1136, 8-bit/color RGB, non-interlaced",
        "filesize": 124057,
        "origname": "assets/Default-568h@2x.png",
        "datetime": (2014, 3, 12, 15, 10, 44),
    },
    "assets/Default@2x.png": {
        "sha256": "89c6c4cee632998a1b2dd52bc200d00c6dd3f512234a0de0c0bb4ae8f84ddd1c",
        "magic": "PNG image data, 640 x 960, 8-bit/color RGB, non-interlaced",
        "filesize": 127001,
        "origname": "assets/Default@2x.png",
        "datetime": (2014, 3, 12, 15, 14, 46),
    },
    "res/raw/rgba8888": {
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "magic": "empty",
        "filesize": 0,
        "origname": "res/raw/rgba8888",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "classes.dex": {
        "sha256": "b4f6d5f6e936aef0fbde5478ad8cd2d40808f3cea2ab8e209cc5a3649614076d",
        "magic": "Dalvik dex file version 035",
        "filesize": 26236,
        "origname": "classes.dex",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "assets/icons/android/Icon-72.png": {
        "sha256": "3fbd3ae53e22bd3f7c6ae6dffb253bd83328efed6e4a2f4f11da1d23ea688629",
        "magic": "PNG image data, 72 x 72, 8-bit/color RGBA, non-interlaced",
        "filesize": 2596,
        "origname": "assets/icons/android/Icon-72.png",
        "datetime": (2014, 3, 18, 17, 42, 40),
    },
    "AndroidManifest.xml": {
        "sha256": "016819895f6b77d247e7d99f7373e12b5228cf7d413dab1fb867d88634f56541",
        "magic": "Android binary XML",
        "filesize": 3376,
        "origname": "AndroidManifest.xml",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "assets/icons/android/Icon-36.png": {
        "sha256": "c30897a1755bcddbc9ce07c89ff136805c43680a24c29975fd3644a716e83868",
        "magic": "PNG image data, 36 x 36, 8-bit/color RGBA, non-interlaced",
        "filesize": 1645,
        "origname": "assets/icons/android/Icon-36.png",
        "datetime": (2014, 3, 18, 17, 43, 16),
    },
    "META-INF/CERT.SF": {
        "sha256": "a62230fabbbfe589737ab9059f82b96ec19fbb1d426fb7bb3c7d64742a7a0555",
        "magic": "ASCII text, with CRLF line terminators",
        "filesize": 1577,
        "origname": "META-INF/CERT.SF",
        "datetime": (2014, 5, 15, 19, 23, 12),
    },
    "assets/META-INF/AIR/application.xml": {
        "sha256": "b369a4aee8471433990ca2ed4b284fa86fee56810ab89146e2f550912e932a9f",
        "magic": "XML 1.0 document, ASCII text, with CRLF line terminators",
        "filesize": 2146,
        "origname": "assets/META-INF/AIR/application.xml",
        "datetime": (2014, 5, 15, 19, 23, 10),
    },
}

NATIVES = {
    "lib/armeabi-v7a/libNativeABI.so": {
        "strings": {
            "__gnu_Unwind_Resume": 1,
            "__gnu_Unwind_Save_VFP": 1,
            ".rel.plt": 1,
            "__gnu_Unwind_Save_VFP_D": 1,
            "_edata": 1,
            ".dynsym": 1,
            "__gnu_Unwind_RaiseException": 1,
            "_Unwind_DeleteException": 1,
            "getNativeABI": 1,
            "__cxa_begin_cleanup": 1,
            "__gnu_Unwind_Save_VFP_D_16_to_31": 1,
            "aeabi": 1,
            "__gnu_Unwind_Restore_VFP_D_16_to_31": 1,
            "___Unwind_Resume": 1,
            "_Unwind_GetLanguageSpecificData": 1,
            "_stack": 1,
            "__bss_start__": 1,
            ".comment": 1,
            "__cxa_type_match": 1,
            "__gnu_Unwind_Restore_WMMXD": 1,
            "__gnu_Unwind_Restore_WMMXC": 1,
            ".dynstr": 1,
            "_Unwind_VRS_Set": 1,
            "memcpy": 1,
            "__gnu_Unwind_Restore_VFP_D": 1,
            "__gnu_Unwind_Save_WMMXD": 1,
            ".data": 1,
            "__gnu_Unwind_Find_exidx": 1,
            "__gnu_Unwind_Save_WMMXC": 1,
            ".ARM.exidx": 1,
            ".dynamic": 1,
            "__end__": 1,
            ".ARM.attributes": 1,
            "__aeabi_unwind_cpp_pr1": 1,
            "__aeabi_unwind_cpp_pr0": 1,
            "__aeabi_unwind_cpp_pr2": 1,
            "___Unwind_RaiseException": 1,
            "libc.so": 1,
            "abort": 1,
            "__exidx_end": 1,
            "_Unwind_GetCFA": 1,
            "___Unwind_Resume_or_Rethrow": 1,
            ".text": 1,
            "libdl.so": 1,
            "_Unwind_VRS_Get": 1,
            "libARMv7AMarker.so": 1,
            "__gnu_Unwind_Restore_VFP": 1,
            "__gnu_unwind_execute": 1,
            "__bss_end__": 1,
            "_Unwind_GetRegionStart": 1,
            ".shstrtab": 1,
            "__exidx_start": 1,
            "__gnu_Unwind_Backtrace": 1,
            "armv7-a": 1,
            "_Unwind_GetTextRelBase": 1,
            ".rel.dyn": 1,
            "___Unwind_Backtrace": 1,
            ".got": 1,
            "_Unwind_Complete": 1,
            "_Unwind_GetDataRelBase": 1,
            "_Unwind_VRS_Pop": 1,
            ".hash": 1,
            "__gnu_Unwind_ForcedUnwind": 1,
            "__restore_core_regs": 1,
            ".ARM.extab": 1,
            "___Unwind_ForcedUnwind": 1,
            "__gnu_Unwind_Resume_or_Rethrow": 1,
            "GCC: (GNU) 4.4.0": 3,
            "__cxa_call_unexpected": 1,
            "__gnu_unwind_frame": 1,
            "__bss_start": 1,
            "__data_start": 1,
        }
    }
}

RESOURCES = {
    u"air.jp.co.studio.arcana.RegWoosh": {
        "DEFAULT": {
            u"raw": [],
            u"drawable": [],
            u"style": [],
            "public": [
                (u"drawable", u"icon", 2130837504),
                (u"drawable", u"mp_warning_32x32_n", 2130837505),
                (u"drawable", u"icon", 2130837504),
                (u"drawable", u"icon", 2130837504),
                (u"drawable", u"icon", 2130837504),
                (u"raw", u"debugger", 2130903040),
                (u"raw", u"debuginfo", 2130903041),
                (u"raw", u"rgba8888", 2130903042),
                (u"string", u"app_name", 2130968576),
                (u"string", u"app_version", 2130968577),
                (u"string", u"button_install", 2130968578),
                (u"string", u"button_exit", 2130968579),
                (u"string", u"title_adobe_air", 2130968580),
                (u"string", u"text_runtime_required", 2130968581),
                (u"string", u"text_install_runtime", 2130968582),
                (u"string", u"text_runtime_on_external_storage", 2130968583),
                (u"style", u"Theme.NoShadow", 2131034112),
            ],
            u"string": [
                [u"app_name", u"RegWoosh"],
                [u"app_version", u"APP_VERSION"],
                [u"button_install", u"Install"],
                [u"button_exit", u"Exit"],
                [u"title_adobe_air", u"Adobe AIR"],
                [u"text_runtime_required", u"This application requires Adobe AIR.\n\n"],
                [
                    u"text_install_runtime",
                    u"To continue, install Adobe AIR on this device.",
                ],
                [
                    u"text_runtime_on_external_storage",
                    u"To continue, either install Adobe AIR on this device or exit this application and mount the SD card containing Adobe AIR before re-launching.",
                ],
            ],
        },
        "ja": {
            "public": [
                (u"string", u"app_name", 2130968576),
                (u"string", u"app_version", 2130968577),
                (u"string", u"button_install", 2130968578),
                (u"string", u"button_exit", 2130968579),
                (u"string", u"title_adobe_air", 2130968580),
                (u"string", u"text_runtime_required", 2130968581),
                (u"string", u"text_install_runtime", 2130968582),
                (u"string", u"text_runtime_on_external_storage", 2130968583),
            ],
            u"string": [
                [u"app_name", u"RegWoosh"],
                [u"app_version", u"APP_VERSION"],
                [u"button_install", u""],
                [u"button_exit", u""],
                [u"title_adobe_air", u"Adobe AIR"],
                [u"text_runtime_required", u"Adobe AIR \n\n"],
                [u"text_install_runtime", u" Adobe AIR "],
                [u"text_runtime_on_external_storage", u" Adobe AIR  Adobe AIR  SD "],
            ],
        },
    }
}

MANIFEST = {
    "text": "",
    "tag": "manifest",
    "attrs": {
        "versioncode": "1000001",
        "versionname": "1.0.1",
        "package": "air.jp.co.studio.arcana.regwoosh",
    },
    "_children": [
        {
            "text": "",
            "tag": "application",
            "attrs": {
                "hardwareaccelerated": "false",
                "icon": "@7f020000",
                "label": "@7f040000",
            },
            "_children": [
                {
                    "text": "",
                    "tag": "activity",
                    "attrs": {
                        "windowsoftinputmode": "0x00000012",
                        "name": ".appentry",
                        "screenorientation": "2",
                        "launchmode": "2",
                        "label": "@7f040000",
                        "theme": "@7f050000",
                        "configchanges": "0x000004a0",
                    },
                    "_children": [
                        {
                            "text": "",
                            "tag": "intent-filter",
                            "attrs": {},
                            "_children": [
                                {
                                    "text": "",
                                    "tag": "action",
                                    "attrs": {"name": "android.intent.action.main"},
                                    "_children": [],
                                },
                                {
                                    "text": "",
                                    "tag": "category",
                                    "attrs": {
                                        "name": "android.intent.category.launcher"
                                    },
                                    "_children": [],
                                },
                            ],
                        },
                        {
                            "text": "",
                            "tag": "meta-data",
                            "attrs": {"name": "namespaceversion", "value": "3.400000"},
                            "_children": [],
                        },
                        {
                            "text": "",
                            "tag": "meta-data",
                            "attrs": {"name": "aspectratio", "value": "portrait"},
                            "_children": [],
                        },
                        {
                            "text": "",
                            "tag": "meta-data",
                            "attrs": {"name": "autoorients", "value": "false"},
                            "_children": [],
                        },
                        {
                            "text": "",
                            "tag": "meta-data",
                            "attrs": {"name": "fullscreen", "value": "false"},
                            "_children": [],
                        },
                        {
                            "text": "",
                            "tag": "meta-data",
                            "attrs": {
                                "name": "uniqueappversionid",
                                "value": "9132dfcd-4c1b-45dc-81a7-d1181f81e14b",
                            },
                            "_children": [],
                        },
                        {
                            "text": "",
                            "tag": "meta-data",
                            "attrs": {
                                "name": "initialcontent",
                                "value": "regwoosh.swf",
                            },
                            "_children": [],
                        },
                    ],
                }
            ],
        },
        {
            "text": "",
            "tag": "uses-sdk",
            "attrs": {"minsdkversion": "8", "targetsdkversion": "14"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "uses-permission",
            "attrs": {"name": "android.permission.internet"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "uses-permission",
            "attrs": {"name": "android.permission.write_external_storage"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "uses-permission",
            "attrs": {"name": "android.permission.read_phone_state"},
            "_children": [],
        },
    ],
}

PERMISSIONS = {
    "internet": "safe",
    "read_phone_state": "safe",
    "write_external_storage": "safe",
}

APKINFOS = {
    "sha256": ID,
    "dex": DVMINFOS,
    # 'natives': NATIVES,
    "manifest": MANIFEST,
    "fileinfos": FILES,
    "resources": RESOURCES,
    "certificate": CERTIFICATE,
    "VERSION": 2,
}
