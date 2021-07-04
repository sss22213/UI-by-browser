"""workspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from apps.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('detect', detect),
    path('temperature', read_temperature, name = 'temperature'),
    path('mqtt_switch', mqtt_switch),
    path('network', network),
    path('system_time', system_time, name = 'system_time'),
    path('system_info', system_info, name = 'system_info'),
    path('support_feature', support_feature, name = 'support_feature'),
    path('network_scan_result', network_scan_result, name = 'network_scan_result'),
    path('live/', livefe, name = 'livefe'),
]
