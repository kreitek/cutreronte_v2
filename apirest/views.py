from rest_framework import viewsets, status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.utils import timezone
from .models import Prueba

from .serializers import ListaUsuariosSerializer


class ListaUsuariosView(viewsets.ModelViewSet):
    model = Prueba
    serializer_class = ListaUsuariosSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.all()
