# any remote errors with inherit from HttpError
class HttpError(Exception):
    error_code = 'INTERNAL_SERVER_ERROR'
    status_code = 500


class HttpNotAcceptable(HttpError):
    error_code = 'NOT_ACCEPTABLE'
    status_code = 406


class HttpUnsupportedMediaType(HttpError):
    error_code = 'UNSUPPORTED_MEDIA_TYPE'
    status_code = 415


class HttpMalformedJSON(HttpError):
    error_code = 'MALFORMED_JSON'
    status_code = 753
