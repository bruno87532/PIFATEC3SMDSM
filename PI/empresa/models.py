import uuid
from djongo import models

# Create your models here.

class Doacao(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   nome_produto = models.CharField(max_length=100)
   descricao_produto = models.CharField(max_length=256, blank=True, null=True)
   quantidade_produto = models.IntegerField()

class ProdutoOfertado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_produto = models.CharField(max_length=100)
    descricao_produto = models.CharField(max_length=256, blank=True, null=True)
    quantidade_produto = models.IntegerField()
    validade_produto = models.DateTimeField()
    disponivel_produto = models.BooleanField(default=True)

class Empresa(models.Model):
    nome_empresa = models.CharField(max_length=100)
    cnpj_empresa = models.CharField(max_length=14)
    tipo_empresa = models.CharField(max_length=100)
    email_login_empresa = models.EmailField(max_length=100)
    senha_login_empresa = models.CharField(max_length=100)
    cep_empresa = models.CharField(max_length=8)
    estado_empresa = models.CharField(max_length=100)
    cidade_empresa = models.CharField(max_length=100)
    bairro_empresa = models.CharField(max_length=100)
    rua_empresa = models.CharField(max_length=100)
    numero_empresa = models.CharField(max_length=10)
    complemento_empresa = models.CharField(max_length=100, null=True, blank=True)
    nome_representante_empresa = models.CharField(max_length=100)
    cpf_representante_empresa = models.CharField(max_length=11)
    telefone_representante_empresa = models.CharField(max_length=20)
    email_representante_empresa = models.EmailField(max_length=100)
    doacao_empresa = models.ArrayField(
        model_container = Doacao,
        null = True,
        blank = True
    )
    produto_ofertado_empresa = models.ArrayField(
        model_container = ProdutoOfertado,
        null = True,
        blank = True
    )