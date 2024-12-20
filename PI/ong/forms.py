from django import forms
from ong.models import Ong
from services.validacao import Validacao
from django_select2.forms import Select2Widget

class OngFormUm(forms.ModelForm):
    class Meta:
        model = Ong
        fields = [
            'nome',
            'cnpj',
            'objetivo_ong',
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
            'objetivo_ong': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email_login': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'senha_login': forms.PasswordInput(attrs={
                'class': 'form-control',
                'type': 'password',
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

class OngFormDois(forms.ModelForm):
    class Meta:
        model = Ong
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

class OngFormTres(forms.ModelForm):
    class Meta:
        model = Ong
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

class OngCompleta(forms.ModelForm):
    class Meta:
        model = Ong
        fields = [
            'nome',
            'cnpj',
            'objetivo_ong',
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
