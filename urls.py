"""
URL configuration for karunna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('signup/', views.signup),
    path('ngo-Home/', views.ngo_dashboard),
    path('volunteer-Home/', views.volunteer_dashboard),
    path('events/', views.events),
    path('register_event/', views.register_event),
    path('blog/', views.blog),
    path('index1/', views.index1),
    path('about/', views.about),
    path('contact/', views.contact),
    path('privacy/', views.privacy),
    path('greenstore/', views.greenstore),
    
]
