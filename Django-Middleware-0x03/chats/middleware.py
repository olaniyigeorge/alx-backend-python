import logging
from datetime import datetime
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file
    including timestamp, user, and request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler('requests.log')
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_entry)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the chat app between certain hours.
    Access allowed only between 6PM and 9PM server time.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow only between 18 (6PM) and 21 (9PM)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access to the chat is restricted at this time.")

        return self.get_response(request)