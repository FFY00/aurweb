"""
Test suite for the RPC interface.

See also `doc/rpc.txt` for the RPC interface documentation.
"""

import pytest
from sqlalchemy.sql import select

from aurweb.schema import Packages


def test_search_by_name(client, db_engine):
    """Take a package from the database, and find it through the RPC interface."""
    with db_engine.connect() as conn:
        pkg = conn.execute(select([Packages]).limit(1)).fetchone()
        if pkg is None:
            pytest.skip("needs at least one package in the database")
    resp = client.get("/rpc/", query_string={"v": "5", "type": "search", "arg": pkg["Name"]})
    result = resp.json
    assert result["resultcount"] >= 1
