# -*- coding: utf-8 -*-

"""Main module."""
import json

from nameko.exceptions import safe_for_serialization
from nameko.web.handlers import HttpRequestHandler
from werkzeug.wrappers import Response

from nameko_http.exceptions import (
    HttpError, HttpNotAcceptable, HttpUnsupportedMediaType,
)
from nameko_http import constants
from nameko_http.utils import client_accepts_json, is_json_request, as_string
from nameko_http.server import WebServer


class HttpApiEntrypoint(HttpRequestHandler):
    """Rest API http Entrypoint."""
    server = WebServer()

    def __init__(self, method, url, **kwargs):
        self.cors_enabled = kwargs.get('cors_enabled', False)
        if self.cors_enabled:
            parts = method.split(',')
            method = ','.join(['OPTIONS'] + parts)

        super().__init__(method, url, **kwargs)

    def handle_request(self, request):
        """Process incoming request and check request headers.
        Depending on request method & request headers a http error may be raised.

        - If client doesn't accept json responses, then HTTP Not Acceptable error will be raised
        - If request method is one of 'POST', 'PUT', 'PATCH' and header `Content-Type` is not
          `application/json`, then HTTP Unsupported MediaType will be raised.

        Args:

            req (werkzeug.Request): Incoming nameko web request.

        Returns:
            None

        Raises:
            HttpNotAcceptable: Client doesn't accept json
            HttpUnsupportedMediaType: Request method in ['post', 'put', 'pach'] but
                                      `Content-Type` does not support `application/json`.
        """
        accept = request.headers.get('accept', 'text/plain')

        try:
            if not client_accepts_json(accept):
                raise HttpNotAcceptable('Only responses encoded as json supported')

            if request.method.lower() in ['post', 'put', 'patch']:
                mimetype = request.mimetype
                if mimetype is None:
                    mimetype = request.content_type

                if not is_json_request(mimetype):
                    raise HttpUnsupportedMediaType('JSON payload expected')

        except HttpError as exc:
            return self.response_from_exception(exc)

        response = super().handle_request(request)

        # Some validation should be applied regarding cors headers
        if self.cors_enabled:
            context_data = self.server.context_data_from_headers(request)
            response.headers.add(
                'Access-Control-Allow-Origin',
                as_string(context_data.get('origin', constants.CORS_ALLOW_ORIGINS_LIST))
            )
            response.headers.add(
                'Access-Control-Allow-Headers',
                as_string(context_data.get('headers', constants.CORS_ALLOW_HEADERS_LIST))
            )
            response.headers.add(
                'Access-Control-Allow-Methods',
                as_string(context_data.get('headers', constants.CORS_ALLOW_METHODS_LIST))
            )
            response.headers.add(
                'Access-Control-Allow-Credentials',
                str(constants.CORS_ALLOW_CREDENTIALS).lower()
            )

        return response

    def response_from_exception(self, exc):

        if isinstance(exc, HttpError):
            status_code = exc.status_code
            error_code = getattr(exc, 'error_code', 'UNEXPECTED_ERROR')
        else:
            status_code, error_code = 500, 'UNEXPECTED_ERROR'

        reason = safe_for_serialization(exc)

        return Response(
            json.dumps({
                'error_code': error_code,
                'reason': reason
            }),
            status=status_code,
            mimetype='application/json'
        )


api = HttpApiEntrypoint.decorator
