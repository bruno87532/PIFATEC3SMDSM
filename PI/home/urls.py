from django.urls import path
from home.views import Home, Erro
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('erro/', Erro.as_view(), name='erro')
]