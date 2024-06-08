from django.urls import path
from base import views

urlpatterns = [
    path('', views.index, name="index_view"),

    # login Process
    path('login', views.login_view, name="login_view"),
    path('signup', views.signup_view, name="signup_view"),
    path('logout', views.logout_view, name='logout_view')

]

