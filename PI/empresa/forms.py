from django import forms
from empresa.models import Empresa
from pessoa.models import Pessoa
import requests
import re

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
        widgets = {
            'nome_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cnpj_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'tipo_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email_login_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'senha_login_empresa': forms.PasswordInput(attrs={
                'class': 'form-control',
                'type': 'password',
            }),
        }
    
    def clean_cnpj_empresa(self):
        cnpj_empresa = self.cleaned_data.get('cnpj_empresa')
        cnpj_empresa = ''.join(re.findall(r'\d', cnpj_empresa))
        if len(cnpj_empresa) != 14:
            raise forms.ValidationError('CNPJ inválido')
        if Empresa.objects.filter(cnpj_empresa=cnpj_empresa):
            raise forms.ValidationError('CNPJ já cadastrado')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        r = requests.get(f'https://brasilapi.com.br/api/cnpj/v1/{cnpj_empresa}', headers=headers)
        if r.status_code != 200 and r.status_code != 504:
            raise forms.ValidationError('CNPJ inválido')
        return cnpj_empresa

    def clean_email_login_empresa(self):
        email_login_empresa = self.cleaned_data.get('email_login_empresa')
        if Empresa.objects.filter(email_login_empresa=email_login_empresa) or Pessoa.objects.filter(email_login_pessoa=email_login_empresa):
            raise forms.ValidationError('Email já cadastrado')
        return email_login_empresa

    def clean_senha_login_empresa(self):
        senha_login_empresa = self.cleaned_data.get('senha_login_empresa')
        if len(senha_login_empresa) < 8:
            raise forms.ValidationError('Senha inválida')
        return senha_login_empresa

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
        widgets = {
            'cep_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'estado_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cidade_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'bairro_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'rua_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'numero_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'complemento_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_cep_empresa(self):
        cep_empresa = self.cleaned_data.get('cep_empresa')
        cep_empresa = ''.join(re.findall(r'\d', cep_empresa))
        if len(cep_empresa) != 8:
            raise forms.ValidationError('CEP inválido')
        r = requests.get(f'https://viacep.com.br/ws/{cep_empresa}/json/')
        if r.status_code != 200:
            raise forms.ValidationError('CEP inválido')
        if r.json().get('erro'):
            raise forms.ValidationError('CEP inválido')
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
        widgets = {
            'nome_representante_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cpf_representante_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'telefone_representante_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email_representante_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }

    def clean_nome_representante_empresa(self):
        nome_representante_empresa = self.cleaned_data.get('nome_representante_empresa')
        nome_representante_empresa = ''.join(re.findall(r'[a-zA-Z\s]', str(nome_representante_empresa)))
        if len(nome_representante_empresa) == 0:
            raise forms.ValidationError('Nome inválido')
        return nome_representante_empresa
    def clean_cpf_representante_empresa(self):
        cpf_representante_empresa = self.cleaned_data.get('cpf_representante_empresa')
        cpf_representante_empresa = ''.join(re.findall(r'\d', str(cpf_representante_empresa)))
        peso_primeiro_digito = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        peso_segundo_digito = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        soma_primeiro_digito = 0
        soma_segundo_digito = 0
        if len(str(cpf_representante_empresa)) != 11:
            raise forms.ValidationError('CPF inválido')
        for n, p in zip(str(cpf_representante_empresa)[0:9], peso_primeiro_digito):
            soma_primeiro_digito += int(n) * p
        resultado_soma_primeiro_digito = soma_primeiro_digito % 11
        if resultado_soma_primeiro_digito > 1 and not str(11 - resultado_soma_primeiro_digito) == str(cpf_representante_empresa)[9]:
            raise forms.ValidationError('CPF inválido!')
        if (resultado_soma_primeiro_digito == 1 or resultado_soma_primeiro_digito == 0) and str(cpf_representante_empresa)[9] != '0':
            raise forms.ValidationError('CPF inválido!')
        for n, p in zip(str(cpf_representante_empresa)[0:10], peso_segundo_digito):
            soma_segundo_digito += int(n) * p
        resultado_soma_segundo_digito = soma_segundo_digito % 11
        if resultado_soma_segundo_digito > 1 and not str(11 - resultado_soma_segundo_digito) == str(cpf_representante_empresa)[10]:
            raise forms.ValidationError('CPF inválido!')
        if (resultado_soma_segundo_digito == 1 or resultado_soma_segundo_digito == 0) and str(cpf_representante_empresa)[10] != '0':
            raise forms.ValidationError('CPF inválido!')
        return cpf_representante_empresa
    def clean_telefone_representante_empresa(self):
        telefone_representante_empresa = self.cleaned_data.get('telefone_representante_empresa')
        telefone_representante_empresa = ''.join(re.findall(r'\d', telefone_representante_empresa))
        if len(telefone_representante_empresa) < 9:
            raise forms.ValidationError('Telefone inválido')
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