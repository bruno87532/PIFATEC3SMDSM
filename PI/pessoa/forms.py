from django import forms
from pessoa.models import Pessoa

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
        print('A sanitização de nome da pessoa foi executada')
        return nome_pessoa
    
    def clean_cpf_pessoa(self):
        cpf_pessoa = self.cleaned_data.get('cpf_pessoa')
        print('A sanitização de cpf da pessoa foi executada')
        return cpf_pessoa

    def clean_telefone_pessoa(self):
        telefone_pessoa = self.cleaned_data.get('telefone_pessoa')
        print('A sanitização de telefone da pessoa foi executada')
        return telefone_pessoa