from django.utils import timezone

class AdminTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            timezone.activate('Africa/Lagos')
        else:
            timezone.activate('UTC')

        response = self.get_response(request)

        return response
