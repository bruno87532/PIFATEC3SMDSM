from django import forms
from empresa.models import Empresa, Doacao
from pessoa.models import Pessoa
import requests
import re
from services.validacao import Validacao

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
            # 'quantidade_produto': forms.NumberInput(attrs={
            #                                         'type': 'number',
            #                                         'step': '0.1',
            #                                         'min': '0',
            #                                         'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57 || event.charCode == 46 || event.charCode == 44'
            #                                         }),
            'nome_produto': forms.TextInput(attrs={
                'class': 'form-control',
            })
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
            raise forms.ValidationError('A quantidade deve ser inteira para valores unitários')

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
            }),
        }
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        nome = Validacao.verifica_campo_vazio(nome)
        if not nome:
            raise forms.ValidationError('Nome inválido')
        return nome

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        cnpj = Validacao.verifica_cnpj(cnpj)
        if not cnpj:
            raise forms.ValidationError('CNPJ inválido')
        if cnpj == 'cadastrado':
            raise forms.ValidationError('CNPJ já cadastrado')
        return cnpj
    
    def clean_tipo_empresa(self):
        tipo_empresa = self.cleaned_data.get('tipo_empresa')
        tipo_empresa = Validacao.verifica_campo_vazio(tipo_empresa)
        if not tipo_empresa:
            raise forms.ValidationError('Tipo de empresa inválido')
        return tipo_empresa

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
    
    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        estado = Validacao.verifica_campo_vazio(estado)
        if not estado:
            raise forms.ValidationError('Estado inválido')
        return estado
    
    def clean_cidade(self):
        cidade = self.cleaned_data.get('cidade')
        cidade = Validacao.verifica_campo_vazio(cidade)
        if not cidade:
            raise forms.ValidationError('Cidade inválida')
        return cidade
    
    def clean_bairro(self):
        bairro = self.cleaned_data.get('bairro')
        bairro = Validacao.verifica_campo_vazio(bairro)
        if not bairro:
            raise forms.ValidationError('Bairro inválido')
        return bairro
    
    def clean_rua(self):
        rua = self.cleaned_data.get('rua')
        rua = Validacao.verifica_campo_vazio(rua)
        if not rua:
            raise forms.ValidationError('Rua inválida')
        return rua 

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        numero = Validacao.verifica_campo_vazio(numero)
        if not numero:
            raise forms.ValidationError('Número inválido')
        return numero   

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
    
    def clean_email_representante(self):
        email_representante = self.cleaned_data.get('email_representante')
        email_representante = Validacao.verifica_campo_vazio(email_representante)
        if not email_representante:
            raise forms.ValidationError('Email do representante inválido')
        return email_representante
    
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