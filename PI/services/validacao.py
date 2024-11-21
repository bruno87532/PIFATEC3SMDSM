import re 
from empresa.models import Empresa
from pessoa.models import Pessoa
from ong.models import Ong
import requests
from django.utils import timezone 
from datetime import datetime

class Validacao():

    @staticmethod
    def verifica_campo_vazio(campo):
        if not campo or len(campo) == 0:
            return False
        return campo
    
    @staticmethod
    def verifica_cnpj(cnpj):
        cnpj = ''.join(re.findall(r'\d', cnpj))
        if len(cnpj) != 14:
            return False
        if Empresa.objects.filter(cnpj=cnpj) or Ong.objects.filter(cnpj=cnpj):
            return 'cadastrado'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        r = requests.get(f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}', headers=headers)
        if r.status_code != 200 and r.status_code != 504:
            return False
        return cnpj
    
    @staticmethod
    def verifica_email(email):
        if Empresa.objects.filter(email_login=email) or Pessoa.objects.filter(email_login_pessoa=email) or Ong.objects.filter(email_login=email):
            return 'cadastrado'
        return email
    
    @staticmethod
    def verifica_senha(senha):
        if len(senha) < 8:
            return False
        return senha
    
    @staticmethod 
    def verifica_cep(cep):
        cep = ''.join(re.findall(r'\d', cep))
        if len(cep) != 8:
            return False
        r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if r.status_code != 200 or r.json().get('erro'):
            return False
        return cep
    
    @staticmethod
    def verifica_nome_representante(nome):
        nome = ''.join(re.findall(r'[a-zA-Z\s]', str(nome))).title()
        if not nome:
            return False
        return nome
    
    @staticmethod
    def verifica_cpf(cpf):
        cpf = ''.join(re.findall(r'\d', str(cpf)))
        peso_primeiro_digito = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        peso_segundo_digito = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        soma_primeiro_digito = 0
        soma_segundo_digito = 0
        if len(str(cpf)) != 11:
            return False
        for n, p in zip(str(cpf)[0:9], peso_primeiro_digito):
            soma_primeiro_digito += int(n) * p
        resultado_soma_primeiro_digito = soma_primeiro_digito % 11
        if resultado_soma_primeiro_digito > 1 and not str(11 - resultado_soma_primeiro_digito) == str(cpf)[9]:
            return False
        if (resultado_soma_primeiro_digito == 1 or resultado_soma_primeiro_digito == 0) and str(cpf)[9] != '0':
            return False
        for n, p in zip(str(cpf)[0:10], peso_segundo_digito):
            soma_segundo_digito += int(n) * p
        resultado_soma_segundo_digito = soma_segundo_digito % 11
        if resultado_soma_segundo_digito > 1 and not str(11 - resultado_soma_segundo_digito) == str(cpf)[10]:
            return False
        if (resultado_soma_segundo_digito == 1 or resultado_soma_segundo_digito == 0) and str(cpf)[10] != '0':
            return False
        return cpf
    
    @staticmethod
    def verifica_telefone(telefone):
        telefone = ''.join(re.findall(r'\d', telefone))
        if len(telefone) < 9:
            return False
        return telefone
    
    @staticmethod
    def verifica_data_nascimento(data):
        print(type(data))
        if timezone.now().date().year - data.year < 18:
            return False
        return data
