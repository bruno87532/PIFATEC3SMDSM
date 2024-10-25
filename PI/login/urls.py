from django.urls import path
from login.views import Login

urlpatterns = [
    path('', Login.as_view(), name='login')
]