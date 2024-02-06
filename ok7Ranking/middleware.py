from django.http import HttpResponseRedirect


class NoWWWRedirectMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_request(request):
        if request.method == 'GET':
            host = request.get_host()
            if host.lower().find('www.') == 0:
                no_www_host = host[4:]
                url = request.build_absolute_uri().replace(host, no_www_host, 1)
                return HttpResponseRedirect(url)
