from django.http import HttpResponseForbidden

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')

        valid_api_keys = ["12firebf12"] 
    
        if api_key not in valid_api_keys:
            return HttpResponseForbidden("Invalid Api Key")

        return self.get_response(request) 