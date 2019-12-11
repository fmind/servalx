# -*- coding: utf-8 -*-
"""Machine-Learning features from APK information."""

from __future__ import division

import re
from collections import Counter, defaultdict
from datetime import datetime
from functools import partial
from operator import truediv
from statistics import mean

from entropy import shannon_entropy

from servalx import android, commands, functions
from servalx import manifest as Manifest
from servalx import package as Package
from servalx import timezones

# CONSTANTS

RE_NO_ALPHA = "\W+"
RE_UPPER_CODE = "^[A-Z_]+$"  # can contain many _
RE_DOLLAR_CODE = "^.*\$.*$"  # must contain a single $
RE_NUMBER_CODE = "^\d[\d.]*$"  # can contain many dots
RE_LOWER_CODE = "^[a-z]+_[a-z_]+$"  # must include at least one _

RE_METHOD_CODE = "^[a-z]+[A-Z]\w+$"
RE_PACKAGE_CODE = "^[\w]+\.[\w.]+$"
RE_REFERENCE_CODE = "^\[?L.+/.+;?$"
RE_CLASS_CODE = "^[A-Z][a-z]+([A-Z][a-z]+)+"

RE_HTTP_URL = "^http:\/\/.*$"
RE_HTTPS_URL = "^https:\/\/.*$"
RE_SCHEME_URL = "^[a-z]+:\/\/.*$"

RE_X509_FIELD = r'[A-Z]+="[^"]+"|[A-Z]+=[^,]+'

DT_X509 = "%a %b %d %H:%M:%S %Z %Y"

# HELPERS


def _true1(cond):
    return 1 if cond else 0


def _merge_docs(initial, doc):
    """NOTE: The operation is destructive on the initial document."""
    initial.update(doc)

    return initial


## REGEXP


def _matches(regexp, s):
    return regexp.match(s) is not None


def _findall(regexp, s):
    return re.findall(regexp, s) if s is not None else []


## FLAT XML


def _is_tag(tag, elt):
    return elt["tag"] == tag


def _has_attr(attr, elt):
    return attr in elt["attrs"]


def _is_attr(attr, val, elt):
    return elt["attrs"].get(attr) == val


## STRINGS


def _split(sub, s, maxsplit=-1):
    return s.split(sub, maxsplit) if s is not None else None


def _entropy(string):
    return shannon_entropy(string.encode("utf-8"))


def _startswith(sub, s):
    return s.lower().startswith(sub) if s is not None else False


## DATETIMES


def _parse_date(format, d):
    try:
        return datetime.strptime(d, format)
    except ValueError:
        return None


def _timedelta_to_hours(td):
    return td.days * 24 + td.seconds // 3600 if td else 0


## FILEINFOS


def _has_magic(magic, infos):
    return magic in infos["magic"].lower()


## ITERABLE


def _has_len(l, coll):
    return len(coll) == l


## PARTIALS

