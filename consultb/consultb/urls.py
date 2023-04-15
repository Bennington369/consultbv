"""consultb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include
from aplicacion import views
from aplicacion.views import VRegistro,cerrar_sesion,logear
from perfil.urls import urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('perfil/', include('perfil.urls')),
    path('administracion/', views.admin,name='admin'),
    path('',views.index,name='index'),
    path('categoria/',views.categoria, name='categoria'),
    path('contacto/',views.contacto, name='contacto'),
    path('registro/',VRegistro.as_view(), name='registro'),
    path('logear',logear,name="logear"),
    path('muestraperfil/<int:id>/<str:nom>',views.muestraperfil,name="muestraperfil"),
    path('resultados/',views.busqueda,name="busqueda"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/logout',views.cerrar_sesion,'logout'),
    path('inicioperfil/',views.inicioxd,name='inicio'),
    path('inicioperfil/borrar/<int:id>', views.borrar, name='borrar'),
	path('inicioperfil/borrando/<int:id>', views.borrando, name='borrando'),
    path('inicioperfil/borrandoxd/<int:id>', views.borrandoadmin, name='borrandoadmin'),
    path('borrar_res/<int:id>', views.eliminar_res, name='eliminar_res'),
    path('borrandores/<int:id>', views.borrando_res, name='borrando_res'),
    path('borrandoprd/<int:id>', views.borrandoproducto, name='borrando_prdrap'),
    path('borrandoctg/<int:id>', views.borrandoctg, name='borrando_ctg'),
    path('inicioperfil/editar_perfil/<int:id>', views.editar_perfil, name='editar'),
    path('publicaciones/<int:id>/<str:nombre>', views.posts, name='posts'),
    path('comentarios/<int:id>/<str:nombre>', views.comentarios, name='comentarios'),

    path('like/<int:pk>', views.darlikeperfil, name='dar_like'),
    path('like_resenia/<int:id>', views.darlikereseniaoperfil, name='dar_likeresenia'),
    path('like_comentario/<int:id>', views.darlikecomentario, name='dar_likecomentario'),
    path('like_comentarioperfil/<int:id>', views.darlikecomentarioperfil, name='dar_likecomentarioperfil'),
    path('inicio/publicaciones/', views.ver_posts, name='ver_posts'),
    path('inicio/comentarios/', views.ver_comentarios, name='ver_comentarios'),
    path('like_postperfil/<int:id>', views.darlikepostperfil, name='dar_likepostperfil'),
    path('like_post/<int:id>', views.darlikepost, name='dar_likepost'), 

   
    path('borrandocomentario/<int:id>', views.borrando_com, name='borrando_com'),
    path('borrandopost/<int:id>', views.borrando_post, name='borrando_post'),
    path('borrandoproducto/<int:id>', views.borrando_prd, name='borrando_prd'),

    path('mapa/', views.mapa, name='mapa'),
    path('estadisticas/', views.ver_estadisticas, name='estadisticas'),


    path('resultadoscategoria/<str:nombre>', views.resultado_categoria, name='resultado_categoria'),

    path('editar_post/<int:id>', views.editar_post, name='editar_post'),
    path('editar_producto/<int:id>', views.editar_productos, name='editar_prd'),

    path('agregar_productos/<int:id>', views.agregar_productos, name='agregar_productos'),
    path('agregar_productos_fast/<int:id>', views.agregar_productos_fast, name='agregar_productos_fast'),
    path('agregar_productos_slow/<int:id>', views.agregar_productos_slow, name='agregar_productos_slow'),

    path('ver_articulos/<int:id>', views.ver_productos, name='ver_articulos'),
    path('editar_respuesta/<int:id>', views.editar_respuesta, name='editar_respuesta'),

    path('notificaciones/<int:id>', views.notificaciones, name='notificaciones'),

    path('marcar-todas-como-leidas/', views.marcar_todas_como_leidas, name='marcar_todas_como_leidas'),





   






]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)