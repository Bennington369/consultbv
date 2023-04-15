

from datetime import timezone
from distutils.command.upload import upload
from unicodedata import decimal
from django.db import models
from django.db.models import Transform
from django.db.models import CharField
from django.contrib.auth.models import User
# Create your models here.

class UpperCase(Transform):
     lookup_name = 'upper'
     function = 'UPPER'
     bilateral = True

CharField.register_lookup(UpperCase)

class Categoria(models.Model):
     nombre = models.CharField(max_length= 50)
     create= models.DateField(auto_now_add=True)
#     producto = models.BooleanField(default=False)

     def __str__(self):
          return self.nombre




def get_default_my_hour():
     hour = timezone.now()
     formatedHour = hour.strftime("%H:%M:%S")
     return formatedHour

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    create= models.DateField(auto_now_add=True)

    def __str__(self):
          return self.nombre





class Perfil(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, related_name='perfiles')
    categoria = models.ForeignKey(Categoria,on_delete=models.PROTECT)
#   coments = models.ForeignKey(Comentario, on_delete=models.CASCADE)  
    nomEstable = models.CharField(max_length= 50,null=False,blank=False)
    descripcion_Estable = models.CharField(max_length= 250,null=False,blank=False)
    sitio_web = models.CharField(max_length= 200,null=True,blank=True,default='')
    twitter = models.CharField(max_length= 200,null=True,blank=True,default='')
    instagram = models.CharField(max_length= 200,null=True,blank=True,default='')
    facebook = models.CharField(max_length= 200,null=True,blank=True,default='')
    correo_tienda = models.CharField(max_length= 200,null=True,blank=True,default='')
    likes= models.ManyToManyField(User, blank=True, related_name='likes') 
    dislikes= models.ManyToManyField(User, blank=True, related_name='dislikes') 
    latitud = models.CharField(max_length=25,null=False,blank=False)
    longitud = models.CharField(max_length=25,null=False,blank=False)
    colonia = models.CharField(max_length= 50,null=True,blank=True)
    telefono = models.CharField(max_length= 10,null=True,blank=True,default='')
    whatsapp= models.CharField(max_length= 10, null=True,blank=True,default='')
    imagen_predeterminada = models.ImageField(upload_to='perfiles', default='perfiles/shop.png')
    imagen= models.ImageField(upload_to="perfiles",null=True,blank=True)
    lunes_entrada= models.CharField(max_length= 10,null=True,blank=True)
    lunes_salida= models.CharField(max_length= 10,null=True,blank=True)
    every_allday=models.CharField(max_length=2,null=True,blank=True)
    martes_entrada= models.CharField(max_length= 10,null=True,blank=True)
    martes_salida= models.CharField(max_length= 10,null=True,blank=True)
    miercoles_entrada= models.CharField(max_length= 10,null=True,blank=True)
    miercoles_salida= models.CharField(max_length= 10,null=True,blank=True)
    jueves_entrada= models.CharField(max_length= 10,null=True,blank=True)
    jueves_salida= models.CharField(max_length= 10,null=True,blank=True)
    viernes_entrada= models.CharField(max_length= 10,null=True,blank=True)
    viernes_salida= models.CharField(max_length= 10,null=True,blank=True)
    sabado_entrada= models.CharField(max_length= 10,null=True,blank=True)
    sabado_salida= models.CharField(max_length= 10,null=True,blank=True)
    domingo_entrada= models.CharField(max_length= 10,null=True,blank=True)
    domingo_salida= models.CharField(max_length= 10,null=True,blank=True)                        
    validate= models.BooleanField(default=False)
    recomendado= models.BooleanField(default=False)
    visit_count = models.PositiveIntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)
    recomendado2= models.BooleanField(default=False)
    vistos= models.ManyToManyField(User, blank=True, related_name='visitados')
    update = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, blank=True)
   

    def nombre(self):
         return "{} - {} - {}".format(self.nomEstable,self.telefono,self.recomendado)
     
    def __str__(self):
         return self.nombre()
    
    def save(self, *args, **kwargs):
         # Si el usuario ha subido una imagen para el producto, sobrescribe la imagen predeterminada
         if self.imagen:
             self.imagen_predeterminada = self.imagen
         super(Perfil, self).save(*args, **kwargs)
    

class Comentario(models.Model):
     autor = models.ForeignKey(User,on_delete=models.CASCADE)
     negocio =models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='comentarios')
     body= models.TextField(blank=True,null=True)
     create = models.DateTimeField(auto_now_add=True)
     update = models.DateTimeField(auto_now_add=True)
     validate= models.BooleanField(default=False)         
     likes= models.ManyToManyField(User, blank=True, related_name='likes_comentario')
     parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE) 

     
     def __str__(self):
          return self.comen() 


     def comen(self):
         return "{} - {}".format(self.body,self.autor)
     
     
     def num_respuestas(self):
          return self.replies.count()



class Post(models.Model):
     autor = models.ForeignKey(User,on_delete=models.CASCADE)
     perfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
     body= models.TextField()
     create = models.DateTimeField(auto_now_add=True)
     update = models.DateTimeField(auto_now_add=True)
     validate= models.BooleanField(default=False)   
     imagen= models.ImageField(upload_to="publicaciones",null=True,blank=True)
     likes= models.ManyToManyField(User, blank=True, related_name='likes_post') 


     def __str__(self):
          return self.body
     

class Resenias(models.Model):
     autor = models.ForeignKey(User,on_delete=models.CASCADE)
     negocio =models.ForeignKey(Perfil,on_delete=models.CASCADE)
     body= models.TextField(blank=False,null=False)
     create = models.DateTimeField(auto_now_add=True)
     validate= models.BooleanField(default=False)
     estrellas= models.IntegerField(blank=False,null=False,default=0)       
     likes= models.ManyToManyField(User, blank=True, related_name='likes_resenia') 
     update = models.DateTimeField(auto_now_add=True)


     def rese(self):
         return "{} - {}".format(self.body,self.estrellas)

     def __str__(self):
          return self.rese()     
      

class Articulo(models.Model):
    autor = models.ForeignKey(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    perfil =models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='articulos')
    descripcion = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_predeterminada = models.ImageField(upload_to='articulos', default='perfiles/shop.png')
    imagen = models.ImageField(upload_to='articulos', blank=True, null=True)
    create= models.DateField(auto_now_add=True)

    def __str__(self):
          return self.nombre

    def save(self, *args, **kwargs):
         # Si el usuario ha subido una imagen para el producto, sobrescribe la imagen predeterminada
         if self.imagen:
             self.imagen_predeterminada = self.imagen
         super(Articulo, self).save(*args, **kwargs)


class Notificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userfrom')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userto')
    message = models.CharField(max_length=255,blank=True,null=True)
    url = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)