## from fnone
_len0 = partial(functions.fnone, len, 0)
# default value (0) means: empty string -> no info
_entropy0 = partial(functions.fnone, _entropy, 0)
## from fempty
_sum0 = partial(functions.fempty, sum, 0)
_max0 = partial(functions.fempty, max, 0)
_min0 = partial(functions.fempty, min, 0)
_mean0 = partial(functions.fempty, mean, 0)
## from fexcept
_div0 = partial(functions.fexcept, truediv, 0)
_date = partial(functions.fexcept, datetime, None)
## from has_len
_has_len1 = partial(_has_len, 1)
_has_len2 = partial(_has_len, 2)
## from has_magic
_is_elf = partial(_has_magic, "elf")
_is_xml = partial(_has_magic, "xml")
_is_audio = partial(_has_magic, "audio")
_is_image = partial(_has_magic, "image")
_is_flash = partial(_has_magic, "flash")
## from has_tag
_has_action = partial(_is_tag, "action")
_has_activity = partial(_is_tag, "activity")
_has_activity_alias = partial(_is_tag, "activity-alias")
_has_application = partial(_is_tag, "application")
_has_category = partial(_is_tag, "category")
_has_data = partial(_is_tag, "@data")
_has_grant_uri_permission = partial(_is_tag, "grant-uri-permission")
_has_instrumentation = partial(_is_tag, "instrumentation")
_has_intent_filter = partial(_is_tag, "intent-filter")
_has_manifest = partial(_is_tag, "manifest")
_has_meta_data = partial(_is_tag, "meta-data")
_has_permission = partial(_is_tag, "permission")
_has_permission_group = partial(_is_tag, "permission-group")
_has_permission_tree = partial(_is_tag, "permission-tree")
_has_provider = partial(_is_tag, "provider")
_has_receiver = partial(_is_tag, "receiver")
_has_service = partial(_is_tag, "service")
_has_supports_screens = partial(_is_tag, "supports-screens")
_has_uses_configuration = partial(_is_tag, "uses-configuration")
_has_uses_feature = partial(_is_tag, "uses-feature")
_has_uses_library = partial(_is_tag, "uses-library")
_has_uses_permission = partial(_is_tag, "uses-permission")
_has_uses_sdk = partial(_is_tag, "uses-sdk")
## from is_attr
_is_attr_true = lambda attr, elt: _is_attr(attr, "true", elt)
_is_attr_false = lambda attr, elt: _is_attr(attr, "false", elt)
_is_exported = partial(_is_attr_true, "exported")
_is_bootaware = partial(_is_attr_true, "directBootAware")
## from split
_split_x509_field = partial(_split, "=", maxsplit=1)
## from parse_date
_parse_x509_date = partial(_parse_date, DT_X509)
## from matches (regexp)
_is_unix = lambda s: s in commands.complete()
_is_noalpha = partial(_matches, re.compile(RE_NO_ALPHA))
_is_upper = partial(_matches, re.compile(RE_UPPER_CODE))
_is_lower = partial(_matches, re.compile(RE_LOWER_CODE))
_is_numbers = partial(_matches, re.compile(RE_NUMBER_CODE))
_has_dollars = partial(_matches, re.compile(RE_DOLLAR_CODE))
_is_class = partial(_matches, re.compile(RE_CLASS_CODE))
_is_method = partial(_matches, re.compile(RE_METHOD_CODE))
_is_package = partial(_matches, re.compile(RE_PACKAGE_CODE))
_is_reference = partial(_matches, re.compile(RE_REFERENCE_CODE))
_is_http = partial(_matches, re.compile(RE_HTTP_URL))
_is_https = partial(_matches, re.compile(RE_HTTPS_URL))
_is_scheme = partial(_matches, re.compile(RE_SCHEME_URL))
## from findall (regexp)
_find_all_x509_fields = partial(_findall, RE_X509_FIELD)

# FUNCTIONS


def find_package(apkinfos):
    return apkinfos["manifest"]["attrs"]["package"]


def find_dexdate(apkinfos):
    return _date(*apkinfos["fileinfos"]["classes.dex"]["datetime"])


def from_debug(debug):
    doc = dict()

    doc["dex_debug"] = _true1(debug)

    return doc


def from_header(header):
    doc = dict()

    doc["dex_header_size"] = header.get("file_size", 0)

    return doc


def from_fields(fields):
    doc = dict()

    # variables
    names = [x for _, x in map(Package.split_field, fields.keys()) if x is not None]

    # attributes
    doc["dex_fields"] = _len0(names)
    doc["dex_fields_len"] = _mean0([len(x) for x in names])
    doc["dex_fields_1ch"] = _len0(filter(_has_len1, names))
    doc["dex_fields_2ch"] = _len0(filter(_has_len2, names))
    doc["dex_fields_1ch_per_field"] = _div0(doc["dex_fields_1ch"], doc["dex_fields"])
    doc["dex_fields_2ch_per_field"] = _div0(doc["dex_fields_2ch"], doc["dex_fields"])

    return doc


