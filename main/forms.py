from django import forms
from .models import Photo
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']  # только поле для загрузки фото


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
