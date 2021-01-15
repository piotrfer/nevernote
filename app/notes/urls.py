from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes, name="notes-list"),
    path('create/', views.create_note, name="create-note"),
    path('<str:id>/show', views.show_note, name="show-note"),
    path('<str:id>/edit', views.edit_note, name="edit-note"),
    path('<str:id>/delete', views.delete_note, name="delete-note"),
]
