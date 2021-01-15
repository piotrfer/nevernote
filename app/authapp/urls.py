from django.urls import path
from . import views as v
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', v.register, name="register"),
    path('login/', v.login, name="login"),
    path('logout/', v.logout, name="logout"),
    path("password-reset", auth_views.PasswordResetView.as_view( template_name="passreset/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view( template_name="passreset/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="passreset/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view( template_name="passreset/password_reset_complete.html"), name="password_reset_complete")
]

