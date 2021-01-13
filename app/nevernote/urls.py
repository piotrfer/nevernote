from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('authapp.urls')),
    path('notes/', include('notes.urls'))
]
