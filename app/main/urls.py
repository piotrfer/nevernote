from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.landing, name="landing-page"),
    path('home/', views.index, name="home"),
    path('me/', views.profile, name="my-profile"),
    path( "favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
]
