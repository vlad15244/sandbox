"""
URL configuration for ajax project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from visu import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name = 'index'),  
    path('ajax_ex/', views.MyView.as_view(), name = 'ajax_ex'),
    path('ajax_ex_plus/', views.ajax_ex_plus, name = 'ajax_ex_plus'),
    path('ajax_ex_minus/', views.ajax_ex_minus, name = 'ajax_ex_plus'),
    path('ajax_runtime/', views.Runtime.as_view(), name = 'ajax_runtime'),                    
]
