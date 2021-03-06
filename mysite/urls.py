"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from buenosaires import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('apiproveedores/',views.stock_proveedores.as_view()),
    path('',include('buenosaires.urls')),
    path('', include('pwa.urls')),
    
]
#Personalizzar titulos admin
admin.site.site_header = "Administracion Buenos Aires"
admin.site.index_title = "Buenos Aires"
admin.site.site_title = "Administracion"
