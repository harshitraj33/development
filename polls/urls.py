from django.urls import path
from . import views
from .views import form_view, home_view, login_view, signup_view
urlpatterns =[
    path("", views.index, name='index'),
    path("home/", views.home_view, name="home_view"),
    path("form/", form_view, name='form_view'),
    path("login/", login_view,name='login_view'),
    path("signup/", signup_view, name='signup_view'),
    
]