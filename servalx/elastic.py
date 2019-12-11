# -*- coding: utf-8 -*-
"""Client methods for accessing Elastic API."""

import elasticsearch as es

# ERRORS

ElasticError = es.ElasticsearchException

# CLASSES


class Connection(object):
    IDX_APKINDEX = "apkindex"
    DOC_TYPE = "doc"  # as common name

    def __init__(self, urls, timeout=60):
        """Initialize a connection to a cluster."""
        self.urls = urls.split()
        self.cluster = es.Elasticsearch(
            self.urls, timeout=timeout, retry_on_timeout=True
        )


# HELPERS

LOWERSTRIP = lambda x: x.strip().lower()

# FUNCTIONS


def get(conn, idx, key, on_key=LOWERSTRIP):
    """Return a document for the given key."""
    key = on_key(key)

    return conn.cluster.get_source(idx, conn.DOC_TYPE, key)


def index(conn, idx, key, doc, on_key=LOWERSTRIP):
    """Create or replace a document on an index."""
    key = on_key(key)

    return conn.cluster.index(idx, conn.DOC_TYPE, doc, key)


def update(conn, idx, key, doc, on_key=LOWERSTRIP):
    """Update an existing document on an index."""
    key = on_key(key)
    body = {"doc": doc}

    return conn.cluster.update(idx, conn.DOC_TYPE, key, body, fields=["_id"])
