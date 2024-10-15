from rest_framework import serializers
from pessoa.models import Pessoa
from datetime import datetime
from django.utils import timezone

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ['nome_pessoa', 'cpf_pessoa', 'email_login_pessoa', 'senha_login_pessoa', 'data_nascimento_pessoa', 'telefone_pessoa']
    def validate_cpf_pessoa(self, value):
        # Regra para validar CPF:
        # Os 9 primeiros dígitos são aleatórios, os últimos 2 são calculados com base em um cálculo feito com os p9 primeiros:
        # O primeiro dígito dos 9 primeiros é multiplicado por 10, o segundo por 8 e assim sucessivamente até o nono que é multiplicado por 2
        # É feito a soma destes valores e divido por 11, se o resto for 0 ou 1, o décimo dígito do cpf é 0, caso o resto for > 1 o décimo dígito do cpf é 11 - resto
        # Para calcular o décimo primeiro dígito é semelhante, mas invés de multiplicar o primeiro dígito por 10 é por 11, o segundo por 10 e assim sucessivamente até o décimo que é por 2, seguidamente se aplica a mesma lógica que usou no décimo dígito
        peso_primeiro_digito = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        peso_segundo_digito = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        soma_primeiro_digito = 0
        soma_segundo_digito = 0
        if len(str(value)) != 11:
            raise serializers.ValidationError('CPF inválido')
        for n, p in zip(str(value)[0:9], peso_primeiro_digito):
            soma_primeiro_digito += int(n) * p
        resultado_soma_primeiro_digito = soma_primeiro_digito % 11
        if resultado_soma_primeiro_digito > 1 and not str(11 - resultado_soma_primeiro_digito) == str(value)[9]:
            raise serializers.ValidationError('CPF inválido!')
        if (resultado_soma_primeiro_digito == 1 or resultado_soma_primeiro_digito == 0) and str(value)[9] != '0':
            raise serializers.ValidationError('CPF inválido!')
        for n, p in zip(str(value)[0:10], peso_segundo_digito):
            soma_segundo_digito += int(n) * p
        resultado_soma_segundo_digito = soma_segundo_digito % 11
        if resultado_soma_segundo_digito > 1 and not str(11 - resultado_soma_segundo_digito) == str(value)[10]:
            raise serializers.ValidationError('CPF inválido!')
        if (resultado_soma_segundo_digito == 1 or resultado_soma_segundo_digito == 0) and str(value)[10] != '0':
            raise serializers.ValidationError('CPF inválido!')
        return value
    
    def validate_data_nascimento_pessoa(self, value):
        if value > timezone.now() or value < datetime(1900, 1, 1, tzinfo=timezone.utc):
            raise serializers.ValidationError('Data de nascimento inválida')
        return value