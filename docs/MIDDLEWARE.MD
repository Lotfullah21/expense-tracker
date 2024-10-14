# Django Middleware Documentation

## What is Middleware?

Middleware is a framework of hooks into Django's request/response processing. It's a lightweight, low-level plugin system for globally altering Django’s input or output. Each middleware component is responsible for doing some specific function.

## Middleware Structure

A middleware is a Python class that defines at least one of the following methods:

- `__init__(self, get_response)`
- `__call__(self, request)`
- `process_view(self, request, view_func, view_args, view_kwargs)`
- `process_template_response(self, request, response)`
- `process_exception(self, request, exception)`
- `process_request(self, request)`
- `process_response(self, request, response)`

### Middleware Methods Explained

1. **`__init__(self, get_response)`**

   - Called once when the server starts. It can be used to initialize state, but it's generally kept lightweight.

2. **`__call__(self, request)`**

   - The actual middleware logic runs here. It takes the request and returns a response. This method must return an `HttpResponse` object.

3. **`process_view(self, request, view_func, view_args, view_kwargs)`**

   - Called just before the view is called. It can return either `None` or an `HttpResponse` object.

4. **`process_template_response(self, request, response)`**

   - Called just after the view has been called if the response has a `render()` method. It can modify the response before rendering the template.

5. **`process_exception(self, request, exception)`**

   - Called when a view raises an exception. It can return either `None` or an `HttpResponse` object.

6. **`process_request(self, request)`**

   - Called on each request, before the view is called. It can return either `None` or an `HttpResponse` object.

7. **`process_response(self, request, response)`**
   - Called on each response, after the view is called. It must return an `HttpResponse` object.

## Default Middleware

Django comes with a set of built-in middleware components:

1. **`django.middleware.security.SecurityMiddleware`**

   - Adds several security-related headers to responses.

2. **`django.contrib.sessions.middleware.SessionMiddleware`**

   - Enables session support.

3. **`django.middleware.common.CommonMiddleware`**

   - Adds various features, including URL rewriting and handling of certain response headers.

4. **`django.middleware.csrf.CsrfViewMiddleware`**

   - Provides protection against Cross-Site Request Forgeries.

5. **`django.contrib.auth.middleware.AuthenticationMiddleware`**

   - Associates users with requests.

6. **`django.contrib.messages.middleware.MessageMiddleware`**

   - Enables cookie- and session-based message storage.

7. **`django.middleware.clickjacking.XFrameOptionsMiddleware`**
   - Prevents the site from being embedded in an iframe, mitigating clickjacking attacks.

## Custom Middleware Example

```python
# custom_middleware.py

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to execute for each request before the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to execute for each request/response after the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Code to execute just before the view is called.
        pass

    def process_exception(self, request, exception):
        # Code to execute if an exception is raised in the view.
        pass
```

## How to add middleware

```py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'yourapp.custom_middleware.CustomMiddleware',
    # other middleware...
]

```