def from_methods(methods):
    doc = dict()

    # variables
    names = [x for _, x in map(Package.split_method, methods.keys()) if x is not None]
    instructions = [x["nb_instructions"] for x in methods.values()]

    # attributes
    doc["dex_methods"] = _len0(names)
    doc["dex_methods_len"] = _mean0([len(x) for x in names])
    doc["dex_methods_1ch"] = _len0(filter(_has_len1, names))
    doc["dex_methods_2ch"] = _len0(filter(_has_len2, names))
    doc["dex_methods_instructions_max"] = _max0(instructions)
    doc["dex_methods_instructions_total"] = _sum0(instructions)
    doc["dex_methods_instructions_per_method"] = _mean0(instructions)
    doc["dex_methods_1ch_per_method"] = _div0(
        doc["dex_methods_1ch"], doc["dex_methods"]
    )
    doc["dex_methods_2ch_per_method"] = _div0(
        doc["dex_methods_2ch"], doc["dex_methods"]
    )

    return doc


def from_classes(classes):
    doc = dict()

    # variables
    names = [x for _, x in map(Package.split_class, classes.keys()) if x is not None]

    # attributes
    doc["dex_classes"] = _len0(names)
    doc["dex_classes_len"] = _mean0([len(x) for x in names])
    doc["dex_classes_1ch"] = _len0(filter(_has_len1, names))
    doc["dex_classes_2ch"] = _len0(filter(_has_len2, names))
    doc["dex_classes_1ch_per_class"] = _div0(doc["dex_classes_1ch"], doc["dex_classes"])
    doc["dex_classes_2ch_per_class"] = _div0(doc["dex_classes_2ch"], doc["dex_classes"])

    return doc


def from_invokes(invokes, app_pkg):
    doc = dict()

    # attributes
    pkgscount = defaultdict(int)
    total = _sum0(invokes.values())
    # group invocation per package
    for invoked, n in invokes.items():
        pkg, _ = Package.split_invoke(invoked)

        if pkg is None:
            # default
            pkg = ""

        folded = Package.fold_support(pkg).replace("/", ".")
        pkgscount[folded] += n
    # copy prior to destructive operations
    pkgscount_copy = pkgscount.copy()
    # start by the most specific packages
    refpkgs_copy = list(android.PACKAGES)
    refpkgs_copy.reverse()
    # count the number of invokes per standard package
    # abs: absolute count, rel: relative to total invokes
    invokes_standard = 0
    for refpkg in refpkgs_copy:
        val = 0
        name = refpkg.lower().replace(".", "_")
        abskey = "dex_invokes_abspkg_{0}".format(name)
        relkey = "dex_invokes_relpkg_{0}".format(name)
        startswith_refpkg = partial(_startswith, refpkg.lower())

        for pkg, n in pkgscount_copy.items():
            if startswith_refpkg(pkg):
                del pkgscount_copy[pkg]
                invokes_standard += n
                val += n

        doc[abskey] = val
        doc[relkey] = _div0(val, total)

    # count the number of invokes for the app and lib packages
    invokes_internal = 0
    invokes_external = 0
    app_pkg = app_pkg.lower()  # avoid duplicate operation
    startswith_app = partial(_startswith, app_pkg)
    for pkg, n in pkgscount_copy.items():
        if startswith_app(pkg):
            invokes_internal += n
        else:
            invokes_external += n

    # variables
    doc["dex_invokes"] = total
    doc["dex_invokes_standard"] = invokes_standard
    doc["dex_invokes_internal"] = invokes_internal
    doc["dex_invokes_external"] = invokes_external
    doc["dex_invokes_standard_per_invoke"] = _div0(invokes_standard, doc["dex_invokes"])
    doc["dex_invokes_internal_per_invoke"] = _div0(invokes_internal, doc["dex_invokes"])
    doc["dex_invokes_external_per_invoke"] = _div0(invokes_external, doc["dex_invokes"])

    return doc


