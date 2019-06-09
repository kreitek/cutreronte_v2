from django.utils import timezone
from rest_framework import serializers

from rest_framework.fields import CurrentUserDefault
from .models import Prueba

class ListaUsuariosSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=False)

    class Meta:
        model = Prueba
        fields = ('nombre',)

