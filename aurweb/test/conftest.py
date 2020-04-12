"""
Fixtures for pytest.

This module is automatically loaded by pytest.
"""

import pytest
import sqlalchemy
import werkzeug.test
import werkzeug.wrappers
import werkzeug.wrappers.json

import aurweb.config
import aurweb.db
from aurweb.test.wsgihttp import WsgiHttpProxy


class Response(werkzeug.wrappers.CommonResponseDescriptorsMixin,
               werkzeug.wrappers.json.JSONMixin,
               werkzeug.wrappers.BaseResponse):
    """
    Custom response object to be returned by the test client. More mixins could
    be added if need be.

    See https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#mixin-classes
    """
    pass


@pytest.fixture
def client():
    """
    Build a Werkzeug test client for making HTTP requests to AUR. It requires
    that the AUR test website is already running at `[options] aur_location`,
    specified in the configuration file.

    When aurweb becomes a pure Flask application, this should return Flask’s
    test_client(), which is a Werkzeug test client too.
    https://flask.palletsprojects.com/en/1.1.x/testing/#the-testing-skeleton
    """
    base_uri = aurweb.config.get("options", "aur_location")
    proxy = WsgiHttpProxy(base_uri)
    return werkzeug.test.Client(proxy, Response)


@pytest.fixture(scope="session")
def db_engine():
    """
    Return an SQLAlchemy engine to the configured database.
    """
    return sqlalchemy.create_engine(aurweb.db.get_sqlalchemy_url())