def from_strings(strings):
    doc = dict()

    remainings = list()
    strings = list(Counter(strings).elements())

    # variables
    http = list()
    https = list()
    schemes = list()
    uppers = list()
    lowers = list()
    dollars = list()
    numbers = list()
    classes = list()
    methods = list()
    packages = list()
    noalphas = list()
    references = list()
    for s in strings:
        if _is_http(s):
            http.append(s)
        elif _is_https(s):
            https.append(s)
        elif _is_scheme(s):
            schemes.append(s)
        elif _is_upper(s):
            uppers.append(s)
        elif _is_lower(s):
            lowers.append(s)
        elif _is_numbers(s):
            numbers.append(s)
        elif _has_dollars(s):
            dollars.append(s)
        elif _is_class(s):
            classes.append(s)
        elif _is_method(s):
            methods.append(s)
        elif _is_package(s):
            packages.append(s)
        elif _is_reference(s):
            references.append(s)
        elif _is_noalpha(s):
            noalphas.append(s)
        else:
            remainings.append(s)

    # attributes
    doc["dex_strings"] = _len0(strings)
    doc["dex_strings_http"] = _len0(http)
    doc["dex_strings_https"] = _len0(https)
    doc["dex_strings_uppers"] = _len0(uppers)
    doc["dex_strings_lowers"] = _len0(lowers)
    doc["dex_strings_schemes"] = _len0(schemes)
    doc["dex_strings_numbers"] = _len0(numbers)
    doc["dex_strings_dollars"] = _len0(dollars)
    doc["dex_strings_classes"] = _len0(classes)
    doc["dex_strings_methods"] = _len0(methods)
    doc["dex_strings_packages"] = _len0(packages)
    doc["dex_strings_noalphas"] = _len0(noalphas)
    doc["dex_strings_references"] = _len0(references)
    doc["dex_strings_remainings"] = _len0(remainings)
    doc["dex_strings_len"] = _mean0([len(x) for x in strings])
    doc["dex_strings_1ch"] = _len0(filter(_has_len1, strings))
    doc["dex_strings_2ch"] = _len0(filter(_has_len2, strings))
    doc["dex_strings_1ch_per_string"] = _div0(
        doc["dex_strings_1ch"], doc["dex_strings"]
    )
    doc["dex_strings_2ch_per_string"] = _div0(
        doc["dex_strings_2ch"], doc["dex_strings"]
    )
    doc["dex_strings_rem_per_string"] = _div0(
        doc["dex_strings_remainings"], doc["dex_strings"]
    )

    return doc


def from_dex(dex, package):
    initial = dict()

    docs = [
        from_debug(dex["debug"]),
        from_header(dex["header"]),
        from_fields(dex["fields"]),
        from_methods(dex["methods"]),
        from_classes(dex["classes"]),
        from_strings(dex["strings"]),
        from_invokes(dex["invokes"], package),
    ]

    doc = reduce(_merge_docs, docs, initial)

    ## derived attributes
    doc["dex_fields_per_class"] = _div0(doc["dex_fields"], doc["dex_classes"])
    doc["dex_methods_per_class"] = _div0(doc["dex_methods"], doc["dex_classes"])
    doc["dex_strings_per_class"] = _div0(doc["dex_strings"], doc["dex_classes"])
    doc["dex_strings_per_field"] = _div0(doc["dex_strings"], doc["dex_fields"])
    doc["dex_strings_per_method"] = _div0(doc["dex_strings"], doc["dex_methods"])
    doc["dex_invokes_per_class"] = _div0(doc["dex_invokes"], doc["dex_classes"])
    doc["dex_invokes_per_method"] = _div0(doc["dex_invokes"], doc["dex_methods"])

    return doc


