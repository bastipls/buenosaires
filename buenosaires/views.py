from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import request
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role
from rolepermissions.utils import user_is_authenticated

from buenosaires.models import (Orden, Producto, Producto_proveedor, Solicitud,
                                Usuario)
from mysite.roles import Cliente

from .serializers import Producto_proveedorSerializador


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['txtuser'].lower()
        password = request.POST['txtpass']
        user = authenticate(request,username = username, password=password)
        if user:
            login(request,user)
            
            return HttpResponseRedirect(reverse('inicio'))
        else:
            messages.error(request,'Credenciales incorrectas')

            return render(request, 'buenosaires/login.html',context)
    else:
        return render(request,'buenosaires/login.html',context) 
@login_required(login_url='login')
def logout_view(request):
  
    if request.method == 'POST':
        logout(request)
    return redirect('inicio')


def registro(request):
    user = User()   
   
    if request.method == 'POST':
  
        
        user = User.objects.create_user(username=request.POST.get('txtemail'),password=request.POST.get('txtpass'))
        user.email = request.POST.get('txtemail')
        user.first_name = request.POST.get('txtnombre')
        user.last_name = request.POST.get('txtapellido')
        user.usuario.direccion = request.POST.get('txtdireccion')
        user.usuario.n_tarjeta = request.POST.get('txttarjeta')
        assign_role(user, 'cliente')
        user.save()
        return HttpResponseRedirect(reverse('inicio'))

    variables = {}
    return render(request,'buenosaires/register.html',variables)

def inicio(request):
    if request.user.is_authenticated:
        
        print(request.user.pk)
    variables = {}
    return render(request,'buenosaires/about.html',variables)
@user_passes_test(lambda u:u.is_staff, login_url=('login'))
def crear_producto(request):
    producto = Producto()
    alert = 'verde' 
    if request.method == 'POST':
        
        producto.nombre = request.POST.get('txtnombre')
        producto.imagen = request.FILES.get('txtimagen')
        producto.medidas = request.POST.get('txtmedidas')
        producto.stock = int(request.POST.get('txtstock'))
       
        if len(request.POST.get('txtmarca')) == 0:
            pass
        else:
            producto.marca = request.POST.get('txtmarca')  

        producto.peso = int(request.POST.get('txtpeso'))
        producto.precio = int(request.POST.get('txtprecio'))
        producto.descripcion = request.POST.get('txtdescripcion')  
        
        try:
            producto.save()
            messages.success(request,"Producto creado con exito")
        except:
            alert ='roja'
            messages.error(request,"No se pudo crear el producto")
    variables = {'alert':alert}
    return render(request,'buenosaires/crear_producto.html',variables)
   
def productos(request):
    
    if request.user.is_staff:
        productos = Producto.objects.all()
    else:
        productos = Producto.objects.filter(stock__gt=0)
    variables = {'productos':productos}
    return render(request,'buenosaires/productos.html',variables)
@user_passes_test(lambda u:u.is_authenticated, login_url=('registro'))  
def detalle_producto(request,id):#falta se crea orden y se resta stock
    # producto = Producto.objects.get(id=id)
    producto   = get_object_or_404(Producto,id=id)
    orden = Orden()
    pro = Producto()
    
    alert = 'verde' 
    if request.user.is_staff:
        if request.method == 'POST':
            pro.id = request.POST.get('txtid')
            pro.nombre = request.POST.get('txtnombre')
            if request.FILES.get('txtimagen') is None:
                pro.imagen = producto.imagen
            else:
                pro.imagen = request.FILES.get('txtimagen')
            
            pro.medidas = request.POST.get('txtmedidas')
            if len(request.POST.get('txtmarca')) == 0:
                
                print("POR AUI PASE XD")
            else:
                pro.marca = request.POST.get('txtmarca') 
               
            pro.peso = int(request.POST.get('txtpeso'))
            if request.POST.get('txtdisponibilidad') == 'Disponbile':
                pro.disponibilidad = True
            elif request.POST.get('txtdisponibilidad') =='No disponible':
                pro.disponibilidad = False
            
            pro.descripcion = request.POST.get('txtdescripcion')
            pro.precio = int(request.POST.get('txtprecio'))
            pro.stock =  request.POST.get('txtstock')
      
            try:
                alert = 'verde' 
                pro.save()
                print(request.POST.get('txtmarca'))
                messages.success(request,'Producto actualizado con exito')
                return redirect('detalle_producto',id=producto.id)
                
            except Exception as e:
                print('ERRRORR')
                print(type(e))
                alert = 'roja'
            
                messages.error(request,'No se pudo actualizar el producto')
               
    else:
        if request.method == 'POST':
            pro.id = request.POST.get('txtid')
            pro.nombre = producto.nombre
            pro.imagen = producto.imagen
            pro.medidas = producto.medidas
            pro.marca = producto.marca
            pro.peso = producto.peso
            pro.disponibilidad = producto.disponibilidad
            pro.descripcion = producto.descripcion
            pro.precio = producto.precio
            pro.stock =  (producto.stock - int(request.POST.get('txtstock')))
            orden.cliente = request.user
            orden.producto = producto
            try:
                orden.save()
                pro.save()
                messages.success(request,'Pedido realizado con exito')
            except:
                alert = 'roja' 
                messages.error(request,'No se pudo realizar el pedido')
        ###FALTA CREAR LA ORDEN AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    variables = {'producto':producto,
                'alert':alert}
    return render(request,'buenosaires/detalle_producto.html',variables)
