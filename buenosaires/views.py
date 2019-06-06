from builtins import object

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.urls import reverse
from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role
from rolepermissions.utils import user_is_authenticated

from buenosaires.models import Orden, Producto, Solicitud, Usuario
from mysite.roles import Cliente


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

def crear_producto(request):
    producto = Producto()
    alert = 'verde' 
    if request.method == 'POST':
        
        producto.nombre = request.POST.get('txtnombre')
        producto.imagen = request.FILES.get('txtimagen')
        producto.medidas = request.POST.get('txtmedidas')
        producto.stock = int(request.POST.get('txtstock'))
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
    
    productos = Producto.objects.all()
    variables = {'productos':productos}
    return render(request,'buenosaires/productos.html',variables)
def detalle_producto(request,id):
    producto = Producto.objects.get(id=id)
    variables = {'producto':producto}


    return render(request,'buenosaires/detalle_producto.html',variables)
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
        except:
            alert = 'roja' 
            messages.error(request,'No se a podido enviar ')
        solicitud.save()
    variables = {'alert':alert}
    return render(request,'buenosaires/solicitar_mantencion.html',variables)
def lista_solicitudes(request):
    user = User.objects.get(id=request.user.pk)
    if has_role(user,[Cliente]):
        ordenes = Orden.objects.filter(cliente=request.user.pk)
    elif request.user.is_staff() or request.user.is_superuser():
        ordenes = Orden.objects.all()
    variables = {}

    return render(request,'buenosaires/solicitudes.html',variables)
