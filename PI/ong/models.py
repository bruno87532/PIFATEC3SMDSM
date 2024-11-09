from django.db import models
from utils.models.model_padrao import ModeloPadrao

# Create your models here.

class Ong(ModeloPadrao):
    objetivo_ong = models.CharField(max_length=256)