#  -*- coding: utf-8 -*-
"""Funtions of classification of the data of apkinfos."""

from servalx import android

# CONSTANTS

VERSION = 1

WEBVIEW_PACKAGES = set(["webview", "WebView", "webView", "Webview", "WEBVIEW"])

PACKAGES_KNOWN_AS_HYBRID = {
    "cordova",
    "phonegap",
    "android_jsc",  # https://github.com/facebook/android-jsc
    "rhomobile",  # http://docs.rhomobile.com/en/5.4/rhoconnect/java-plugin
    "appcelerator.titanium",  # http://docs.appcelerator.com/module-apidoc/latest/android/org/appcelerator/titanium/package-summary.html
}

ANDROID_PACKAGES = {"com/android", "com/google/android", "android/support"}


#  FUNCTIONS


def add_one_at_item_in_dic(dic, item):
    """This function add one to a dictionary or init the dic"""
    try:
        dic[item] += 1
    except Exception:
        dic[item] = 1
    return


def get_class_and_method_from_invoke(invokes_string):
    """This function get the name fo the class and the method from which \
    the invokes belongs to"""
    # L{package}/{class}${innerClass};->{function}({type parameter})L{typeOfReturnValue};
    [class_name, method_temp_name] = invokes_string.split("->")
    return (class_name, method_temp_name.split("(")[0])


def test_class_in_set(class_string, set_to_detect, strict=True):
    """This function test if a class belongs to a certain category \
    this category is represented by a set"""
    # strict = False => if any part of the string set_to_detect somewere in class_string
    if strict:
        set_detected = set(
            [
                component_to_detect if component_to_detect in class_string else "None"
                for component_to_detect in list(set_to_detect)
            ]
        )
    else:
        set_detected = set(
            [
                component_to_detect if component_to_detect in itemPackage else "None"
                for itemPackage in class_string.split("/")
                for component_to_detect in set_to_detect
            ]
        )
    set_detected.discard("None")
    return set_detected != set([])


def test_item_in_list(class_string, list_to_detect):
    """This function tests if a class is in a list. \
    The list having a particular data format"""
    return any(itemTest in class_string for itemTest in list_to_detect)


def from_class_name_get_category(own_package, class_name):
    """This function return the category from which the class \
    belongs to"""
    if test_class_in_set(class_name, PACKAGES_KNOWN_AS_HYBRID):
        return "hybrid"
    elif test_item_in_list(class_name, ANDROID_PACKAGES):
        return "android"
    elif own_package in class_name:
        return "ownPackage"
    else:
        return "other"


