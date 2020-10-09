"""MovieStreaming URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views as auth_views
import admin.views as admin_views
import users.views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', auth_views.register, name='register'),
    path('movie/<str:id>/', users_views.movie, name='movie'),
    path('', users_views.home, name='home'),
    path('adminhome/',admin_views.adminhome,name='adminhome'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('comment/<str:id>/', users_views.comment, name='comment'),
    path('addmovies/', admin_views.addmovies, name='addmovies'),
    path('modifymovies/', admin_views.modifymovies, name='modifymovies'),
    path('updatemovie/<str:id>/', admin_views.updatemovie, name='updatemovie'),
    path('updatedone/<str:id>/', admin_views.updatedone, name='updatedone'),
    path('deletemovies/<str:id>/', admin_views.deletemovies, name='deletemovies'),
]
