# Signals

signals allow us to trigger certain actions automatically when specific events occur in our application.

They are a way of "listening" for certain system actions (like saving a model or finishing a user registration) and responding to them by executing custom logic. Signals are useful for decoupling various parts of our code, meaning one part can be notified of certain events in another part without direct connections.

### Common use cases

`Post-save actions`: Automatically perform an action after saving an object (e.g., sending a confirmation email after user registration).

`Pre-save actions`: Modify or validate data before it is saved to the database (e.g., generating a slug from a title before saving a blog post).

`Logging`: Log actions like user login, logout, or data changes.

`Notifications`: Send real-time notifications (like emails, SMS, etc.) when certain actions occur.

`Post-delete actions`: Clean up related data after an object is deleted (e.g., deleting files related to a deleted object).

### Example

Let's say we are having a blog post model defined in our `models.py`

`/models.py`

```py
# models.py
from django.db import models
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
```

Here, we are using a `pre_save` signal, whenever a BlogPost object is created, we check if the title is slugyfied, if not, we will do it using given function with the help of signals.

`./views.py`

```py
#views.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import BlogPost
@receiver(pre_save, sender=BlogPost)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
```

### How it works:

When the `@receiver(pre_save, sender=BlogPost)` decorator is applied, it registers the generate_slug function to be triggered whenever the pre_save signal is emitted for a BlogPost instance

Automatic triggering:

Each time we save a BlogPost instance (e.g., when we call `blog_post.save()` in our code), the pre_save signal is automatically emitted by Django before the actual save operation happens.

Django looks for any functions that are registered to listen to the pre_save signal for the BlogPost model and automatically calls them (in this case, generate_slug).

### Parameters:

#### sender:

This is the model class that sends the signal. In our case, the sender is the BlogPost model. It tells the signal which model instance triggered the signal.

#### instance:

This is the specific instance of the model that is about to be saved. In our example, it refers to the BlogPost object that is being saved. we can access the instance's attributes (e.g., instance.title, instance.slug) and modify them, as done in generate_slug.

#### kwargs:

kwargs stands for keyword arguments, which contains additional information about the signal. Common arguments passed in kwargs include:

`created`: A boolean indicating whether a new record is being created.
`raw`: A boolean indicating whether the model is being saved in raw format (used when loading data via fixtures).
`update_fields`: A list of fields that are being updated in the model. In this case, we’re not using kwargs directly, but it’s provided to give flexibility for additional information.

## aggregate()

aggregate() calculates values for the entire `queryset` and returns a dictionary of those calculated values.

```py
from django.db.models import Sum
total_price = Course.objects.aggregate(Sum('price'))
print(total_price)  # Output: {'price__sum': 4500.00} (sum of all course prices)

```

This query returns a dictionary where the key is the name of the operation (e.g., 'price\_\_sum') and the value is the result of the calculation.

## Annotate

annotate() computes values for each item in the queryset, adding the result as an additional field to each object.

It is used when you want to perform calculations per item (or group) and add the result as a field in each instance of the queryset.

```py
from django.db.models import Count

courses = Course.objects.annotate(lesson_count=Count('lessons'))
for course in courses:
    print(course.title, course.lesson_count)

```

aggregate(): Operates on the entire queryset and returns a summary result.
annotate(): Adds calculated fields to individual objects in the queryset
