import uuid
from djongo import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

import uuid
from djongo import models

class Doacao(models.Model):
    id = models.ObjectIdField(primary_key=True)
    id_pessoa = models.CharField(max_length=256)
    valor_doacao = models.FloatField()
    data_doado = models.DateField(auto_now_add=True)


class Pessoa(models.Model):
    id = models.ObjectIdField(primary_key=True)
    nome_pessoa = models.CharField(max_length=100)
    cpf_pessoa = models.CharField(max_length=20)
    email_login_pessoa = models.EmailField(max_length=100)
    senha_login_pessoa = models.CharField(max_length=100)
    data_nascimento_pessoa = models.DateField()
    telefone_pessoa = models.CharField(max_length=20)
    valor_total_doado_pessoa = models.FloatField(default=0)

    def set_senha(self, senha_login_pessoa):
        self.senha_login_pessoa = make_password(senha_login_pessoa)

    def verifica_senha(self, senha_login_pessoa):
        return check_password(senha_login_pessoa, self.senha_login_pessoa)