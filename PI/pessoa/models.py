import uuid
from djongo import models

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
    data_nascimento_pessoa = models.DateTimeField()
    telefone_pessoa = models.CharField(max_length=20)
    doacao_pessoa  = models.ArrayField(
        model_container = Doacao,
        null = True,
        blank = True
    )
