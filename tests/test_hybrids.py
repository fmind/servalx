# -*- coding: utf-8 -*-

from servalx import hybrids

from .res import APK, HYBRIDS

OWN_PACKAGE = "Lcn/zhui/client553863"

ANDROID_NOT_WEBVIEW_CLASS = "Landroid/support/v7/internal/view/menu/MenuView;"
HYBRID_WEBVIEW_CLASS = "Lorg/apache/cordova/CordovaWebView$2;"
HYBRID_NOT_WEBVIEW_CLASS = "Lorg/apache/cordova/CordovaChromeClient$7;"
OWN_PACKAGE_CLASS = (
    "Lcn/zhui/client553863/modulepage/ModulePageLayout$WeiboWallAdapter$3;"
)
OTHER_CLASS = (
    "Lorg/apache/commons/codec/language/DoubleMetaphone$DoubleMetaphoneResult;"
)


def test_function_test_package_in_set():
    assert not (
        hybrids.test_class_in_set(
            ANDROID_NOT_WEBVIEW_CLASS, hybrids.PACKAGES_KNOWN_AS_HYBRID
        )
    )
    assert hybrids.test_class_in_set(
        HYBRID_NOT_WEBVIEW_CLASS, hybrids.PACKAGES_KNOWN_AS_HYBRID
    )


def test_function_test_package_is_webview():
    assert not (
        hybrids.test_class_in_set(
            HYBRID_NOT_WEBVIEW_CLASS, list(hybrids.WEBVIEW_PACKAGES), strict=False
        )
    )
    assert hybrids.test_class_in_set(
        HYBRID_WEBVIEW_CLASS, hybrids.PACKAGES_KNOWN_AS_HYBRID
    )


def test_detect_package():
    assert (
        hybrids.from_class_name_get_category(OWN_PACKAGE, OWN_PACKAGE_CLASS)
        == "ownPackage"
    )
    assert (
        hybrids.from_class_name_get_category(OWN_PACKAGE, HYBRID_WEBVIEW_CLASS)
        == "hybrid"
    )
    assert (
        hybrids.from_class_name_get_category(OWN_PACKAGE, ANDROID_NOT_WEBVIEW_CLASS)
        == "android"
    )
    assert hybrids.from_class_name_get_category(OWN_PACKAGE, OTHER_CLASS) == "other"


def test_get_apkhybrid():
    apkhybrid = hybrids.from_apkinfos(APK.APKINFOS)
    assert apkhybrid == HYBRIDS.APKWEB
