
from this import d
from django.db.models import Avg,Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from requests import request
from aplicacion.forms import UsuarioNuevo
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from perfil.models import Categoria,Perfil,Comentario,Resenias,Post,Producto,Articulo,Notificacion
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from .badwords import BAD_WORDS
from django.urls import reverse
import re
from django.utils import timezone
from django.views.decorators.http import require_POST
# Create your views here.

def create_notification(user, user_to,message,url):
    notification = Notificacion(user=user, user_to=user_to, message=message,url=url)
    notification.save()

def index(request):
    perfiles=Perfil.objects.filter(recomendado=True)
    return render(request,'index.html',{"perfiles":perfiles})

def admin(request):
    perfil = Perfil.objects.all().order_by('-create')
    comentario = Comentario.objects.all().order_by('-create')
    resenia = Resenias.objects.all().order_by('-create')
    articulo = Articulo.objects.all().order_by('-create')
    producto = Producto.objects.all().order_by('-create')
    post = Post.objects.all().order_by('-create')
    categoria = Categoria.objects.all().order_by('-create')
    return render(request,'registration/admin.html',{"perfil":perfil,'comentario':comentario,'resenia':resenia,'articulo':articulo,'producto':producto,'post':post,'categoria':categoria})



def mapa(request):
    return render(request,'web/mapa.html')

#QUEDA PENDIENTE PARA MOSTRARLO EN EL MAPA
# def obtener_perfiles(request):
#     negocios = Perfil.objects.all()
#     json_negocios = serializers.serialize('json', negocios)
#     return JsonResponse(json_negocios, safe=False)

def categoria(request):
    cate= Categoria.objects.all().order_by('nombre')
    perfiles =Perfil.objects.all()
#    taq= Categoria.objects.get()
    return render(request,'web/categorias.html',{"cate":cate,'perfiles':perfiles})


def contacto(request):
    return render(request,'web/contacto.html')

class VRegistro(View):
    def get(self, request):
       form = UsuarioNuevo()
       return render(request,'web/registro.html',{"form":form})
    
    def post(self, request):
        form = UsuarioNuevo(request.POST)
        if form.is_valid():
            usuario=form.save()
            login(request,usuario)
            return redirect('inicio')

        else:
            for msg in form.error_messages:
                messages.error(request,form.error_messages[msg])
            
            return render(request,'web/registro.html',{"form":form})
            
def cerrar_sesion(request):
    logout(request)
    return render(request,"index.html")


