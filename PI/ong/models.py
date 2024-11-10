from djongo import models
from utils.models.model_padrao import ModeloPadrao

# Create your models here.

class Ong(ModeloPadrao):
    objetivo_ong = models.CharField(max_length=256)
    
    def __str__(self):
        return self.nome
    
class DoacaoRecebida(models.Model):
    id = models.ObjectIdField(primary_key=True)
    id_empresa = models.CharField(max_length=256)
    id_ong = models.CharField(max_length=256)
    nome_produto = models.CharField(max_length=100)
    descricao_produto = models.CharField(max_length=256, blank=True, null=True)
    quantidade_produto = models.CharField(max_length=20)
    unidade_medida_produto = models.CharField(max_length=50)
    categoria_produto = models.CharField(max_length=50)
    data_doado_produto = models.DateTimeField()
    data_recebido_produto = models.DateTimeField(auto_now_add=True)