def from_manifest(manifest):
    doc = dict()
    man = Manifest.flatten(manifest)

    # variables
    activities = filter(_has_activity, man)
    activity_aliases = filter(_has_activity_alias, man)
    applications = filter(_has_application, man)
    configurations = filter(_has_uses_configuration, man)
    customperms = filter(_has_permission, man)
    features = filter(_has_uses_feature, man)
    groupperms = filter(_has_permission_group, man)
    instrumentations = filter(_has_instrumentation, man)
    intent_actions = filter(_has_action, man)
    intent_categories = filter(_has_category, man)
    intent_data = filter(_has_data, man)
    intent_filters = filter(_has_intent_filter, man)
    librairies = filter(_has_uses_library, man)
    manifests = filter(_has_manifest, man)
    metadatas = filter(_has_meta_data, man)
    permissions = filter(_has_uses_permission, man)
    providers = filter(_has_provider, man)
    providers_bootaware = filter(_is_bootaware, providers)
    providers_exported = filter(_is_exported, providers)
    receivers = filter(_has_receiver, man)
    receivers_bootaware = filter(_is_bootaware, receivers)
    receivers_exported = filter(_is_exported, receivers)
    screens = filter(_has_supports_screens, man)
    sdks = filter(_has_uses_sdk, man)
    services = filter(_has_service, man)
    services_bootaware = filter(_is_bootaware, services)
    services_exported = filter(_is_exported, services)
    treeperms = filter(_has_permission_tree, man)
    uriperms = filter(_has_grant_uri_permission, man)

    app = applications[0] if applications else {}
    manman = manifests[0] if manifests else {}
    sdk = sdks[0]["attrs"] if sdks else {}

    permnames = frozenset(
        [
            x["attrs"]["name"].replace("android.permission.", "").upper()
            for x in permissions
        ]
    )

    # attribute
    ## sdk
    doc["man_sdk_min"] = int(sdk.get("minsdkversion", 0))
    doc["man_sdk_max"] = int(sdk.get("maxsdkversion", 0))
    doc["man_sdk_target"] = int(sdk.get("targetsdkversion", 0))
    ## manifest
    doc["man_shared_user"] = _true1(_has_attr("shareduserid", manman))
    ## application
    doc["man_app_has_allowtaskreparenting"] = _true1(
        _is_attr_true("allowtaskreparenting", app)
    )
    doc["man_app_has_debuggable"] = _true1(_is_attr_true("debuggable", app))
    doc["man_app_has_directbootaware"] = _true1(_is_attr_true("directbootaware", app))
    doc["man_app_has_isgame"] = _true1(_is_attr_true("isgame", app))
    doc["man_app_has_largeheap"] = _true1(_has_attr("largeheap", app))
    doc["man_app_has_networksecurityconfig"] = _true1(
        _has_attr("networksecurityconfig", app)
    )
    doc["man_app_has_persistent"] = _true1(_is_attr_true("persistent", app))
    doc["man_app_has_requiredaccounttype"] = _true1(
        _has_attr("requiredaccounttype", app)
    )
    doc["man_app_has_restrictedaccounttype"] = _true1(
        _has_attr("restrictedaccounttype", app)
    )
    doc["man_app_has_supportsrtl"] = _true1(_is_attr_true("supportsrtl", app))
    doc["man_app_has_testonly"] = _true1(_is_attr_true("testonly", app))
    doc["man_app_has_vmsafemode"] = _true1(_is_attr_true("vmsafemode", app))
    doc["man_app_hasno_allowbackup"] = _true1(_is_attr_false("allowbackup", app))
    doc["man_app_hasno_enabled"] = _true1(_is_attr_false("enabled", app))
    doc["man_app_hasno_extractnativelibs"] = _true1(
        _is_attr_false("extractnativelibs", app)
    )
    doc["man_app_hasno_hascode"] = _true1(_is_attr_false("hascode", app))
    doc["man_app_hasno_usescleartexttraffic"] = _true1(
        _is_attr_false("usescleartexttraffic", app)
    )
    ## services
    doc["man_services"] = _len0(services)
    doc["man_services_exported"] = _len0(services_exported)
    doc["man_services_bootaware"] = _len0(services_bootaware)
    ## activities
    doc["man_activities"] = _len0(activities)
    doc["man_activities_aliases"] = _len0(activity_aliases)
    ## receivers
    doc["man_receivers"] = _len0(receivers)
    doc["man_receivers_exported"] = _len0(receivers_exported)
    doc["man_receivers_bootaware"] = _len0(receivers_bootaware)
    ## providers
    doc["man_providers"] = _len0(providers)
    doc["man_providers_exported"] = _len0(providers_exported)
    doc["man_providers_bootaware"] = _len0(providers_bootaware)
    ## intent-filters
    doc["man_intent_filters"] = _len0(intent_filters)
    doc["man_intent_filters_data"] = _len0(intent_data)
    doc["man_intent_filters_actions"] = _len0(intent_actions)
    doc["man_intent_filters_categories"] = _len0(intent_categories)
    ## permissions
    doc["man_perms"] = _len0(permissions)
    ## other attributes
    doc["man_configurations"] = _len0(configurations)
    doc["man_custom_perms"] = _len0(customperms)
    doc["man_features"] = _len0(features)
    doc["man_groupperms"] = _len0(groupperms)
    doc["man_instrumentations"] = _len0(instrumentations)
    doc["man_librairies"] = _len0(librairies)
    doc["man_metas"] = _len0(metadatas)
    doc["man_screens"] = _len0(screens)
    doc["man_treeperms"] = _len0(treeperms)
    doc["man_uriperms"] = _len0(uriperms)
    # intersect the number of dangerous and standard permissions
    dangerousperms_used = android.DANGEROUS & permnames
    standardperms_used = android.PERMISSIONS & permnames
    for perm in android.PERMISSIONS:
        key = "man_can_{0}".format(perm.lower())
        doc[key] = _true1(perm in standardperms_used)
    doc["man_perms_standard"] = _len0(standardperms_used)
    doc["man_perms_dangerous"] = _len0(dangerousperms_used)
    doc["man_perms_standard_per_perm"] = _div0(
        doc["man_perms_standard"], doc["man_perms"]
    )
    doc["man_perms_dangerous_per_perm"] = _div0(
        doc["man_perms_dangerous"], doc["man_perms"]
    )

    return doc


