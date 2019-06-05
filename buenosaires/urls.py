from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/',views.registro,name ='registro'),
    path('login/',views.login_view, name = 'login'),
    path('logout/',views.logout_view,name='logout')
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)