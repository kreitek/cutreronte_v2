from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.sniffer1, name='sniffer1'),

]
