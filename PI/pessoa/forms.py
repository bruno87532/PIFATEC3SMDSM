from django import forms
from pessoa.models import Pessoa
from empresa.models import Empresa
from datetime import date
from django.utils import timezone
import re 
from services.validacao import Validacao

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = [
            'nome_pessoa',
            'cpf_pessoa',
            'email_login_pessoa',
            'senha_login_pessoa',
            'data_nascimento_pessoa',
            'telefone_pessoa'
        ]
        widgets = {
            'nome_pessoa': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cpf_pessoa': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '14',
                'oninput': "this.value=this.value.replace(/[^0-9]/g,'');",
            }),
            'email_login_pessoa': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'senha_login_pessoa': forms.PasswordInput(attrs={
                'type': 'password',
                'minlength': '8',
                'class': 'form-control',
            }),
            'data_nascimento_pessoa': forms.DateInput(attrs={
                'type': 'date',
                'min': '1900-01-01',
                'max': date.today(),
                'onkeydown': 'return false',
                'class': 'form-control',
            }),
            'telefone_pessoa': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '15',
                'oninput': "this.value=this.value.replace(/[^0-9]/g,'');",
            }),
        }
    
    def clean_nome_pessoa(self):
        nome_pessoa = self.cleaned_data.get('nome_pessoa')
        nome_pessoa = Validacao.verifica_nome_representante(nome_pessoa)
        if not nome_pessoa:
            raise forms.ValidationError('Nome inválido')
        return nome_pessoa
    
    def clean_cpf_pessoa(self):
        cpf_pessoa = self.cleaned_data.get('cpf_pessoa')
        if Pessoa.objects.filter(cpf_pessoa=cpf_pessoa):
            raise forms.ValidationError('CPF já cadastrado')
        cpf_pessoa = Validacao.verifica_cpf(cpf_pessoa)
        if not cpf_pessoa:
            raise forms.ValidationError('CPF inválido')
        return cpf_pessoa

    def clean_email_login_pessoa(self):
        email_login_pessoa = self.cleaned_data.get('email_login_pessoa')
        if Pessoa.objects.filter(email_login_pessoa=email_login_pessoa) or Empresa.objects.filter(email_login=email_login_pessoa):
            raise forms.ValidationError('Email já cadastrado')
        return email_login_pessoa
        
    def clean_senha_login_pessoa(self):
        senha_login_pessoa = self.cleaned_data.get('senha_login_pessoa')
        senha_login_pessoa = Validacao.verifica_senha(senha_login_pessoa)
        if not senha_login_pessoa:
            raise forms.ValidationError('Senha inválida')
        return senha_login_pessoa

    def clean_telefone_pessoa(self):
        telefone_pessoa = self.cleaned_data.get('telefone_pessoa')
        telefone_pessoa = Validacao.verifica_telefone(telefone_pessoa)
        if not telefone_pessoa:
            raise forms.ValidationError('Número de telefone inválido')
        return telefone_pessoa
    
    def clean_data_nascimento_pessoa(self):
        data_nascimento_pessoa = self.cleaned_data.get('data_nascimento_pessoa')
        data_nascimento_pessoa = Validacao.verifica_data_nascimento(data_nascimento_pessoa)
        if not data_nascimento_pessoa:
            raise forms.ValidationError('É necessário ser maior de idade')
        return data_nascimento_pessoa