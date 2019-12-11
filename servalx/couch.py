# -*- coding: utf-8 -*-
"""Client methods for accessing Couch API."""

import itertools

import couchdb
import couchdb.json
import requests
import simplejson as json

# the default encode/decode causes unicode errors
couchdb.json.use(encode=json.dumps, decode=json.loads)

# CONSTANTS

DB_KEYS = frozenset(["_id", "_rev"])

# ERRORS


class CouchError(Exception):
    pass


class DocumentNotFound(CouchError):
    pass


class RevisionConflict(CouchError):
    pass


# CLASSES


class Connection(object):
    DB_APKCODES = "apkcodes"
    DB_APKINFOS = "apkinfos"
    DB_APKFEATS = "apkfeats"
    DB_APKMETAS = "apkmetas"
    DB_APKPERMS = "apkperms"
    DB_APKEXTRAS = "apkextras"
    DB_APKLABELS = "apklabels"
    DB_APKMARKETS = "apkmarkets"
    DB_VIRUSTOTAL = "virustotal"
    DB_APKINDEXES = "apkindexes"
    DB_APKHYBRIDS = "apkhybrids"

    def __init__(self, url):
        self.url = url
        self.server = couchdb.Server(self.url)


# HELPERS

IDENTITY = lambda x: x
TO_INT = lambda x: int(x)
LOWERSTRIP = lambda x: x.strip().lower()
REMOVE_DBKEYS = lambda x: {k: v for k, v in x.items() if k not in DB_KEYS}

# FUNCTIONS


def keys(conn, db_id, view="_all_docs", _per_http=100):
    """Return the list of keys for a given database."""
    db = conn.server[db_id]
    gen = itertools.chain(db.iterview(view, _per_http))

    for key in gen:
        yield key.id


def head(conn, db_id, doc_key, on_key=LOWERSTRIP, on_res=IDENTITY):
    """Return True if a document exists in the database."""
    key = on_key(doc_key)
    db = conn.server[db_id]

    return on_res(key in db)


def get(conn, db_id, doc_key, on_key=LOWERSTRIP, on_doc=REMOVE_DBKEYS):
    """Return a document if it exists in the database, else a CouchError."""
    key = on_key(doc_key)
    db = conn.server[db_id]

    try:
        return on_doc(db[key])
    except couchdb.ResourceNotFound:
        raise DocumentNotFound({"db": db_id, "key": key})


def get_or_none(*args, **kwargs):
    """Return a document if it exists in the database, else return None."""
    try:
        return get(*args, **kwargs)
    except DocumentNotFound:
        return None


def raw(conn, db_id, doc_key, on_key=LOWERSTRIP, on_doc=IDENTITY):
    """Return a raw json if it exists in the database, else a CouchError. """
    key = on_key(doc_key)
    uri = "/".join([conn.url, db_id, key])

    res = requests.get(uri)
    code = res.status_code

    if code == 404:
        raise DocumentNotFound({"db": db_id, "key": key})
    elif code != 200:
        raise CouchError("Could not retrieve JSON from: {}".format(uri))

    try:
        return res.text.strip().encode("utf-8")
    except couchdb.ResourceNotFound:
        raise DocumentNotFound({"db": db_id, "key": key})


def rawall(conn, db_id, doc_keys, on_key=LOWERSTRIP, chunk_size=2048):
    """Return a raw json if it exists in the database, else a CouchError. """
    params = {"include_docs": True}
    keys = {"keys": [on_key(k) for k in doc_keys]}
    uri = "/".join([conn.url, db_id, "_all_docs"])

    res = requests.post(uri, json=keys, params=params, stream=True)

    if res.status_code != 200:
        raise CouchError("Could not retrieve content from: {}".format(uri))

    for chunk in res.iter_content(chunk_size=chunk_size):
        yield chunk


def put(conn, db_id, doc_key, doc, on_doc=IDENTITY, on_key=LOWERSTRIP):
    """Put a document in the database and returns its key, else a CouchError."""
    doc = on_doc(doc)
    key = on_key(doc_key)
    db = conn.server[db_id]

    try:
        db[key] = doc

        return key
    except Exception as e:
        raise CouchError({"db": db_id, "key": key, "error": str(e), "type": type(e)})


def delete(conn, db_id, doc_key, on_key=LOWERSTRIP):
    """Delete a document from the database and return True, else an Error."""
    key = on_key(doc_key)
    db = conn.server[db_id]
    doc = get(conn, db_id, key, on_doc=IDENTITY)

    if doc is None:
        return True

    try:
        db.delete(doc)

        return True
    except Exception as e:
        raise CouchError({"db": db_id, "key": key, "error": str(e), "type": type(e)})
