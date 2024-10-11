from django.urls import path
from empresa.views import Empresa
urlpatterns = [
    path('', Empresa.as_view(), name='empresa')
]