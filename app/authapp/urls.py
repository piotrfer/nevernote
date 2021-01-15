from django.urls import path
from . import views as v

urlpatterns = [
    path('register/', v.register, name="register"),
    path('login/', v.login, name="login"),
    path('logout/', v.logout, name="logout"),
]
