from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=50)
    tipo = models.BooleanField(default=False)
    n_tarjeta = models.IntegerField()


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    instance.usuario.save()

class Producto(models.Model):
    nombre = models.CharField(max_length=40)
    imagen = models.ImageField(upload_to='producto/%Y/%m/%d', blank=True,default='static/img/default-img.jpg')
    medidas = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    precio = models.IntegerField()
    disponibilidad = models.BooleanField()
    descripcion = models.TextField()
    class Meta:
        ordering = ('nombre',)
    def __str__(self):
        return self.nombre

class Orden(models.Model):
    cliente = models.ForeignKey(User,on_delete=models.CASCADE)
    estado = (('Espera','Espera'),
              ('Enviada','Enviada'))
    fecha_emision = models.DateField(default=timezone.now)
    estado = models.CharField(choices=estado,default='Espera',max_length=20)
    fecha_llegada = models.DateField(blank=True,null=True)
    def __int__(self):
        return self.id

class Producto_proveedor(models.Model):
    nombre = models.CharField(max_length=40)
    medidas = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField()
    disponibilidad = models.BooleanField()
    descripcion = models.TextField()
    
    class Meta:
        ordering = ('nombre',)
    def __str__(self):
        return self.nombre