@user_passes_test(lambda u:u.is_staff, login_url=('inicio'))  
def eliminar_producto(request,id):
    producto = get_object_or_404(Producto,id=id)
    producto.delete()

    return redirect('productos')
@login_required(login_url='login')
def solocitar_mantencion(request):
    solicitud = Solicitud()
   
    alert = 'verde' 
    if request.method == 'POST':

        solicitud.cliente = request.user
        solicitud.hora_llegada = request.POST.get('txthora')
        solicitud.fecha_llegada = request.POST.get('txtfecha')
        solicitud.tipo = request.POST.get('txttipo')
        solicitud.descripcion = request.POST.get('txtdescripcion')
        try:
            messages.success(request,'Solicitud enviada')
            solicitud.save()
        except:
            alert = 'roja' 
            messages.error(request,'No se a podido enviar ')
        
    variables = {'alert':alert}
    return render(request,'buenosaires/solicitar_mantencion.html',variables)
@login_required(login_url='login')
def lista_solicitudes(request):#faltar probar si funciona aun no lo veo equisde
    user = User.objects.get(id=request.user.pk)
    ##Me fatlaria filtar por solicitudes mostrar las dos a la vez ordenes y solic
    if has_role(user,[Cliente]):
        ordenes = Orden.objects.filter(cliente=request.user.pk)
    elif request.user.is_staff or request.user.is_superuser:
        ordenes = Orden.objects.all()
    if has_role(user,[Cliente]):
        solicitudes = Solicitud.objects.filter(cliente=request.user.pk)
    elif request.user.is_staff or request.user.is_superuser:
        solicitudes = Solicitud.objects.all()
    variables = {'ordenes':ordenes,
                'solicitudes':solicitudes}

    return render(request,'buenosaires/solicitudes.html',variables)

@user_passes_test(lambda u:u.is_staff, login_url=('login'))  
def enviar_producto(request,id):
    act = Orden.objects.filter(id=id)
    act.update(fecha_llegada=timezone.now() + timezone.timedelta(days=3))
    act.update(estado='Enviada')
    return redirect('lista_solicitudes')
@user_passes_test(lambda u:u.is_staff, login_url=('login'))  
def aprobar_solicitud(request,id):##esto es para solicitudes no orden
    soli = Solicitud.objects.filter(id=id)
    soli.update(estado='Aprobada')
    return redirect('lista_solicitudes')
@user_passes_test(lambda u:u.is_staff, login_url=('login')) 
def rechazar_solicitud(request,id):##esto es para solicitudes no orden
    #Esto es otra foram de actualizar un objeto mas segura que la  de arriba xd
    solicitud = get_object_or_404(Solicitud,id=id)
    solicitud.estado = 'Rechazada'
    solicitud.save(update_fields=['estado'])
    
    return redirect('lista_solicitudes')

class stock_proveedores(APIView):#web servies
    def get(self,request):
        productos = Producto_proveedor.objects.all()
        serializador = Producto_proveedorSerializador(productos ,context={"request":request},many=True)
        return Response(serializador.data)
    def post(self,request):
        pass
