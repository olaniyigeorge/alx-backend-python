import logging
from datetime import datetime, timedelta
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
    




class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of POST requests (messages) from an IP
    to a maximum of 5 per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = {}  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path.lower():
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Get or create timestamp list for this IP
            timestamps = self.ip_message_log.get(ip, [])

            # Remove timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            timestamps = [t for t in timestamps if t > one_minute_ago]

            # Check if user exceeded the limit
            if len(timestamps) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")

            # Record this message timestamp
            timestamps.append(now)
            self.ip_message_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        """Retrieve client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip