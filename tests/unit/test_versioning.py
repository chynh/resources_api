import pytest
from flask import Flask, Response

from app.versioning import versioned, LATEST_API_VERSION


def test_passes_valid_version_specified_in_api_header_to_wrapped_route(app, client):
    @app.route('/endpoint')
    @versioned(valid_versions=['1.4'])
    def endpoint(version: float):
        return dict(version=version)

    response: Response = client.get('/endpoint', headers=[('X-Api-Version', '1.4')])

    assert response.json == dict(version=1.4)


def test_defaults_to_latest_api_version_when_api_header_is_not_passed(app, client):
    @app.route('/endpoint')
    @versioned
    def endpoint(version: float):
        return dict(version=version)

    response: Response = client.get('/endpoint')

    expected_version = float(LATEST_API_VERSION)
    assert response.json == dict(version=expected_version)


@pytest.mark.parametrize('header_value', ['99.99', 'i-am-a-monkey', '1.2.0-alpha.1'])
def test_defaults_to_latest_api_version_when_invalid_version_passed_in_api_header(
        app, client, header_value):
    @app.route('/endpoint')
    @versioned
    def endpoint(version: float):
        return dict(version=version)

    response: Response = client.get(
        '/endpoint', headers=[('X-API-Version', header_value)])

    expected_version = float(LATEST_API_VERSION)
    assert response.json == dict(version=expected_version)


@pytest.fixture
def app():
    return Flask(__name__)


@pytest.fixture
def client(app):
    return app.test_client()
