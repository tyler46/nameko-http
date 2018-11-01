nameko-http
===========

Http utilities for Nameko built-in HTTP extension

Quickstart
----------

Install from Vermantia pypi:

```bash
  $ pip install --extra-index-url https://pypi.vermantiagaming.com/simple nameko-mst
```

Example:

```python
# helloworld.py
import json

from werkzeug.wrappers import Response

from nameko_http import api
from nameko_http.exceptions import HttpError


class HttpForbidden(HttpError):
    # Any Http Exceptions that are going to be raised need to inherit
    # from base exception class: HttpError.
    error_code = 'FORBIDDEN'
    status_code = 403


class ExampleService:
    name = "exampleservice"

    @api('GET', '/privileged')
    def forbidden(self, request):
      raise HttpForbidden('You shall not access')

    @api('GET', '/foo', cors_enabled=True)
    def get_foo(self, request):
        return Response(
            json.dumps({'value': 'foo'}),
            status=200,
            mimetype='application/json'
        )
```

```bash
$ nameko run helloworld
starting services: exampleservice
```

```bash
$ curl -i localhost:8000/privileged
HTTP/1.1 403 FORBIDDEN
Content-Type: application/json
Content-Lentgh: 61
Date: Thu, 01 Nov 2018 14:21:14 GMT

{"error_code": "FORBIDDEN", "reason": "You shall not access"}
```

```bash 
curl -i localhost:8000/foo
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 16
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Authorization, Content-Type, Accept
Access-Control-Allow-Methods: OPTIONS, GET, POST, PUT, PATCH, DELETE
Access-Control-Allow-Credentials: false
Date: Thu, 01 Nov 2018 14:23:21 GMT

{"value": "foo"}
```

Features
--------

* Optional payload validation using Marshmallow Schemas

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
