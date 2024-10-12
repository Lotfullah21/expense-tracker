from .views import index, removeTransaction
from django.urls import path

urlpatterns = [
     path("",index,name="index"),
     path("remove/<int:id>/",removeTransaction,name="removeTransaction")
]
