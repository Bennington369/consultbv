
from django.shortcuts import render,redirect
from perfil.forms import PerfilModelForm
from .models import Perfil,Categoria
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.

@login_required
def perfil(request):
    cate = Categoria.objects.all().order_by('nombre') 
    ps = Perfil.objects.all()

    if request.method == 'POST':
        categoria_id = request.POST.get('categ', None)
        nueva_categoria = request.POST.get('nueva_categoria', None)
        
        # Validar que se haya seleccionado una categoría o se haya escrito una nueva
        if not categoria_id and not nueva_categoria:
            messages.error(request, 'Debes seleccionar una categoría existente o escribir una nueva.')
            return render(request, "perfil.html", {"cate": cate, "ps": ps})

        if nueva_categoria:
            # Si se proporciona un nombre de nueva categoría, creamos una nueva instancia de Categoria y la guardamos
            categoria, created = Categoria.objects.get_or_create(nombre=nueva_categoria)
            categoria_id = categoria.pk

        if categoria_id:
            tipo_id = Categoria.objects.get(pk=categoria_id)
            xd = Perfil(
                usuario=User.objects.get(pk=request.POST['userxd']),
                categoria=tipo_id,
                nomEstable=request.POST['nombre'],
                colonia=request.POST['colonia'],
                descripcion_Estable=request.POST['descripcion'],
                sitio_web=request.POST['web'],
                telefono=request.POST['telefono'],
                latitud=request.POST['lat'],
                longitud=request.POST['lng'],
                whatsapp=request.POST['whats'],
                imagen=request.FILES.get('img'),
                twitter=request.POST['twitter'],
                instagram=request.POST['instagram'],
                facebook=request.POST['facebook'],
                correo_tienda=request.POST['correo'],
                every_allday=request.POST['alldayxd'],
                lunes_entrada=request.POST['hora1'],
                lunes_salida=request.POST['hora2'],
                martes_entrada=request.POST['hora3'],
                martes_salida=request.POST['hora4'],
                miercoles_entrada=request.POST['hora5'],
                miercoles_salida=request.POST['hora6'],
                jueves_entrada=request.POST['hora7'],
                jueves_salida=request.POST['hora8'],
                viernes_entrada=request.POST['hora9'],
                viernes_salida=request.POST['hora10'],
                sabado_entrada=request.POST['hora11'],
                sabado_salida=request.POST['hora12'],
                domingo_entrada=request.POST['hora13'],
                domingo_salida=request.POST['hora14'],
            )
            xd.save()

            return redirect('inicio')

    return render(request, "perfil.html", {"cate": cate, "ps": ps})


