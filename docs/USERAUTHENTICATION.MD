## User

The User model in Django is a built-in model provided by the `django.contrib.auth` package, which handles authentication and user management in Django applications. This model is essential for managing users and implementing authentication systems.

The User model is designed to facilitate user authentication, including user registration, login, password management, and user permissions. It provides a standard way to manage user data and integrates with Django's authentication framework.

The default User model includes the following fields:

| **Field Name** | **Type**        | **Description**                                                             | **Attributes**                         |
| -------------- | --------------- | --------------------------------------------------------------------------- | -------------------------------------- |
| `username`     | `CharField`     | A unique identifier for the user.                                           | Required, unique                       |
| `first_name`   | `CharField`     | The user's first name.                                                      | Optional                               |
| `last_name`    | `CharField`     | The user's last name.                                                       | Optional                               |
| `email`        | `EmailField`    | The user's email address.                                                   | Optional, unique if used               |
| `password`     | `CharField`     | The hashed password for the user.                                           | Required                               |
| `is_active`    | `BooleanField`  | Indicates whether the user account is active.                               | Default: `True`                        |
| `is_staff`     | `BooleanField`  | Indicates whether the user can log into the admin site.                     | Default: `False`                       |
| `is_superuser` | `BooleanField`  | Indicates whether the user has all permissions without explicit assignment. | Default: `False`                       |
| `last_login`   | `DateTimeField` | A timestamp of the last time the user logged in.                            | Optional                               |
| `date_joined`  | `DateTimeField` | A timestamp of when the user account was created.                           | Automatically set to current date/time |

#### User methods

| **Method**                     | **Description**                                                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `set_password(raw_password)`   | Sets the user's password to the given raw password after hashing it.                                         |
| `check_password(raw_password)` | Checks whether the given raw password is correct by comparing it to the stored hashed password.              |
| `get_full_name()`              | Returns the user's full name by combining `first_name` and `last_name`.                                      |
| `get_short_name()`             | Returns the user's short name, which is typically the `first_name`.                                          |
| `is_authenticated`             | Returns `True` if the user is authenticated (i.e., logged in).                                               |
| `is_active`                    | Returns `True` if the user's account is active (i.e., `is_active` is `True`).                                |
| `is_staff`                     | Returns `True` if the user can access the admin site (i.e., `is_staff` is `True`).                           |
| `is_superuser`                 | Returns `True` if the user has all permissions without explicit assignment (i.e., `is_superuser` is `True`). |

```py
from .models import TrackingExpenses, CurrentBalance
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def login_view(request):
    return render(request, "login.html")

def register_view(request):

    if request.method =="POST":
        user_name = request.POST.get("user_name")
        first_name= request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        user = User.objects.filter(username=user_name)
        if user.exists():
            messages.error(request,"User already existed")
            return redirect("register_view")

        user = User.objects.create(
            username = user_name,
            first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.save()
        messages.success(request,"User created successfully")
        return redirect("login_view")

    return render(request, "register.html")
```

```py
    user = User.objects.create(
        username = user_name,
        first_name=first_name, last_name=last_name
    )
    user.set_password(password)
    user.save()
```

we can use

```py
  # Create the new user
    user = User.objects.create_user(
        username=user_name,
        first_name=first_name,
        last_name=last_name,
        password=password
        )
```

#### Login

`./app_name/urls.py`

```py
from .views import index, removeTransaction, login_view, register_view, logout_view
from django.urls import path

urlpatterns = [
     path("",index,name="index"),
     path("remove/<int:id>/",removeTransaction,name="removeTransaction"),
     path("login/",login_view, name="login_view"),
     path("register/", register_view, name="register_view"),
     path("logout/", logout_view, name="logout_view")
]
```

`./app_name/views.py`

```py
from django.contrib.auth import authenticate, login, logout
def login_view(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user = User.objects.filter(username=user_name)
        if not user:
            messages.error(request,"User does not exist, please register first")
            return redirect("register_view")
        user = authenticate(username=user_name, password=password)
        if not user:
            messages.error(request,"Incorrect password, try again")
            return redirect("login_view")
        # Now user is authenticated, login it.
        login(request,user)
        return redirect("index")
    return render(request, "login.html")
```

`user = User.objects.filter(username=user_name)` queries the database for any user with the provided username. This returns a queryset, which will be empty if no user is found.

#### authentication

```py
user = authenticate(username=user_name, password=password)
```

`user = authenticate(username=user_name, password=password)` attempts to authenticate the user with the provided username and password.
If authentication is successful, user will hold the user object; if unsuccessful, it will return None.

```py
login(request, user)
return redirect("/")
```

`login(request, user)` logs the user in by creating a session for the authenticated user.
return redirect("/") redirects the user to the home page (or dashboard) after successful login.

#### Breakdown of the login() Function

###### Session Creation:

The login() function creates a new session for the user. This session is a way for Django to remember that the user is authenticated across multiple requests. It involves generating a session ID and storing it in the session store (often in the database or cache).

###### User's Authentication Status:

It marks the user as authenticated in the session. This means that, for the duration of their session, Django will consider this user to be logged in, allowing them to access views and resources that require authentication.

###### Setting Session Data:

The user's ID is stored in the session data, typically as request.session[django.contrib.auth.LOGIN_SESSION_KEY]. This allows Django to retrieve the user object on subsequent requests and determine if the user is logged in or not.

###### Handling User Permissions:

If you have any custom permissions or groups set up for users, the login() function can also help in checking these permissions when the user accesses different parts of your application.

###### Redirecting the User:

After calling login(), it is common to redirect the user to a different page (like the home page or dashboard). This is typically done with a redirect() call after successfully logging in.

when we use the `login()` function in Django, it sets up the session for the authenticated user, allowing them to access protected resources. It is an essential part of managing user authentication in a Django application

when user is logged in, we can print the users information on screen using `request.user.attribute` inside a template.

`py{{request.user.first_name}} {{request.user.last_name}}`

`/app_name/templates`

```html
<div class="container mx-auto px-4">
	<a
		href="{% url 'logout_view' %}"
		class="btn bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition inline-block mb-4 pointer"
		>logout</a
	>
	{{request.user.first_name}} {{request.user.last_name}}
</div>
```

## Route Protection

By using `login_required` decoration from django, we can protect our routes and only authenticated users can login.

```py
from django.contrib.auth.decorators import login_required
```

`@login_required(login_url="login_view")`, the params we pass here is the view we want to guide the user if the user is not authenticated.

paste it on top of every view you want protect.

```py
from django.contrib.auth.decorators import login_required
@login_required(login_url="login_view")
def index(request):
    # logic
```

### Returning the User Object for Further Use

When we call `create_user` or `create_superuser`, we expect a `CustomUser` instance to be returned. This allows the created user object to be used further in our code, for example, to log in the user, access their attributes, or perform additional operations.
By returning the CustomUser instance, Django or any code calling this function gets access to the newly created user object, which is essential for working with the user in later steps.
