from rest_framework import serializers
from empresa.models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['nome_empresa', 'cnpj_empresa', 'tipo_empresa', 'email_login_empresa', 'senha_login_empresa', 'cep_empresa', 'estado_empresa', 'cidade_empresa', 'bairro_empresa', 'rua_empresa', 'numero_empresa', 'complemento_empresa', 'nome_representante_empresa', 'cpf_representante_empresa', 'telefone_representante_empresa', 'email_representante_empresa']
    def validate_cnpj_empresa(self, value):
        return value
    def validate_cep_empresa(self, value):
        return value
    def validate_cpf_representante_empresa(self, value):
        return value