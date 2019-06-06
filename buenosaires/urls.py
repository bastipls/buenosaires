from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/',views.registro,name ='registro'),
    path('login/',views.login_view, name = 'login'),
    path('logout/',views.logout_view,name='logout'),
    path('solicitudes/',views.lista_solicitudes,name='lista_solicitudes'),
    path('productos/',views.productos,name='productos'),
    path('productos/crear_productos/',views.crear_producto,name = 'çrear_producto'),
    path('productos/detalle_producto/<int:id>',views.detalle_producto, name='detalle_producto'),
    path('solicitar_mantencion/',views.solocitar_mantencion,name='solicitar_mantencion'),
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)