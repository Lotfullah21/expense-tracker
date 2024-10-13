from expenses.models import RequestLogs
from typing import Any

class RequestMiddleWareLogin:
    # The constructor is called when the middleware is initialized.
    def __init__(self, get_response) -> None:
        # get_response is a callable (usually a view) that takes a request and returns a response
        self.get_response = get_response
    
    # The __call__ method is called on each request processed by the middleware,request parameter represents the incoming HTTP request.
    def __call__(self,request) -> Any:
        request_info = (request)
        # vars(request_info) to capture all attributes of the request object as a dictionary.
        # print(vars(request_info))
        RequestLogs.objects.create(

            request_info=vars(request_info), request_type=request_info.method, request_method=request_info.path
        )
        print(request_info.path, request_info.method)
        # the middleware calls self.get_response(request) to pass the request to the next middleware or view in the chain and returns the resulting response.y
        return self.get_response(request)