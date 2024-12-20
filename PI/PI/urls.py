"""PI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from ong.urls import urlpatternscad as url_ong_cad, urlpatterns as url_ong
from empresa.urls import urlpatternscad as url_empresa_cad
from home.urls import urlpatterns as url_home
from pessoa.urls import urlpatternscad as url_pessoa_cad
from home.urls import urlpatterns as url_home
from login.urls import urlpatterns as url_login_logout
from pessoa.urls import urlpatternsdoacao as url_pessoa_doacao
from empresa.urls import urlpatternsdoacao as url_empresa_doacao

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/empresa/', include(url_empresa_cad)),
    path('cadastro/pessoa/', include(url_pessoa_cad)),
    path('cadastro/ong/', include(url_ong_cad)),
    path('home/', include(url_home)),
    path('auth/', include(url_login_logout)),
    path('doacao/pessoa/', include(url_pessoa_doacao)),
    path('doacao/', include(url_empresa_doacao)),
    path('', include(url_home)),
    path('distribuicao/', include(url_ong)),
    path('pessoa/pagamento/', include(url_pessoa_doacao))
]
