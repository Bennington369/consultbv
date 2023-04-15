import imp
from pydoc import importfile

from django.forms.widgets import TextInput,EmailInput,PasswordInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from perfil.models import Comentario


from perfil.models import Perfil


class UsuarioNuevo(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': "Nombre de Usuario"}))  
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': "Contraseña"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': "Repetir Contraseña"}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1']
        help_texts = {k:"" for k in fields}
        widgets = {
        'first_name': TextInput(attrs={
        'class': "form-control",
        'placeholder': "Nombres"
        }),
        'last_name': TextInput(attrs={
        'class': "form-control",
        'placeholder': "Apellidos"
        }),
        'email': EmailInput(attrs={
        'class': "form-control",
        'placeholder': 'Correo electrónico'
        })
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields ='__all__'

class NuevaCategoriaForm(forms.Form):
    nombre = forms.CharField(max_length=50)

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['body', 'parent_comment']