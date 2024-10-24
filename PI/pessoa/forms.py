from django import forms
from pessoa.models import Pessoa
from datetime import date
from django.utils import timezone
import re 

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
            'data_nascimento_pessoa': forms.DateInput(attrs={'type': 'date',
                                                             'min': '1900-01-01',
                                                             'max': date.today(),
                                                             'onkeydown': 'return false',
                                                             }),
            'senha_login_pessoa': forms.PasswordInput(attrs={'type': 'password',})
        }
    
    def clean_nome_pessoa(self):
        nome_pessoa = self.cleaned_data.get('nome_pessoa')
        nome_pessoa = ''.join(re.findall(r'[a-zA-Z\s]', str(nome_pessoa))).title()
        if not nome_pessoa:
            raise forms.ValidationError('Nome inválido')
        return nome_pessoa
    
    def clean_cpf_pessoa(self):
        cpf_pessoa = self.cleaned_data.get('cpf_pessoa')
        if Pessoa.objects.filter(cpf_pessoa=cpf_pessoa):
            raise forms.ValidationError('CPF já cadastrado')
        cpf_pessoa = ''.join(re.findall(r'\d', str(cpf_pessoa)))
        peso_primeiro_digito = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        peso_segundo_digito = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        soma_primeiro_digito = 0
        soma_segundo_digito = 0
        if len(str(cpf_pessoa)) != 11:
            raise forms.ValidationError('CPF inválido')
        for n, p in zip(str(cpf_pessoa)[0:9], peso_primeiro_digito):
            soma_primeiro_digito += int(n) * p
        resultado_soma_primeiro_digito = soma_primeiro_digito % 11
        if resultado_soma_primeiro_digito > 1 and not str(11 - resultado_soma_primeiro_digito) == str(cpf_pessoa)[9]:
            raise forms.ValidationError('CPF inválido!')
        if (resultado_soma_primeiro_digito == 1 or resultado_soma_primeiro_digito == 0) and str(cpf_pessoa)[9] != '0':
            raise forms.ValidationError('CPF inválido!')
        for n, p in zip(str(cpf_pessoa)[0:10], peso_segundo_digito):
            soma_segundo_digito += int(n) * p
        resultado_soma_segundo_digito = soma_segundo_digito % 11
        if resultado_soma_segundo_digito > 1 and not str(11 - resultado_soma_segundo_digito) == str(cpf_pessoa)[10]:
            raise forms.ValidationError('CPF inválido!')
        if (resultado_soma_segundo_digito == 1 or resultado_soma_segundo_digito == 0) and str(cpf_pessoa)[10] != '0':
            raise forms.ValidationError('CPF inválido!')
        return cpf_pessoa

    def clean_email_login_pessoa(self):
        email_login_pessoa = self.cleaned_data.get('email_login_pessoa')
        if Pessoa.objects.filter(email_login_pessoa=email_login_pessoa):
            raise forms.ValidationError('Email já cadastrado!')
        return email_login_pessoa
        
    def clean_senha_login_pessoa(self):
        senha_login_pessoa = self.cleaned_data.get('senha_login_pessoa')
        if len(senha_login_pessoa) < 8:
            raise forms.ValidationError('Senha inválida')
        return senha_login_pessoa

    def clean_telefone_pessoa(self):
        telefone_pessoa = self.cleaned_data.get('telefone_pessoa')
        telefone_pessoa = ''.join(re.findall(r'\d', str(telefone_pessoa)))
        if len(telefone_pessoa) < 9:
            raise forms.ValidationError('Número de telefone inválido')
        return telefone_pessoa
    
    def clean_data_nascimento_pessoa(self):
        data_nascimento_pessoa = self.cleaned_data.get('data_nascimento_pessoa')
        if timezone.now().date().year - data_nascimento_pessoa.year < 18:
            raise forms.ValidationError('Data de nascimento inválida')
        return data_nascimento_pessoa