#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nameko_http` package."""

import json
import pytest

from nameko.testing.utils import get_extension

from nameko_http import api
from nameko_http.exceptions import HttpNotAcceptable
from nameko_http.utils import api_response



class ExampleService(object):
    name = 'exampleservice'

    @api('GET', '/foo/<int:bar>')
    def do_get(self, request, bar):
        return api_response(
            status=200,
            data={'value': bar}
        )

    @api('POST', '/post')
    def do_post(self, request):
        data = json.loads(request.get_data(as_text=True))
        value = data['value']
        return api_response(
            status=200,
            data={'value': value}
        )

    @api('GET', '/status_code', cors_enabled=True)
    def do_cors_enabled(self, request):
        return api_response(
            status=200,
            data={'value': 1},
        )

    @api('POST', '/cors_post', cors_enabled=True)
    def do_post_cors_enabled(self, request):
        data = json.loads(request.get_data(as_text=True))
        value = data['value']
        return api_response(
            status=201,
            data={'value': value}
        )

    @api('GET', '/cors_headers', cors_enabled=True)
    def do_get_cors_headers(self, request):
        return api_response(
            status=200,
            data={'headers': request.headers}
        )

    @api('GET', '/no_content', cors_enabled=False)
    def do_no_content(self, request):
        return api_response(
            status=204,
        )

    @api('PUT', '/empty_body')
    def handle_empty_body(self, request):
        return api_response(status=204)



@pytest.fixture
def web_session(container_factory, web_config, web_session):
    container = container_factory(ExampleService, web_config)
    container.start()
    return web_session


def test_no_acceptable(web_session):
    """Test that HttpNotAcceptable is raised when incorrect ``Accept`` header is used."""
    rv = web_session.get('/foo/42', headers={'Accept': 'application/xml'})
    assert rv.status_code == 406
    assert rv.json() == {
        'error_code': 'NOT_ACCEPTABLE',
        'reason': 'Only responses encoded as json supported'
    }


def test_unsupported_media(web_session):
    """Test that HttpUnsupportedMediaType is raised when incorrect ``Content-Type`` header is used."""
    rv = web_session.post(
        '/post',
        data=json.dumps({
            'value': 'foo'
        }),
        headers={'Accept': 'application/json', 'Content-Type': 'text/plain'}
    )
    assert rv.status_code == 415
    assert rv.json() == {
        'error_code': 'UNSUPPORTED_MEDIA_TYPE',
        'reason': 'JSON payload expected'
    }


def test_plain_get(web_session):
    rv = web_session.get('/foo/42')
    print(rv.headers)
    print(rv.request.headers)
    assert 'Access-Control-Allow-Origin' not in rv.headers
    assert rv.json() == {'value': 42}


def test_cors_enabled(web_session):
    rv = web_session.get('/status_code')
    assert 'Access-Control-Allow-Origin' in rv.headers
    assert rv.headers['Access-Control-Allow-Origin'] == '*'
    assert rv.headers['Access-Control-Allow-Methods'] == 'OPTIONS, GET, POST, PUT, PATCH, DELETE'


def test_post_cors_enabled(web_session):
    rv = web_session.post(
        '/cors_post',
        data=json.dumps({
            'value': 'foo'
        }),
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
    )
    assert 'Access-Control-Allow-Origin' in rv.headers
    assert rv.headers['Access-Control-Allow-Origin'] == '*'
    assert rv.headers['Access-Control-Allow-Methods'] == 'OPTIONS, GET, POST, PUT, PATCH, DELETE'


def test_get_cors_headers(web_session):
    rv = web_session.get(
        '/cors_headers',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'http://foo.example',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Accept, Authorization, Content-Type'
        }
    )
    assert 'Access-Control-Allow-Origin' in rv.headers
    assert rv.headers['Access-Control-Allow-Origin'] == 'http://foo.example'
    assert rv.headers['Access-Control-Allow-Methods'] == 'GET'
    assert rv.headers['Access-Control-Allow-Headers'] == 'Accept, Authorization, Content-Type'


def test_options_cors_headers(web_session):
    rv = web_session.options(
        '/cors_headers',
        headers={
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Accept, Authorization, Content-Type'
        }
    )
    assert 'Access-Control-Allow-Origin' in rv.headers
    assert rv.headers['Access-Control-Allow-Origin'] == '*'
    assert rv.headers['Access-Control-Allow-Methods'] == 'GET'
    assert rv.headers['Access-Control-Allow-Headers'] == 'Accept, Authorization, Content-Type'


def test_no_content(web_session):
    rv = web_session.get(
        '/no_content',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    )
    assert rv.status_code == 204
    assert rv.headers['Content-Length'] == '0'


def test_empty_request_body(web_session):
    rv = web_session.put(
        '/empty_body',
    )

    assert rv.status_code == 204
