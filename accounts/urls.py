from django.urls import path, include
from accounts.views import user


urlpatterns = [
     path("", user,name="user_view")
]
