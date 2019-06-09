from django.urls import path, include
from . import views as v
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('listausuarios', v.ListaUsuariosView, 'apirest-lista-usuarios')

urlpatterns = [
    path('', include(router.urls))
]
