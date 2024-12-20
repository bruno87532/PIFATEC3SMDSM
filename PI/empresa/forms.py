from django import forms
from empresa.models import Empresa, Doacao
import re
from services.validacao import Validacao

from django import forms
from .models import Doacao

class EmpresaDoacao(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = [
            'nome_produto',
            'descricao_produto',
            'quantidade_produto',
            'unidade_medida_produto',
            'categoria_produto',
        ]
        widgets = {
            'nome_produto': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descricao_produto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'quantidade_produto': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'step': '0.1',
                'min': '0',
            }),
            'unidade_medida_produto': forms.Select(attrs={
                'class': 'form-control',
            }),
            'categoria_produto': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


    def clean_quantidade_produto(self):
        quantidade_produto = str(self.cleaned_data.get('quantidade_produto'))
        contador = 0
        for i in quantidade_produto:
            if i == ',':
                quantidade_produto = quantidade_produto.replace(',', '.')
                contador += 1
            if i == '.':
                contador += 1
        if contador > 1 or ''.join(re.findall(r'[\d.]+', quantidade_produto)) != quantidade_produto or (quantidade_produto[len(quantidade_produto) - 1] == '.'):
            raise forms.ValidationError('Quantidade inválida')
        return quantidade_produto
    def clean(self):
        cleaned_data = super().clean() 
        unidade_medida = cleaned_data.get('unidade_medida_produto')
        quantidade_produto = cleaned_data.get('quantidade_produto')
        if unidade_medida == 'unidade' and ('.' in str(quantidade_produto) or quantidade_produto is None):
            raise forms.ValidationError('O valor deve ser inteiro para medidas unitária')
        return cleaned_data



class EmpresaFormUm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome',
            'cnpj',
            'tipo_empresa',
            'email_login',
            'senha_login',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'tipo_empresa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email_login': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'senha_login': forms.PasswordInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'minlength': '8',
            }),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        cnpj = Validacao.verifica_cnpj(cnpj)
        if not cnpj:
            raise forms.ValidationError('CNPJ inválido')
        if cnpj == 'cadastrado':
            raise forms.ValidationError('CNPJ já cadastrado')
        return cnpj

    def clean_email_login(self):
        email_login = self.cleaned_data.get('email_login')
        email_login = Validacao.verifica_email(email_login)
        if email_login == 'cadastrado':
            raise forms.ValidationError('Email já cadastrado')
        return email_login
    
    def clean_senha_login(self):
        senha_login = self.cleaned_data.get('senha_login')
        senha_login = Validacao.verifica_senha(senha_login)
        if not senha_login:
            raise forms.ValidationError('Senha inválida')
        return senha_login

class EmpresaFormDois(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'cep',
            'estado',
            'cidade',
            'bairro',
            'rua',
            'numero',
            'complemento',
        ]
        widgets = {
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'rua': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        cep = Validacao.verifica_cep(cep)
        if not cep:
            raise forms.ValidationError('CEP inválido')
        return cep  

class EmpresaFormTres(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome_representante',
            'cpf_representante',
            'telefone_representante',
            'email_representante',
        ]
        widgets = {
            'nome_representante': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cpf_representante': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'telefone_representante': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email_representante': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }

    def clean_nome_representante(self):
        nome_representante = self.cleaned_data.get('nome_representante')
        nome_representante = Validacao.verifica_nome_representante(nome_representante)
        if not nome_representante:
            raise forms.ValidationError('Nome do representante inválido')
        return nome_representante
    
    def clean_cpf_representante(self):
        cpf_representante = self.cleaned_data.get('cpf_representante')
        cpf_representante = Validacao.verifica_cpf(cpf_representante)
        if not cpf_representante:
            raise forms.ValidationError('CPF do representante inválido')
        return cpf_representante
    
    def clean_telefone_representante(self):
        telefone_representante = self.cleaned_data.get('telefone_representante')
        telefone_representante = Validacao.verifica_telefone(telefone_representante)
        if not telefone_representante:
            raise forms.ValidationError('Telefone do representante inválido')
        return telefone_representante

class EmpresaCompleta(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome',
            'cnpj',
            'tipo_empresa',
            'email_login',
            'senha_login',
            'cep', 
            'estado',
            'cidade',
            'bairro',
            'rua',
            'numero',
            'complemento',
            'nome_representante',
            'cpf_representante',
            'telefone_representante',
            'email_representante',
        ]