from .views import Login, register, index

from django.urls import include, path
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', index,name='index'),

    path('signup/', register, name='register'),
    path('login/', Login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(),{'next_page': 'index'}, name='logout'),

]