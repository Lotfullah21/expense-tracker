from .views import index, removeTransaction, login_view, register_view, logout_view, contact
from django.urls import path

urlpatterns = [
     path("",index,name="index"),
     path("remove/<int:id>/",removeTransaction,name="removeTransaction"),
     path("login/",login_view, name="login_view"),
     path("register/", register_view, name="register_view"),
     path("contact/", contact, name="contact_view"),
     path("logout/", logout_view, name="logout_view")
]
