from rest_framework import serializers
from pessoa.models import Pessoa

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ['nome_pessoa', 'cpf_pessoa', 'email_login_pessoa', 'senha_login_pessoa', 'data_nascimento_pessoa', 'telefone_pessoa']
    def validate_cpf_pessoa(self, value):
        return value
    def validate_data_nascimento_pessoa(self, value):
        return value