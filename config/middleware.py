import uuid
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class RequestIDMiddleware(MiddlewareMixin):
    """
    Adds a unique request id to each request/response for tracing.
    """
    def process_request(self, request):
        request.id = uuid.uuid4().hex

    def process_response(self, request, response):
        req_id = getattr(request, "id", None)
        if req_id:
            response["X-Request-ID"] = req_id
        return response


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """
    Applies a basic Content Security Policy; can be tuned via settings.
    """
    def process_response(self, request, response):
        csp = getattr(settings, "CONTENT_SECURITY_POLICY", None)
        if csp:
            response["Content-Security-Policy"] = csp
        return response
