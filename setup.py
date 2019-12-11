# -*- coding: utf-8 -*-

from setuptools import setup

PROJECT = "servalx"
PACKAGE = "servalx"
VERSION = "1.7.0"
LICENSE = "LGPL-3.0"
USERNAME = "fmind"
AUTHOR = u"Médéric Hurier (fmind)"
COPYRIGHT = u"2019, Médéric Hurier"
EMAIL = "fmind@fmind.me"
URL = "https://github.com/fmind/servalx"

DESC = "A set of tools and modules to process Android malware on Androzoo."

DOC = DESC

PLATFORMS = "any"

KEYWORDS = [PACKAGE]

PACKAGES = [PACKAGE]

SCRIPTS = [
    "bin/apkcert",
    "bin/apkfeats",
    "bin/apkhybrid",
    "bin/apkindex",
    "bin/apkinfos",
    "bin/apkmanif",
    "bin/apkperms",
    "bin/apksha256",
    "bin/apkstream",
    "bin/apkupload",
    "bin/dball",
    "bin/dbids",
    "bin/dbone",
    "bin/dbput",
    "bin/idxone",
    "bin/idxput",
    "bin/vtreport",
]

CLASSIFIERS = [
    "Operating System :: POSIX",
    "Natural Language :: English",
    "Intended Audience :: Developers",
    "Development Status :: 2 - Pre-Alpha",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
]

REQUIRES = {
    "dev": [
        "tox",
        "yapf",
        "ipdb",
        "wheel",
        "isort",
        "invoke",
        "ipython",
        "autoenv",
        "pygments",
        "virtualenv",
    ],
    "docs": ["sphinx"],
    "setup": [],
    "tests": ["pytest-xdist"],
    "coverage": ["pytest-cov"],
    "install": [
        "funcy",
        "couchdb",
        "entropy",
        "memoize2",
        "requests",
        "simplejson",
        "statistics",
        "python-magic",
        "elasticsearch",
        "androguard==3.0.1",
    ],
}

if __name__ == "__main__":
    setup(
        name=PACKAGE,
        version=VERSION,
        license=LICENSE,
        description=DESC,
        long_description=DOC,
        author=AUTHOR,
        author_email=EMAIL,
        maintainer=AUTHOR,
        maintainer_email=EMAIL,
        url=URL,
        download_url=URL,
        keywords=KEYWORDS,
        platforms=PLATFORMS,
        classifiers=CLASSIFIERS,
        extras_require=REQUIRES,
        tests_require=REQUIRES["tests"],
        setup_requires=REQUIRES["setup"],
        install_requires=REQUIRES["install"],
        include_package_data=True,
        packages=PACKAGES,
        scripts=SCRIPTS,
        zip_safe=False,
    )
