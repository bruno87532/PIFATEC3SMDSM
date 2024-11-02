import uuid
from djongo import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Doacao(models.Model):
    categoria = [
        ('carne', 'Carne'),
        ('flv', 'Frutas, legumes e verduras'),
        ('frios', 'Frios'),
        ('higiene', 'Higiene'),
        ('limpeza', 'Limpeza'),
        ('mercearia', 'Mercearia'), 
    ]
    medida = [
        ('gramas', 'Grama'),
        ('kg', 'Kg'),
        ('tonelada', 'Tonelada'),
        ('unidade', 'Unidade'),
    ]    

    id_empresa = models.CharField(max_length=256)
    nome_produto = models.CharField(max_length=100)
    descricao_produto = models.CharField(max_length=256, blank=True, null=True)
    quantidade_produto = models.CharField(max_length=20)
    unidade_medida_produto = models.CharField(max_length=50, choices=medida)
    categoria_produto = models.CharField(max_length=50, choices=categoria)
    data_doado_produto = models.DateField(auto_now_add=True)

class ProdutoOfertado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_produto = models.CharField(max_length=100)
    descricao_produto = models.CharField(max_length=256, blank=True, null=True)
    quantidade_produto = models.IntegerField()
    validade_produto = models.DateTimeField()
    disponivel_produto = models.BooleanField(default=True)

class Empresa(models.Model):
    nome_empresa = models.CharField(max_length=100)
    cnpj_empresa = models.CharField(max_length=20)
    tipo_empresa = models.CharField(max_length=100)
    email_login_empresa = models.EmailField(max_length=100)
    senha_login_empresa = models.CharField(max_length=100)
    cep_empresa = models.CharField(max_length=20)
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
    # doacao_empresa = models.ArrayField(
    #     model_container = Doacao,
    #     null = True,
    #     blank = True
    # )
    # produto_ofertado_empresa = models.ArrayField(
    #     model_container = ProdutoOfertado,
    #     null = True,
    #     blank = True
    # )

    def set_senha(self, senha_login_empresa):
        self.senha_login_empresa = make_password(senha_login_empresa)

    def verifica_senha(self, senha_login_empresa):
        return check_password(senha_login_empresa, self.senha_login_empresa)