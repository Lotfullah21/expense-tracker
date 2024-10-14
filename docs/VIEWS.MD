## VIEWS

view is a Python function or class that handles a web request and returns a web response (like rendering a template or redirecting to another page).

##### Why adding `redirect` is crucial?

```py
def index(request):
    if request.method=="POST":
        amount = request.POST.get("amount")
        remarks = request.POST.get("description")
        new_track = TrackingExpenses(amount=amount, description=remarks)
        print(remarks, amount)
        return redirect("/")
```

If there's no `redirect("/")`, the code execution will continue to the return render(request, "index.html", context={}) part. This will render the template again with a blank form.

`new_track.amount` is still being treated as a string is because the form data received through request.POST (which includes amount) is always a string, even if the input type in your form is number

```py

def index(request):
    if request.method=="POST":
        amount = request.POST.get("amount")
        remarks = request.POST.get("description")
        current_balance,_ = CurrentBalance.objects.get_or_create(id=1)
        expense_type ="CREDIT"
        if float(amount)<0:
            expense_type="DEBIT"

        new_track = TrackingExpenses(current_balance=current_balance,amount=amount, description=remarks, expense_type = expense_type)
        new_track.save()
        current_balance.current_balance = current_balance.current_balance + float(new_track.amount)
        current_balance.save()
        return redirect("/")
    return render(request, "index.html", context={})
```

`Why Use _?`

get_or_create() returns a tuple with two values:

The first value (current_balance) is the instance of CurrentBalance that was either retrieved or created.
The second value is a boolean (True or False) indicating whether the instance was created (True) or retrieved from the database (False).

`get_or_create()` only retrieves or creates the initial CurrentBalance record, but once we update `current_balance.current_balance`, we need to call `save()` to persist that update.

The `{% url %}` tag is a built-in Django template tag that generates a URL by reversing the name of a view (in this case, 'removeTransaction')

`reversing the name` means converting the name of a view into a URL path. Instead of hardcoding URLs in our templates,we use the `{% url %}` tag with the view's name, and Django automatically finds the corresponding URL pattern from our urls.py file

## How it works

#### 1. Define a URL pattern

```py
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('remove/<int:id>/', views.removeTransaction, name='removeTransaction'),
]

```

#### 2. Create a delete link

Using `{%url%}`, we generate a link for every transaction and pass the id as second parameter.
the id will be captured automatically by url pattern.

#### 3. User clicks on delete button link

When a user clicks on the button, the browser makes a get request to the generated URL, for instance if id is 3, the request will be made to `/remove/3`.

#### 4. Django's URL dispatcher

Django receives the request and uses its `URL` dispatcher to match the incoming `URL` against the defined pattern in `urls.py`.
It finds the `remove/<int:id>/` pattern, extracts the id parameter (in this case, 3), and determines which view to call.

#### 5. Calling the view function

Django calls the `removeTransaction` view function passing the extracted `id` as its parameter.

```py
# views.py
def removeTransaction(request, id):
    transaction = get_object_or_404(TrackingExpenses, id=id)
    transaction.delete()
    messages.success(request, "Transaction deleted successfully.")
    return redirect("/")
```