def logear(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario_ingreso = authenticate(username=nombre, password=contra)
            if usuario_ingreso is not None:
                login(request, usuario_ingreso)
                # Si hay una url guardada en la cookie, redirige al usuario a esa url.
                url_redireccion = request.COOKIES.get('url_redireccion', '')
                if url_redireccion:
                    response = redirect(url_redireccion)
                    response.delete_cookie('url_redireccion')
                    return response
                else:
                    return redirect('inicio')
            else:
                messages.error(request, "Usuario o contraseña no correcto")
        else:
            messages.error(request, "Usuario o contraseña no correcto")

    # Guarda la url actual en una cookie antes de redirigir al usuario a la página de inicio de sesión
    url_redireccion = request.META.get('HTTP_REFERER')
    response = render(request, 'registration/login.html', {'form': AuthenticationForm()})
    if url_redireccion:
        response.set_cookie('url_redireccion', url_redireccion)
    return response


def muestraperfil(request,id,nom):
    
    if Perfil.objects.filter(id=id,nomEstable=nom).exists():    
        perfil=Perfil.objects.get(id=id)
        perfil2=Perfil.objects.get(id=id).nomEstable
        word= BAD_WORDS

        found=False

        for bad_word in BAD_WORDS:
            pattern = re.compile(bad_word, re.IGNORECASE)
            if pattern.search(perfil2):
                perfil2 = pattern.sub('*' * len(bad_word), perfil2)
                found=True
        
        if found:
            perfil2
        else:
            perfil2=''
           

        tiene_like=request.user in perfil.likes.all()        
        res= Resenias.objects.filter(negocio=perfil).order_by('-create')
        promedio_estrellas = Resenias.objects.filter(negocio=perfil).aggregate(Avg('estrellas'))['estrellas__avg']

        perfil.visit_count += 1
        perfil.save()



        if perfil.lunes_entrada and perfil.lunes_entrada.strip() and perfil.lunes_salida and perfil.lunes_salida.strip():
            perfil.lunes_entrada = datetime.strptime(perfil.lunes_entrada, "%H:%M")
            perfil.lunes_salida = datetime.strptime(perfil.lunes_salida, "%H:%M")

        if perfil.martes_entrada and perfil.martes_entrada.strip() and perfil.martes_salida and perfil.martes_salida.strip():
            perfil.martes_entrada = datetime.strptime(perfil.martes_entrada, "%H:%M")
            perfil.martes_salida = datetime.strptime(perfil.martes_salida, "%H:%M")

        if perfil.miercoles_entrada and perfil.miercoles_entrada.strip() and perfil.miercoles_salida and perfil.miercoles_salida.strip():
            perfil.miercoles_entrada = datetime.strptime(perfil.miercoles_entrada, "%H:%M")
            perfil.miercoles_salida = datetime.strptime(perfil.miercoles_salida, "%H:%M")

        if perfil.jueves_entrada and perfil.jueves_entrada.strip() and perfil.jueves_salida and perfil.jueves_salida.strip():
            perfil.jueves_entrada = datetime.strptime(perfil.jueves_entrada, "%H:%M")
            perfil.jueves_salida = datetime.strptime(perfil.jueves_salida, "%H:%M")

        if perfil.viernes_entrada and perfil.viernes_entrada.strip() and perfil.viernes_salida and perfil.viernes_salida.strip():
            perfil.viernes_entrada = datetime.strptime(perfil.viernes_entrada, "%H:%M")
            perfil.viernes_salida = datetime.strptime(perfil.viernes_salida, "%H:%M")

        if perfil.sabado_entrada and perfil.sabado_entrada.strip() and perfil.sabado_salida and perfil.sabado_salida.strip():
            perfil.sabado_entrada = datetime.strptime(perfil.sabado_entrada, "%H:%M")
            perfil.sabado_salida = datetime.strptime(perfil.sabado_salida, "%H:%M")

        if perfil.domingo_entrada and perfil.domingo_entrada.strip() and perfil.domingo_salida and perfil.domingo_salida.strip():
            perfil.domingo_entrada = datetime.strptime(perfil.domingo_entrada, "%H:%M")
            perfil.domingo_salida = datetime.strptime(perfil.domingo_salida, "%H:%M")            

        if request.user.is_authenticated:
            perfil.vistos.add(request.user)

        if promedio_estrellas is not None:
            promedio_estrellas = round(promedio_estrellas, 1)

        
        com= Comentario.objects.filter(negocio=perfil).order_by('-create')[:10]
        come= Comentario.objects.filter(negocio=perfil)
        art= Articulo.objects.filter(perfil=perfil)
        pub= Post.objects.filter(perfil=perfil)
         
        resenia= Resenias()

        
        rese = None
        if request.user.is_authenticated:
            rese = Resenias.objects.filter(negocio=perfil, autor=request.user).first()

        if request.method == 'POST':
            resenia.negocio = Perfil.objects.get(pk=request.POST['perfilxdd'])
            resenia.autor = User.objects.get(pk=request.POST['userxd'])
            resenia.body = request.POST['body']
            estrellas = request.POST.get('rating') # Usamos get en lugar de index para evitar una excepción KeyError
            if estrellas:
                resenia.estrellas = estrellas
                resenia.save()
                create_notification(request.user,resenia.negocio.usuario, f'{request.user.username} hizo una reseña a tu perfil "{perfil.nomEstable}"', f'/muestraperfil/{perfil.id}/{perfil.nomEstable}')
  
                return redirect(request.path_info)
         
           
        return render(request,"web/perfil_description.html",{"per":perfil,"res":res,"com":com,"come":come,"pub":pub,"tiene_like":tiene_like,"promedio_estrellas": promedio_estrellas,'perfil2':perfil2,'word':word,'rese':rese,'art':art})



	

def busqueda(request):
    tiendas = Perfil.objects.all()
    busc = request.GET.get('prd').upper()

    if busc != '' and busc is not None:
        
        tiendas = tiendas.filter(
            Q(nomEstable__upper__contains=busc) |
            Q(telefono__icontains=busc) |
            Q(categoria__nombre__upper__icontains=busc)|
            Q(productos__nombre__upper__icontains=busc)|
            Q(colonia__upper__icontains=busc)
   
        )

        
        return render(request, "web/busqueda.html", {"tiendas": tiendas, "query": busc})
    else:
        mensaje = "No has introducido nada"  
    
    return render(request, 'web/busqueda.html', {"mensaje": mensaje})

@login_required
def inicioxd(request):
     perfiles= Perfil.objects.all().filter(usuario_id=request.user).order_by('-update')
     return render(request,"inicio.html",{"perfiles":perfiles})

def borrar(request, id):
	perfil = Perfil.objects.get(id=id)
	return render(request, 'web/borrar.html', {'perfil':perfil })

def borrando(request, id):
	perfil = Perfil.objects.get(id=id)
	perfil.delete()
	return redirect('inicio')

def borrandoadmin(request, id):
	perfil = Perfil.objects.get(id=id)
	perfil.delete()
	return redirect('admin')

def borrandoproducto(request, id):
	prd = Producto.objects.get(id=id)
	prd.delete()
	return redirect('admin')

def borrandoctg(request, id):
	ctg = Categoria.objects.get(id=id)
	ctg.delete()
	return redirect('admin')


def editar_perfil(request, id):
    perfil = get_object_or_404(Perfil, id=id)
    cate = Categoria.objects.all().order_by('nombre')

    if request.method == 'POST':
    # Actualizar los datos del perfil con los valores enviados mediante el formulario POST
        perfil.categoria_id = request.POST.get('categ', None)
        perfil.nomEstable = request.POST['nombre']
        perfil.colonia=request.POST['colonia']
        perfil.descripcion_Estable = request.POST['descripcion']
        perfil.sitio_web = request.POST['web']
        perfil.telefono = request.POST['telefono']
        perfil.latitud = request.POST['lat']
        perfil.longitud = request.POST['lng']
        perfil.whatsapp = request.POST['whats']
        perfil.twitter = request.POST['twitter']
        perfil.instagram = request.POST['instagram']
        perfil.facebook = request.POST['facebook']
        perfil.correo_tienda = request.POST['correo']
        perfil.every_allday = request.POST['alldayxd']
        perfil.lunes_entrada = request.POST['hora1']
        perfil.lunes_salida = request.POST['hora2']
        perfil.martes_entrada = request.POST['hora3']
        perfil.martes_salida = request.POST['hora4']
        perfil.miercoles_entrada = request.POST['hora5']
        perfil.miercoles_salida = request.POST['hora6']
        perfil.jueves_entrada = request.POST['hora7']
        perfil.jueves_salida = request.POST['hora8']
        perfil.viernes_entrada = request.POST['hora9']
        perfil.viernes_salida = request.POST['hora10']
        perfil.sabado_entrada = request.POST['hora11']
        perfil.sabado_salida = request.POST['hora12']
        perfil.domingo_entrada = request.POST['hora13']
        perfil.domingo_salida = request.POST['hora14']
        nueva_categoria = request.POST.get('nueva_categoria', None)
        

        # Verificar si se proporcionó una nueva imagen
        imagen_nueva = request.FILES.get('img')
        if imagen_nueva:
            perfil.imagen = imagen_nueva

        # Validar que se haya seleccionado una categoría o se haya escrito una nueva
        if not perfil.categoria_id and not nueva_categoria:
            messages.error(request, 'Debes seleccionar una categoría existente o escribir una nueva.')
            return render(request, "editar_perfil.html", {"perfil": perfil, "cate": cate})

        if nueva_categoria:
            # Si se proporciona un nombre de nueva categoría, creamos una nueva instancia de Categoria y la guardamos
            categoria, created = Categoria.objects.get_or_create(nombre=nueva_categoria)
            perfil.categoria_id = categoria.pk
        
        perfil.update = timezone.now()
        perfil.save()
        
        return redirect('inicio')


    return render(request, "web/editar_perfil.html", {"perfil": perfil, "cate": cate})



def posts(request,id,nombre):
    per = Perfil.objects.get(id=id,nomEstable=nombre) 
    pos = Post.objects.filter(perfil=per.id).order_by('-update')
    pub= Post()

    if request.method == 'POST':
        pub.autor=User.objects.get(pk=request.POST['userxdxd'])
        pub.perfil=Perfil.objects.get(pk=request.POST['perfilxd'])
        pub.body=request.POST['despub']
        pub.imagen=request.FILES.get('imgpub')
        pub.save()


        return render(request, 'perfil/post.html',{'pos':pos,'per':per})       
    return render(request, 'perfil/post.html',{'pos':pos,'per':per})

def ver_posts(request):
    post=Post.objects.all().order_by('-update')
    return render(request, 'web/publicaciones.html',{'post':post})

def ver_comentarios(request):
    comentarios=Comentario.objects.all().order_by('-create')
    return render(request, 'perfil/comentarios.html',{'comentarios':comentarios})

def ver_estadisticas(request):
    usuario=request.user.id
    usuario2=request.user.username
    
    comentarios = Comentario.objects.filter(likes__id=request.user.id).order_by('-create')
    perfiles = Perfil.objects.filter(likes__id=request.user.id).order_by('-create')
    publicaciones = Post.objects.filter(likes__id=request.user.id).order_by('-create')
    resenias = Resenias.objects.filter(likes__id=request.user.id).order_by('-create')
    perfilesxd = Perfil.objects.filter(usuario=usuario).order_by('-create')
    comentariosxd = Comentario.objects.filter(autor=usuario).order_by('-create')
    publicacionesxd = Post.objects.filter(autor=usuario).order_by('-create')
    reseniasxd = Resenias.objects.filter(autor=usuario).order_by('-create')
    visitados = Perfil.objects.filter(vistos=usuario).order_by('-nomEstable')



    return render(request, 'web/estadisticas.html', {'comentarios': comentarios, 'perfiles': perfiles, 'publicaciones': publicaciones,'resenias':resenias,'perfilesxd':perfilesxd,'comentariosxd':comentariosxd,'publicacionesxd':publicacionesxd,'reseniasxd':reseniasxd,'visitados':visitados})










def eliminar_res(request, id):
    re = Resenias.objects.get(id=id) 
    if request.user != re.autor:
        return HttpResponse('suck')

    if request.method == 'POST':
        re.delete()
        return redirect('index') 
    return render(request,'web/reseniaborrar.html',{'re':re})       

def borrando_res(request, id):
    re = Resenias.objects.get(id=id)
    re.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def borrando_prd(request, id):
    prd = Articulo.objects.get(id=id)
    prd.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     

def borrando_com(request,id):
    com = Comentario.objects.get(id=id)
    if com:
        com.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def borrando_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post:
        post.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def darlikeperfil(request,pk):
    perfil=get_object_or_404(Perfil,id=pk)
    if request.user in perfil.likes.all():
        perfil.likes.remove(request.user)
    else:
        perfil.likes.add(request.user)
        create_notification(request.user,perfil.usuario, f'{request.user.username} le dio like a tu perfil', f'/muestraperfil/{perfil.id}/{perfil.nomEstable}')
    
    return redirect('muestraperfil', perfil.id, perfil.nomEstable)






def darlikecomentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    is_liked = request.user in comentario.likes.all()
    if is_liked:
        comentario.likes.remove(request.user)
    else:
        comentario.likes.add(request.user)
        if request.user != comentario.autor:
            create_notification(request.user,comentario.autor, f'{request.user.username} le dio like a tu comentario', f'/comentarios/{comentario.negocio.id}/{comentario.negocio.nomEstable}')  
    likes_count = comentario.likes.all().count()
    print('likes_count:', likes_count)
    return JsonResponse({'likes_count': likes_count, 'is_liked': is_liked})


def darlikereseniaoperfil(request, id):
    resenia = get_object_or_404(Resenias, id=id)
    is_likeded = request.user in resenia.likes.all()
    if is_likeded:
        resenia.likes.remove(request.user)
    else:
        resenia.likes.add(request.user)
        if request.user != resenia.autor:
            create_notification(request.user,resenia.autor, f'{request.user.username} le dio like a tu reseña', f'/muestraperfil/{resenia.negocio.id}/{resenia.negocio.nomEstable}') 



    likes_countre = resenia.likes.all().count()
    print('likes_countre:', likes_countre)
    return JsonResponse({'likes_countre': likes_countre, 'is_likeded': is_likeded})

def darlikecomentarioperfil(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    is_liked = request.user in comentario.likes.all()
    if is_liked:
        comentario.likes.remove(request.user)
    else:
        comentario.likes.add(request.user)
        print(comentario.autor)
        if request.user != comentario.autor:
            create_notification(request.user,comentario.autor, f'{request.user.username} le dio like a tu comentario', f'/comentarios/{comentario.negocio.id}/{comentario.negocio.nomEstable}')

     
    likes_count = comentario.likes.all().count()
    print('likes_count:', likes_count)
    return JsonResponse({'likes_count': likes_count, 'is_liked': is_liked})

def darlikepostperfil(request, id):
    post = get_object_or_404(Post, id=id)
    is_liked = request.user in post.likes.all()
    if is_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if request.user != post.autor:
            create_notification(request.user,post.perfil.usuario, f'{request.user.username} le dio like a tu publicación', f'/publicaciones/{post.perfil.id}/{post.perfil.nomEstable}') 

    likes_count = post.likes.all().count()
    print('likes_count:', likes_count)
    return JsonResponse({'likes_count': likes_count, 'is_liked': is_liked})

def darlikepost(request, id):
    post = get_object_or_404(Post, id=id)
    is_liked = request.user in post.likes.all()
    if is_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if request.user != post.autor:
            create_notification(request.user,post.perfil.usuario, f'{request.user.username} le dio like a tu publicación', f'/publicaciones/{post.perfil.id}/{post.perfil.nomEstable}')
    likes_count = post.likes.all().count()
    print('likes_count:', likes_count)
    return JsonResponse({'likes_count': likes_count, 'is_liked': is_liked})


def resultado_categoria(request, nombre):
    perfiles = Perfil.objects.filter(categoria__nombre=nombre)
    categoria = Categoria.objects.get(nombre=nombre)
    return render(request, 'web/resultado_categoria.html', {'perfiles': perfiles, 'categoria': categoria})



def comentarios(request,id,nombre):
    per = Perfil.objects.get(id=id,nomEstable=nombre) 
    com = Comentario.objects.filter(negocio=per.id).order_by('-create')
    parent = Comentario.objects.filter(negocio=per.id)
    
        

    if request.method == 'POST':
        user_id = request.POST['userxdxdxd']
        perfil_id = request.POST['perfilxdxd']
        if 'comentario_form' in request.POST:
            comentario = Comentario(
                autor=User.objects.get(pk=user_id),
                negocio=Perfil.objects.get(pk=perfil_id),
                body=request.POST['descom']

            )
            comentario.save()

            if request.user != comentario.negocio.usuario:
                create_notification(request.user,comentario.negocio.usuario, f'{request.user.username} hizo un comentario en tu perfil {comentario.negocio.nomEstable}', f'/comentarios/{comentario.negocio.id}/{comentario.negocio.nomEstable}')


        elif 'respuesta_form' in request.POST:
            parent_id = request.POST.get('parent_comment_id')
            parent = Comentario.objects.get(id=parent_id)
            respuesta = Comentario(
                autor=User.objects.get(pk=user_id),
                negocio=Perfil.objects.get(pk=perfil_id),
                body=request.POST['desres'],
                parent_comment=parent
            )
            respuesta.save()
            if request.user != respuesta.parent_comment.autor :
                create_notification(request.user,respuesta.parent_comment.autor, f'{request.user.username} respondió a tu comentario en {respuesta.negocio.nomEstable}', f'/comentarios/{respuesta.negocio.id}/{respuesta.negocio.nomEstable}')

        elif 'edicion_form' in request.POST:
            comentario_id = request.POST['comentario_id']
            comentario = Comentario.objects.get(id=comentario_id)
            user_id = request.POST['userxdxdxd']
            perfil_id = request.POST['perfilxdxd']
            comentario.body = request.POST['descomentario']
            comentario.update = timezone.now()
            comentario.save()

    return render(request, 'perfil/comentarios_perfil.html', {'com':com, 'per':per, 'parent_comment':parent})



def editar_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.body = request.POST['body']

        # Verificar si se ha solicitado eliminar la imagen
        if request.POST.get('delete_image') == 'true':
            # Eliminar la imagen anterior si existe
            if post.imagen:
                post.imagen.delete()
            # Asignar None para eliminar la referencia de la imagen en el post
            post.imagen = None

        # Verificar si se ha subido una nueva imagen
        if 'imagen' in request.FILES:
            # Eliminar la imagen anterior si existe
            if post.imagen:
                post.imagen.delete()
            # Asignar la nueva imagen al post
            post.imagen = request.FILES['imagen']
            print(post.imagen)  # Imprime la información de la nueva imagen
            print(post.imagen.name)  # Imprime el nombre del archivo de imagen
            print(post.imagen.size) 
        post.update = timezone.now()
        post.save()
        perfil_id = post.perfil.nomEstable
        # Generar la URL de la vista anterior y redirigir al usuario
        url = reverse('posts', args=[perfil_id])
        return redirect(url)

    return render(request, 'perfil/editar_post.html', {'post': post})


def agregar_productos(request,id):
    perfil=Perfil.objects.get(id=id)
    return render(request,'perfil/agregar_productos.html',{'perfil':perfil})

def agregar_productos_fast(request, id):
    perfil = get_object_or_404(Perfil, id=id)

    if request.method == 'POST':
        # Obtener el producto desde la petición
        nombre_producto = request.POST.get('nombreproducto', '')

        # Obtener o crear un objeto Producto con el nombre especificado
        producto, created = Producto.objects.get_or_create(nombre=nombre_producto)

        # Agregar el producto al campo many-to-many
        perfil.productos.add(producto)

    return render(request, 'web/agregar_producto_fast.html',{'perfil':perfil})




def agregar_productos_slow(request,id):
    perfil= get_object_or_404(Perfil, id=id)

    if request.method == 'POST':
        nombre = request.POST['nombrearticulo']
        descripcion = request.POST['descripcionarticulo']
        precio = request.POST['precioarticulo']
        imagen = request.FILES.get('imagenarticulo')
        Articulo.objects.create(autor=request.user,nombre=nombre, perfil=perfil, descripcion=descripcion, precio=precio, imagen=imagen)
        return HttpResponseRedirect(reverse('agregar_productos_slow',args=[perfil.id]))

    return render(request,'web/agregar_producto_slow.html',{'perfil':perfil})
 
             

    

def ver_productos(request,id):
    perfil = Perfil.objects.filter(id=id).first()
    articulo=Articulo.objects.filter(perfil=id)
    
    return render(request,'perfil/ver_productos.html',{'articulo':articulo,'perfil':perfil})

def editar_productos(request, id):
    producto = get_object_or_404(Articulo, id=id)
    

    if request.method == 'POST':
        # Actualizar el producto con los datos del formulario
        producto.nombre = request.POST['nombrearticulo']
        producto.descripcion = request.POST['descripcionarticulo']
        producto.precio = request.POST['precioarticulo']
        if 'imagenarticulo' in request.FILES:
            producto.imagen = request.FILES['imagenarticulo']
        producto.save()
        return HttpResponseRedirect(reverse('ver_articulos',args=[producto.perfil.id]))

    return render(request, 'perfil/editar_productos.html', {'prd': producto})

def editar_respuesta(request,id):
    comentario=Comentario.objects.get(id=id)
    comentario_padre = comentario.parent_comment

    if request.method == 'POST':
        # Actualizar el producto con los datos del formulario
        comentario.body = request.POST['comentario']
        comentario.update = timezone.now()
     
        comentario.save()
        return HttpResponseRedirect(reverse('comentarios',args=[comentario.negocio.nomEstable]))
    
    return render(request,'perfil/editar_respuesta.html',{'comentario':comentario,'comentario_padre':comentario_padre})


def notificaciones_sin_leer(user):
    count = Notificacion.objects.filter(user_to=user, read=False).count()
    return count

def notificaciones(request,id):
    notifications = Notificacion.objects.filter(user_to=id).order_by('-create')
    unread_count = notificaciones_sin_leer(id)


    return render(request, 'web/notificaciones.html', {'notifications': notifications,'unread_count':unread_count})

@login_required
def marcar_todas_como_leidas(request):
    Notificacion.objects.filter(user_to=request.user).update(read=True)
    return redirect('notificaciones',id=request.user.id)