def get_dic_classed(apkinfos, app_dic):
    """This function return the dictionnary with the data classified \
    from the apkinfos"""

    def add_class_in_dic(app_dic, categrory, class_, class_dic):
        """This function add the class at the good place in the dictionnary"""
        app_dic[categrory]["classes"][class_] = {
            "super": class_dic["super"],
            "methods": {},
            "nbMethods": 0,
        }
        add_one_at_item_in_dic(app_dic[categrory], "nbClasses")
        return

    def add_method_in_dic(app_dic, categrory, class_name, methods_dic, method_name):
        """This function add the method at the good place in the dictionnary"""
        class_dic = app_dic[categrory]["classes"][class_name]
        class_dic["methods"][method_name] = {
            "nbInstructions": methods_dic["nb_instructions"],
            "nbInvokes": 0,
        }
        add_one_at_item_in_dic(class_dic, "nbMethods")
        return

    def add_invoke_in_iic(app_dic, categrory, class_name, method_name, nb_invokes):
        """This function add the invoke at the good place in the dictionnary"""
        try:
            app_dic[categrory]["classes"][class_name]["methods"][method_name][
                "nbInvokes"
            ] = nb_invokes
        except Exception:
            try:
                app_dic[categrory]["classes"][class_name]["nbInvokes"] += nb_invokes
            except Exception:
                try:
                    app_dic[categrory]["classes"][class_name]["nbInvokes"] = nb_invokes
                except Exception:
                    try:
                        app_dic[categrory]["classes"]["otherCalls"][
                            "nbInvokes"
                        ] += nb_invokes
                    except Exception:
                        app_dic[categrory]["classes"]["otherCalls"] = {
                            "nbInvokes": nb_invokes
                        }
                    add_one_at_item_in_dic(
                        app_dic[categrory]["classes"]["otherCalls"], "nbMethods"
                    )
        return

    def loop_in_classes(classes, app_dic, own_package):
        """This function loop in the classes dictionnary"""
        set_frameworks_detected = set()
        for class_ in list(classes.keys()):
            class_dic = classes[class_]

            category_class = from_class_name_get_category(own_package, class_)
            is_webview_call = test_class_in_set(
                class_, list(WEBVIEW_PACKAGES), strict=False
            )
            if category_class == "hybrid":
                set_frameworks_detected.update(
                    set(
                        [
                            component_to_detect
                            if component_to_detect in class_
                            else "None"
                            for component_to_detect in list(PACKAGES_KNOWN_AS_HYBRID)
                        ]
                    )
                )
                if is_webview_call:
                    add_one_at_item_in_dic(app_dic, "nbwebviewHybridCalls")
            else:
                if is_webview_call:
                    add_one_at_item_in_dic(app_dic, "nbwebviewCalls")
            add_class_in_dic(app_dic, category_class, class_, class_dic)
        list_frameworks_detected = list(set_frameworks_detected)
        try:
            list_frameworks_detected.remove("None")
        except Exception:
            pass
        app_dic["hybrid"]["frameworkDetected"] = list_frameworks_detected
        return

    def loop_in_methods(methods, app_dic, own_package):
        """This function loop in the methods dictionnary"""
        for method in list(methods.keys()):
            method_dic = methods[method]
            class_name = method_dic["class"]
            method_name = method_dic["name"]

            category_class = from_class_name_get_category(own_package, class_name)
            add_method_in_dic(
                app_dic, category_class, class_name, method_dic, method_name
            )
        return

    def loop_in_invokes(invokes, app_dic, own_package):
        """This function loop in the invokes dictionnary"""
        for invoke in list(invokes.keys()):
            (class_name, method_name) = get_class_and_method_from_invoke(invoke)
            nb_invokes = invokes[invoke]

            category_class = from_class_name_get_category(own_package, class_name)
            add_invoke_in_iic(
                app_dic, category_class, class_name, method_name, nb_invokes
            )
        return

    own_package = apkinfos["manifest"]["attrs"]["package"].replace(".", "/")

    loop_in_classes(apkinfos["dex"]["classes"], app_dic, own_package)

    loop_in_methods(apkinfos["dex"]["methods"], app_dic, own_package)

    loop_in_invokes(apkinfos["dex"]["invokes"], app_dic, own_package)

    return


def classify_apkinfos(apkinfos):
    """This function initialize the app_dic and classify the apkinfos"""
    app_dic = {
        "sha256": apkinfos["sha256"],
        "VERSION": VERSION,
        "android": {"classes": {}, "nbClasses": 0},
        "ownPackage": {"classes": {}, "nbClasses": 0},
        "hybrid": {"classes": {}, "nbClasses": 0},
        "other": {"classes": {}, "nbClasses": 0},
        "nbwebviewCalls": 0,
        "nbwebviewHybridCalls": 0,
    }
    get_dic_classed(apkinfos, app_dic)
    return app_dic


def list_dangerous_permissions(manifest_infos, dangerous_permissions):
    """This function initialize the app_dic and classify the apkinfos"""
    dangerous_permission_output = []
    for manifest_info in manifest_infos:
        if manifest_info["tag"] in ["permission", "uses-permission"]:
            permission = manifest_info["attrs"]["name"]
            if permission.split(".")[-1].upper() in dangerous_permissions:
                dangerous_permission_output.append(permission)
    return dangerous_permission_output