def from_files(filesinfos):
    doc = dict()
    files = filesinfos.values()
    filesize = lambda files: sum(x["filesize"] for x in files)

    # variables
    ## files
    elfs = filter(_is_elf, files)
    xmls = filter(_is_xml, files)
    audios = filter(_is_audio, files)
    images = filter(_is_image, files)
    flashes = filter(_is_flash, files)
    ## sizes
    elfs_size = filesize(elfs)
    xmls_size = filesize(xmls)
    files_size = filesize(files)
    audios_size = filesize(audios)
    images_size = filesize(images)
    flashes_size = filesize(flashes)
    others_size = (
        files_size - elfs_size - xmls_size - audios_size - images_size - flashes_size
    )
    ## times
    times = [_date(*x["datetime"]) for x in files]
    deltas = [_timedelta_to_hours(x - _min0(times)) for x in times if x]
    mean_delta, max_delta = _mean0(deltas), _max0(deltas)

    # attributes
    doc["file_count_elfs"] = _len0(elfs)
    doc["file_count_xmls"] = _len0(xmls)
    doc["file_count_files"] = _len0(files)
    doc["file_count_audios"] = _len0(audios)
    doc["file_count_images"] = _len0(images)
    doc["file_count_flashes"] = _len0(flashes)
    doc["file_time_range_hours"] = max_delta
    doc["file_time_recent_hours"] = mean_delta
    doc["file_abssize_elfs"] = elfs_size
    doc["file_abssize_xmls"] = xmls_size
    doc["file_abssize_files"] = files_size
    doc["file_abssize_audios"] = audios_size
    doc["file_abssize_images"] = images_size
    doc["file_abssize_others"] = others_size
    doc["file_abssize_flashes"] = flashes_size
    doc["file_relsize_elfs"] = _div0(elfs_size, files_size)
    doc["file_relsize_xmls"] = _div0(xmls_size, files_size)
    doc["file_relsize_audios"] = _div0(audios_size, files_size)
    doc["file_relsize_images"] = _div0(images_size, files_size)
    doc["file_relsize_others"] = _div0(others_size, files_size)
    doc["file_relsize_flashes"] = _div0(flashes_size, files_size)

    return doc


