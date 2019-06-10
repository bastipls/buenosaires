from datetime import datetime

from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=50)
    n_tarjeta = models.IntegerField(null=True,blank=False)


@receiver(post_save, sender=User)
def create_user_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_usuario(sender, instance, **kwargs):
    instance.usuario.save()

class Producto(models.Model):
    nombre = models.CharField(max_length=40)
    imagen = models.ImageField(upload_to='producto/%Y/%m/%d', blank=True,default='static/img/default-img.jpg')
    medidas = models.CharField(max_length=50)
    marca = models.CharField(max_length=20,blank=True,null=True,default='Desconocida')
    peso = models.PositiveIntegerField(blank=True,null=True)
    stock = models.PositiveIntegerField()
    precio = models.IntegerField()
    disponibilidad = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True,null=True)
    class Meta:
        ordering = ('nombre',)
    def __str__(self):
        return self.nombre
class Solicitud(models.Model):
    estado = (('Sin revisar','Sin revisar'),
              ('Aprobada','Aporbada'),
              ('Rechazada','Rechazada'))
    fecha_emision = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(User,on_delete=models.CASCADE)
    hora_llegada = models.TimeField()
    fecha_llegada = models.DateField()
    tipo = models.CharField(max_length=20)
    estado = models.CharField(max_length=20,choices=estado,default='Sin revisar',null=True,blank=True)
    descripcion = models.TextField()

    def __int__(self):
        return self.id

  
class Orden(models.Model):
    cliente = models.ForeignKey(User,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,null=True,blank=True)
    estado = (('Espera','Espera'),
              ('Enviada','Enviada'))

    fecha_emision = models.DateField(default=timezone.now)
    estado = models.CharField(choices=estado,default='Espera',max_length=20)
    fecha_llegada = models.DateField(blank=True,null=True)
    def __int__(self):
        return self.id

class Producto_proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=50,null=True,blank=True)
    nombre = models.CharField(max_length=40)
    medidas = models.CharField(max_length=50)
    marca = models.CharField(max_length=20,default='Desconocida',null=True,blank=True)
    peso = models.PositiveIntegerField(null=True,blank=True)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField()
    disponibilidad = models.BooleanField()
    descripcion = models.TextField()
    
    class Meta:
        ordering = ('nombre',)
    def __str__(self):
        return self.nombre
