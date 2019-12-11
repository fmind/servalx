# -*- coding: utf-8 -*-
"""High-order functions for the servalx project."""

import hashlib

import funcy as F

# FUNCTIONS


def fnone(fn, default, x):
    return fn(x) if x is not None else default


def fempty(fn, default, coll):
    return fn(coll) if len(coll) != 0 else default


def fexcept(fn, default, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception:
        return default


def flatten(index):
    """Flatten a dict structure in a list."""
    return [F.merge(v, {"ID": k}) for k, v in index.items()]


def unflatten(flat):
    """Unflatten a list in a dict structure."""
    return {d["ID"]: F.omit(d, ["ID"]) for d in flat}


def compute_sha256(buffer):
    """Compute the sha256 of a buffer."""
    return hashlib.sha256(buffer).hexdigest()
