from djongo import models
from django.contrib.auth.hashers import make_password, check_password

class ModeloPadrao(models.Model):
    id = models.ObjectIdField(primary_key=True)
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20)
    email_login = models.EmailField(max_length=100)
    senha_login = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)
    estado = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    nome_representante = models.CharField(max_length=100)
    cpf_representante = models.CharField(max_length=11)
    telefone_representante = models.CharField(max_length=20)
    email_representante = models.EmailField(max_length=100)

    def set_senha(self, senha_login):
        self.senha_login = make_password(senha_login)

    def verifica_senha(self, senha_login):
        return check_password(senha_login, self.senha_login)

    class Meta:
        abstract = True