def list_type_files_from_apkinfos(apkinfos, type_files):
    """This function lists all the files belonging to a certain type of \
    file"""
    apkfiles_data = apkinfos["fileinfos"]
    empty_set = set([])
    set_files = {}
    for file_name in list(apkfiles_data):
        file_infos = apkfiles_data[file_name]
        if set(file_infos["magic"].split(" ")) & set(
            type_files
        ) != empty_set or file_name.split(".")[-1] in set(type_files):
            set_files[file_name] = file_infos
    return set_files


def size_files(files_infos):
    """This function calculates the size of files from files_infos"""
    size = 0
    for file_name in list(files_infos):
        file_info = files_infos[file_name]
        size += file_info["filesize"]
    return size


def from_apkinfos(apkinfos):
    """This function return the apkhybrid from the apkinfos"""
    infos_analysed = classify_apkinfos(apkinfos)

    # Listing data to write
    apkhybrid = {"sha256": apkinfos["sha256"]}
    framework_detected = infos_analysed["hybrid"]["frameworkDetected"]

    # Ishybrid
    apkhybrid["isHybrid"] = 1 if framework_detected != [] else 0

    # Files data
    for type_file in [
        ["HTML", "html"],
        ["CSS", "css"],
        ["Js", "JS", "js", "javascript", "JAVASCRIPT"],
    ]:
        list_type_file = list_type_files_from_apkinfos(apkinfos, type_file)
        apkhybrid["nb" + type_file[0]] = len(list_type_file)
        apkhybrid["size" + type_file[0]] = size_files(list_type_file)

    # isHybrid
    for package_hybrid in PACKAGES_KNOWN_AS_HYBRID:
        pkg_detected = 1 if package_hybrid in framework_detected else 0
        apkhybrid["{}IsDetected".format(package_hybrid)] = pkg_detected

    # Hybrid Webviews calls
    apkhybrid["nbhybridWebviewCalls"] = infos_analysed["nbwebviewHybridCalls"]
    # Webviews calls
    apkhybrid["nbnonHybridWebviewCalls"] = infos_analysed["nbwebviewCalls"]

    # Total instructions and invokes
    for type_package in ["android", "ownPackage", "hybrid", "other"]:
        apkhybrid["nb" + type_package + "Classes"] = infos_analysed[type_package][
            "nbClasses"
        ]
        total_instructions = 0
        total_instructions = 0
        nb_methods = 0
        if infos_analysed[type_package]["nbClasses"] > 0:
            for class_name in infos_analysed[type_package]["classes"].keys():
                class_dic = infos_analysed[type_package]["classes"][class_name]
                if class_name == "otherCalls":
                    # No need to loop inside methods : there is no such dic : there are not listed
                    total_instructions += class_dic["nbInvokes"]
                else:
                    # Loop inside methods
                    for method in list(class_dic["methods"].keys()):
                        method_dic = class_dic["methods"][method]
                        total_instructions += method_dic["nbInstructions"]
                        total_instructions += method_dic["nbInvokes"]
                # Anyway the number of methods is present
                nb_methods += class_dic["nbMethods"]
        else:
            try:
                total_instructions += infos_analysed[type_package]["classes"][
                    "otherCalls"
                ]["nbInvokes"]
            except Exception:
                pass
        apkhybrid["nb" + type_package + "Methods"] = nb_methods
        apkhybrid["nbTotal" + type_package + "Instructions"] = total_instructions
        apkhybrid["nbTotal" + type_package + "Invokes"] = total_instructions

    # Dangerous Permissions
    apkhybrid["list_dangerous_permissions"] = list_dangerous_permissions(
        apkinfos["manifest"]["_children"], android.DANGEROUS
    )

    return apkhybrid
