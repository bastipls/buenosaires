from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import request
from django.urls import reverse
from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role
from rolepermissions.utils import user_is_authenticated
from django.utils import timezone
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
                pass
            else:
                producto.marca = request.POST.get('txtmarca') 
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
                print(request.FILES.get('txtimagen'))
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
        except:
            alert = 'roja' 
            messages.error(request,'No se a podido enviar ')
        solicitud.save()
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
    variables = {'ordenes':ordenes}

    return render(request,'buenosaires/solicitudes.html',variables)


def enviar_producto(request,id):
    orden = get_object_or_404(Orden,id=id)
    act = Orden.objects.filter(id=id)
    act.update(fecha_llegada=timezone.now() + timezone.timedelta(days=1))
    act.update(estado='Enviada')
    return redirect('lista_solicitudes')
@user_passes_test(lambda u:u.is_staff, login_url=('login'))  
def detalle_solicitudes(request):##esto es para solicitudes no orden
    pass

def stock_proveedores(request):#web servies
    pass
###FALTA INTERFAZ VER CLIENTES MODIFICO INTERFAZ DE ADMIN
#MODIFICAR PRODUCTOS