def from_certificate(certificate, dex_date):
    doc = dict()

    # variables
    owner = certificate.get("owner")
    issuer = certificate.get("issuer")
    validity = certificate.get("valid_from")
    same_issuer_owner = owner and issuer and owner == issuer

    if validity is not None and " until: " in validity:
        valid_from, valid_until = validity.split(" until: ")
        valid_from = _parse_x509_date(valid_from)
    else:
        valid_from = None

    if owner is not None:
        owner_fields = {
            k: v for k, v in map(_split_x509_field, _find_all_x509_fields(owner))
        }
    else:
        owner_fields = {}

    if issuer is not None:
        issuer_fields = {
            k: v for k, v in map(_split_x509_field, _find_all_x509_fields(issuer))
        }
    else:
        issuer_fields = {}

    if dex_date and valid_from:
        delta_creation_publication = dex_date - valid_from
    else:
        delta_creation_publication = None

    # attributes
    doc["cert_owner_cn_len"] = _len0(owner_fields.get("CN"))
    doc["cert_owner_on_len"] = _len0(owner_fields.get("OU"))
    doc["cert_owner_o_len"] = _len0(owner_fields.get("O"))
    doc["cert_owner_cn_entropy"] = _entropy0(owner_fields.get("CN"))
    doc["cert_owner_on_entropy"] = _entropy0(owner_fields.get("OU"))
    doc["cert_owner_o_entropy"] = _entropy0(owner_fields.get("O"))
    doc["cert_owner_tz_detla"] = timezones.DELTAS.get(issuer_fields.get("C"), 0)
    doc["cert_issuer_cn_len"] = _len0(issuer_fields.get("CN"))
    doc["cert_issuer_on_len"] = _len0(issuer_fields.get("OU"))
    doc["cert_issuer_o_len"] = _len0(issuer_fields.get("O"))
    doc["cert_issuer_cn_entropy"] = _entropy0(issuer_fields.get("CN"))
    doc["cert_issuer_on_entropy"] = _entropy0(issuer_fields.get("OU"))
    doc["cert_issuer_o_entropy"] = _entropy0(issuer_fields.get("O"))
    doc["cert_issuer_tz_detla"] = timezones.DELTAS.get(issuer_fields.get("C"), 0)
    doc["cert_same_issuer_owner"] = _true1(same_issuer_owner)
    doc["cert_delta_creation_publication"] = _timedelta_to_hours(
        delta_creation_publication
    )

    return doc


def from_apkinfos(apkinfos):
    """Convert an apkinfos document to a feature map."""
    initial = {"VERSION": 1}
    package = find_package(apkinfos)
    dex_date = find_dexdate(apkinfos)

    docs = [
        from_dex(apkinfos["dex"], package),
        from_files(apkinfos["fileinfos"]),
        from_manifest(apkinfos["manifest"]),
        from_certificate(apkinfos["certificate"], dex_date),
    ]

    doc = reduce(_merge_docs, docs, initial)

    ## derived
    doc["pkg_len"] = _len0(package)
    doc["pkg_entropy"] = _entropy0(package)
    doc["man_perms_per_class"] = _div0(doc["man_perms"], doc["dex_classes"])
    doc["man_perms_per_method"] = _div0(doc["man_perms"], doc["dex_methods"])
    doc["man_perms_per_invoke"] = _div0(doc["man_perms"], doc["dex_invokes"])
    doc["man_perms_per_instructions"] = _div0(
        doc["man_perms"], doc["dex_methods_instructions_total"]
    )

    return doc
