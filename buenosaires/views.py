from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.urls import reverse
from rolepermissions.roles import assign_role
from rolepermissions.utils import user_is_authenticated

from buenosaires.models import Usuario


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
    pass
def detalle_producto(request):
    pass
def solocitar_mantencion(request):
    pass
def lsita_solicitudes(request):
    pass
