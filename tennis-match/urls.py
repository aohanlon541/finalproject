from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("match/<int:match_id>", views.get_match, name="match"),
    path("message/<int:match_id>", views.message, name="message"),
]
