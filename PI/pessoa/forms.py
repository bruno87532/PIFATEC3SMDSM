from django import forms
from pessoa.models import Pessoa
import re 

# AQUI SERÁ FEITA A SANITAÇÃO DOS DADOS, A VERIFICAÇÃO DE SE ESTAR CORRETOS FAREMOS NO SERIALIZER USANDO DJANGO REST FRAMEWORK

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
    
    def clean_nome_pessoa(self):
        nome_pessoa = self.cleaned_data.get('nome_pessoa')
        nome_pessoa = ''.join(re.findall(r'[a-zA-Z\s]', nome_pessoa)).title()
        return nome_pessoa
    
    def clean_cpf_pessoa(self):
        cpf_pessoa = self.cleaned_data.get('cpf_pessoa')
        cpf_pessoa = ''.join(re.findall(r'\d', cpf_pessoa))
        return cpf_pessoa

    def clean_telefone_pessoa(self):
        telefone_pessoa = self.cleaned_data.get('telefone_pessoa')
        telefone_pessoa = ''.join(re.findall(r'\d', telefone_pessoa))
        return telefone_pessoa