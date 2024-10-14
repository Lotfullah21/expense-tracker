```py
# to create a super user(admin)
python manage.py createsuperuser
```

```py
from django.contrib import admin
from expenses.models import *

admin.site.register(CurrentBalance)
admin.site.register(TrackingExpenses)
```

add a search for the following fields `expense_type","description`.

```py
search_fields = ["expense_type","description"]
ordering = ["-updated_at"]
```
