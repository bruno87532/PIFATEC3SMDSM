from utils.models.model_padrao import ModeloPadrao
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

    id = models.ObjectIdField(primary_key=True)
    id_empresa = models.CharField(max_length=256)
    nome_produto = models.CharField(max_length=100)
    descricao_produto = models.CharField(max_length=256, blank=True, null=True)
    quantidade_produto = models.CharField(max_length=20)
    unidade_medida_produto = models.CharField(max_length=50, choices=medida)
    categoria_produto = models.CharField(max_length=50, choices=categoria)
    data_doado_produto = models.DateTimeField(auto_now_add=True)
    disponivel_produto = models.BooleanField(default=True)

class Empresa(ModeloPadrao):
    tipo_empresa = models.CharField(max_length=100)