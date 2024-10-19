from django import forms
from empresa.models import Empresa

# AQUI SERÁ FEITA A SANITAÇÃO DOS DADOS, A VERIFICAÇÃO DE SE ESTAR CORRETOS FAREMOS NO SERIALIZER USANDO DJANGO REST FRAMEWORK

class EmpresaFormUm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome_empresa',
            'cnpj_empresa',
            'tipo_empresa',
            'email_login_empresa',
            'senha_login_empresa',
        ]
    
    def clean_nome_empresa(self):
        nome_empresa = self.cleaned_data.get('nome_empresa')   
        print('A sanitização de nome da empresa foi executada')
        # REMOVA NÚMEROS
        return nome_empresa
    
    def clean_cnpj_empresa(self):
        cnpj_empresa = self.cleaned_data.get('cnpj_empresa')
        print('A sanitização de cnpj da empresa foi executada')
        # REMOVA CARACTERES E DEIXE APENAS OS NÚMEROS DO CNPJ
        return cnpj_empresa


class EmpresaFormDois(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'cep_empresa',
            'estado_empresa',
            'cidade_empresa',
            'bairro_empresa',
            'rua_empresa',
            'numero_empresa',
            'complemento_empresa',
        ]

    def clean_cep_empresa(self):
        cep_empresa = self.cleaned_data.get('cep_empresa')
        print('A sanitização de cep da empresa foi executada')
        # REMOVA CARACTERES E DEIXE APENAS OS NUMEROS DO CEP
        return cep_empresa

class EmpresaFormTres(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome_representante_empresa',
            'cpf_representante_empresa',
            'telefone_representante_empresa',
            'email_representante_empresa',
        ]

    def clean_nome_representante_empresa(self):
        nome_representante_empresa = self.cleaned_data.get('nome_representante_empresa')
        print('A sanitização de nome do representante da empresa foi executada')
        # REMOVA NÚMEROS E DEIXE A PRIMEIRA LETRA DE CADA PALAVRA CAPITALIZADA
        return nome_representante_empresa
    def clean_cpf_representante_empresa(self):
        cpf_representante_empresa = self.cleaned_data.get('cpf_representante_empresa')
        print('A sanitização de cpf do representante da empresa foi executada')
        # REMOVA CARACTERES E DEIXA APENAS O NUMERO DO CPF
        return cpf_representante_empresa
    def clean_telefone_representante_empresa(self):
        telefone_representante_empresa = self.cleaned_data.get('telefone_representante_empresa')
        print('A sanitização de telefone do representante da empresa foi executada')
        # REMOVA CARACTERES E DEIXA APENAS O NUMERO DO TELEFONE
        return telefone_representante_empresa
    
class EmpresaCompleta(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome_empresa',
            'cnpj_empresa',
            'tipo_empresa',
            'email_login_empresa',
            'senha_login_empresa',
            'cep_empresa', 
            'estado_empresa',
            'cidade_empresa',
            'bairro_empresa',
            'rua_empresa',
            'numero_empresa',
            'complemento_empresa',
            'nome_representante_empresa',
            'cpf_representante_empresa',
            'telefone_representante_empresa',
            'email_representante_empresa',
        ]