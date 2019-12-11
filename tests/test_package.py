# -*- coding: utf-8 -*-

from servalx import package


def test_can_fold_support_from_package():
    # has effect
    assert package.fold_support("android.support.graphics") == "android.graphics"
    assert package.fold_support("android.support.v21.graphics") == "android.graphics"

    # has no effects
    ## not a support package
    assert package.fold_support("android.dom") == "android.dom"
    assert package.fold_support("android.graphics") == "android.graphics"
    ## not an android package
    assert package.fold_support("apple.support.graphics") == "apple.support.graphics"
    ## support is at the end
    assert package.fold_support("android.support") == "android.support"
    ## no support before version
    assert package.fold_support("android.v17.graphics") == "android.v17.graphics"
    ## the full module is not support
    assert (
        package.fold_support("android.nosupport.graphics")
        == "android.nosupport.graphics"
    )


def test_can_split_class_identifier():
    # ok
    assert package.split_class("LProcess;") == (None, "Process")
    assert package.split_class("Landroid/os/Process;") == ["android/os", "Process"]
    assert package.split_class("[Landroid/os/Process;") == ["android/os", "Process"]

    # errors
    ## no L at beginning
    assert package.split_class("android/os/Process;") == (None, None)
    ## no ; at the end
    assert package.split_class("Landroid/os/Process") == (None, None)


def test_can_split_field_identifier():
    # ok
    assert package.split_field("Landroid/os/Process;->STDIN") == (
        "android/os/Process",
        "STDIN",
    )
    assert package.split_field("[Landroid/os/Process;->STDIN") == (
        "android/os/Process",
        "STDIN",
    )

    # errors
    ## no L at beginning
    assert package.split_field("android/os/Process;->STDIN") == (None, None)
    ## no ;-> in the middle
    assert package.split_field("Landroid/os/Process>STDIN") == (None, None)
    ## missing identifier name
    assert package.split_field("Landroid/os/Process;->") == (None, None)
    ## missing identifier package
    assert package.split_field("L;->STDIN") == (None, None)


def test_can_split_method_identifier():
    # ok
    assert package.split_method("Landroid/os/Process;->killProcess(I)V") == (
        "android/os/Process",
        "killProcess(I)V",
    )
    assert package.split_method("[Landroid/os/Process;->killProcess(I)V") == (
        "android/os/Process",
        "killProcess(I)V",
    )

    # errors
    ## no L at beginning
    assert package.split_method("android/os/Process;->killProcess(I)V") == (None, None)
    ## no ;-> in the middle
    assert package.split_method("Landroid/os/Process>killProcess(I)V") == (None, None)
    ## missing identifier name
    assert package.split_method("Landroid/os/Process;->") == (None, None)
    ## missing identifier package
    assert package.split_method("L;->killProcess(I)V") == (None, None)


def test_can_split_invoke_identifier():
    # ok
    assert package.split_invoke("Ljava/lang/System;->exit(I)V") == (
        "java/lang/System",
        "exit(I)V",
    )
    assert package.split_invoke(
        "Ljava/lang/Class;->getClasses()[Ljava/lang/Class;"
    ) == ("java/lang/Class", "getClasses()[Ljava/lang/Class;")
    assert package.split_invoke(
        "[Ljava/lang/Class;->getClasses()[Ljava/lang/Class;"
    ) == ("java/lang/Class", "getClasses()[Ljava/lang/Class;")

    # errors
    ## no L at beginning
    assert package.split_invoke("java/lang/System;->exit(I)V") == (None, None)
    ## no ;-> in the middle
    assert package.split_invoke("Ljava/lang/System-exit(I)V") == (None, None)
    ## missing identifier name
    assert package.split_invoke("Ljava/lang/System;->(I)V") == (None, None)
    ## missing identifier package
    assert package.split_invoke("L;->exit(I)V") == (None, None)
    ## missing identifier signature
    assert package.split_invoke("Ljava/lang/System;->exitV") == (None, None)
    ## missing identifier return type
    assert package.split_invoke("Ljava/lang/System;->exit(I)") == (None, None)
