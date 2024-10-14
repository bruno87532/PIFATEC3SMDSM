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
from empresa.urls import urlpatternscad as url_empresa_cad, urlpatternslogin as url_empresa_login
from home.urls import urlpatterns as url_home
from pessoa.urls import urlpatternscad as url_pessoa_cad, urlpatternslogin as url_pessoa_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/empresa/', include(url_empresa_cad)),
    path('login/empresa/', include(url_empresa_login)),
    path('cadastro/pessoa/', include(url_pessoa_cad)),
    path('login/pessoa/', include(url_pessoa_login)),
    path('', include(url_home))
]
