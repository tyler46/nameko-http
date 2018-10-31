from nameko.web.server import WebServer as BaseWebServer


class WebServer(BaseWebServer):

    def context_data_from_headers(self, request):
        context_data = super().context_data_from_headers(request)
        context_data['origin'] = request.headers.get('origin')
        context_data['methods'] = request.headers.get('access-control-request-method')
        context_data['headers'] = request.headers.get('access-control-request-headers')
        return context_data
