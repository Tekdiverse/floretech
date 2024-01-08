from django.utils import timezone
from userauths.views import perform_daily_task

class AdminTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            perform_daily_task()
            timezone.activate('Africa/Lagos')
        else:
            timezone.activate('UTC')

        response = self.get_response(request)

        return response
