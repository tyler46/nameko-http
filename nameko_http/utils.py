# pylint: disable=missing-docstring
import json

import mimeparse
from nameko.exceptions import BadRequest
from werkzeug.wrappers import Response

from nameko_http.exceptions import HttpMalformedJSON


def client_accepts_json(accept):
    # Taken from https://github.com/falconry/falcon/blob/master/falcon/request.py#L967
    """Determine whether or not the client accepts json media type.

    Args:
        media_type (str): the ``Accept`` request header

    Returns:
        bool: ``True`` if the client  has  indicated in the accept header
        that accepts application/json media type. Otherwise, returns
        ``False``
    """
    if (accept == 'application/json') or (accept == '*/*'):
        return True

    try:
        return mimeparse.quality('application/json', accept) != 0.0
    except ValueError:
        return False


# Taken from https://github.com/sloria/webargs/blob/dev/webargs/core.py
def get_mimetype(content_type):
    return content_type.split(';')[0].strip() if content_type else None


def is_json_request(mimetype):
    """Indicates if the mimetype is JSON or not. By default a request
    is considered to include JSON data if the mimetype is
    ``application/json`` or ``application/*+json``.
    """
    if not mimetype:
        return False
    if ';' in mimetype:  # Allow Content-Type header to be parsed
        mimetype = get_mimetype(mimetype)
    if mimetype == 'application/json':
        return True
    if mimetype.startswith('application/') and mimetype.endswith('+json'):
        return True
    return False


def as_string(items):
    return ', '.join(items)


def get_json(request):
    """Returns request payload as json. In case of malformed json or
    no body, an appropriate http error gets returned.

    Args:
        req (werkzeug.Request): Incoming nameko web request.

    Returns:
        payload (dict):  Parsed request body as json.

    Raises:
        HttpBadRequest: If client has sent empty request body.
        HttpError: Status code 753. If client has sent a malformed request data.
    """
    body = request.get_data(as_text=True)
    if not body:
        raise BadRequest('Empty request body')

    try:
        return json.loads(body)
    except ValueError:
        raise HttpMalformedJSON('Malformed JSON. Could not decode the request body.')


def api_response(status=200, data=None):
    return Response(
        response=json.dumps(data) if data is not None else '',
        status=status,
        mimetype='application/json'
    )
