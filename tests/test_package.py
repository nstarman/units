"""Test the package itself."""

from __future__ import annotations

import importlib.metadata

import units as m


def test_version():
    assert importlib.metadata.version("units") == m.__version__
