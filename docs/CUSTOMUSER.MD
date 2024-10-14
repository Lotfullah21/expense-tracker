# User model customization

## AbstractUser

AbstractUser is a base class for creating a custom user model that includes all the fields and methods of Django's default User model, including username, first_name, last_name, email, password, and more.

If you only need to add a few additional fields or make minor changes to the user model, AbstractUser is ideal because it provides a complete, pre-built user model, allowing you to inherit from it and add custom fields or methods.

```py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
```

In this example, CustomUser inherits everything from AbstractUser (like username, email, etc.) and adds a custom field phone_number

## AbstractBaseUser

AbstractBaseUser is a more minimal base class for custom user models. It provides the core fields and functionality but leaves out some details, such as username, email, first_name, and last_name.

It's used when you need full control over your user model. You define which fields are important (e.g., using email instead of username for login), and you need to provide more customization, such as defining how authentication work

AbstractBaseUser includes only: `password` `last_login`.

objects is the default manager that interacts with the database.
CustomManager allows you to customize how your model behaves in queries and user management.
You override objects to provide your custom logic for creating, filtering, and managing users

Create a custom user model in the app.
`accounts/models`

```py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.IntegerField(unique =True)
    age = models.IntegerField()
    gender = models.Choices(choices = (("Male","Male"),("Female","Female")))
    profile_picture = models.ImageField(upload_to="files/image/profile")
    # overwrite the main identifier from username to phone number
    USERNAME_FIELD = "phone_number"
    # add the required fields to the user
    REQUIRED_FIELDS = [age, gender]
```

`self.model(....)` is equivalent to `user = CustomUser(phone_number=phone_number, **extra_fields)`

#### Custom manager

CustomManager plays a key role in handling the logic for creating and managing users, especially when we are customizing Django's authentication system

By default, Django’s UserManager (the manager provided for the default user model) expects fields like username and email. But if we want to replace those fields with something else (like phone_number), we need a custom manager to handle the creation process accordingly.

Django expects certain methods to exist in the manager for the user model, especially when dealing with authentication. These methods include:

` create_user()`: Responsible for creating a regular user.
`create_superuser()`: Responsible for creating an admin/superuser.

default custom user.

```PY
def create_user(self, username, email=None, password=None, **extra_fields):
    user = self.model(username=username, email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

```

Since we’ve changed the default behavior (e.g., using phone_number instead of username), we need to customize these methods accordingly. Django’s built-in UserManager won’t work for our new user model, as it expects certain fields like username to exist. By creating CustomManager, we can override this behavior and define our own rules for user creation.

Create a manager app to let the django know that we have changed or customized the default behavior of user model.
inside `manager.py`, we will override two default methods, the `create_user` and `create_superuser`.

```py
from django.contrib.auth.base_user import BaseUserManager
class CustomManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("phone number must be present to create a user")
        user = self.model(phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("is_staff should be set to True")

        if extra_fields.get("is_active") is not True:
            raise ValueError("is_active should be set to True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser should be set to True")

        return self.create_user(phone_number, password, **extra_fields)
```

##### Attaching the manager to a model

Django's AbstractUser uses the default UserManager by default, but when we create a custom user model (like CustomUser), we need to specify a manager that understands how to create and handle this new model. That’s what CustomManager does—it knows how to create and manage instances of our CustomUser model with the customized fields and logic we’ve defined.

We attach the custom manager to a model by defining it as an attribute of the model class,

```py
class CustomUser(AbstractUser):
    # Fields here
    objects = CustomManager()  # Attach the custom manager here

```

When we define `objects = CustomManager()`, Django automatically sets ` self.model` within the `CustomManager` to refer to the CustomUser model.

## One last step

We have to specify that which model are using to custom user instead of `auth.user`.
By setting `AUTH_USER_MODEL`, we instruct Django to use accounts.CustomUser as the user model instead of the default.

`project_name/settings.py`

```py
# settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'
```

Now, run the following command

```shell
python manage.py createsuperuser
```

If it asked for `phone number` and required fields, it means we have successfully created a custom user.

`Overwrite`: Replaces the content in memory or storage.
`Override`: Replaces the behavior of a method in OOP when subclassing.
