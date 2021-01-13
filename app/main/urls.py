from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing-page"),
    path('home/', views.index, name="home"),
    path('notes/', views.notes, name="notes-list"),
    path('me/', views.profile, name="my-profile"),
]
