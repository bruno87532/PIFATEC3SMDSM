import uuid
from djongo import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

import uuid
from djongo import models

class Doacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    valor_doacao = models.FloatField()


class Pessoa(models.Model):
    nome_pessoa = models.CharField(max_length=100)
    cpf_pessoa = models.CharField(max_length=20)
    email_login_pessoa = models.EmailField(max_length=100)
    senha_login_pessoa = models.CharField(max_length=100)
    data_nascimento_pessoa = models.DateField()
    telefone_pessoa = models.CharField(max_length=20)
    # doacao_pessoa  = models.ArrayField(
    #     model_container = Doacao,
    #     null = True,
    #     blank = True
    # )

    def set_senha(self, senha_login_pessoa):
        self.senha_login_pessoa = make_password(senha_login_pessoa)

    def verifica_senha(self, senha_login_pessoa):
        return check_password(senha_login_pessoa, self.senha_login_pessoa)