from django.test import TestCase
from datetime import date
from django.urls import reverse
from pessoa.models import Pessoa

class cadastra_dados_correto_pessoa(TestCase):
    def test_cadastro(self):
        self.dados = {'nome_pessoa': 'Bruno Henrique Guinerio', 'cpf_pessoa': '08883681002', 'email_login_pessoa': 'teste@gmail.com', 'senha_login_pessoa': '123456789', 'data_nascimento_pessoa': date(2003, 4, 12), 'telefone_pessoa': '19982869853'}
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertEqual(Pessoa.objects.count(), 1)
        self.assertTemplateNotUsed(resposta, 'cadastro.html')
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('login'))

class cadatra_dados_errado_pessoa(TestCase):
    def setUp(self):
        self.dados = {'nome_pessoa': 'Bruno Henrique Guinerio', 'cpf_pessoa': '123', 'email_login_pessoa': 'teste@gmail.com', 'senha_login_pessoa': '123456789', 'data_nascimento_pessoa': date(2003, 4, 12), 'telefone_pessoa': '19982869853'}
        return super().setUp()
    def test_cadastro_cpf_invalido(self):
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.assertContains(resposta, 'CPF inválido')
        self.assertNotContains(resposta, 'Nome inválido')
        self.assertNotContains(resposta, 'É necessário ser maior de idade')
        self.assertNotContains(resposta, 'Senha inválida')
        self.assertNotContains(resposta, 'Número de telefone inválido')
    def test_cadastro_nome_invalido(self):
        self.dados['nome_pessoa'] = '123'
        self.dados['cpf_pessoa'] = '08883681002'
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.assertNotContains(resposta, 'CPF inválido')
        self.assertContains(resposta, 'Nome inválido')
        self.assertNotContains(resposta, 'É necessário ser maior de idade')
        self.assertNotContains(resposta, 'Senha inválida')
        self.assertNotContains(resposta, 'Número de telefone inválido')
    def test_cadastro_data_nascimento_invalida(self):
        self.dados['cpf_pessoa'] = '08883681002'
        self.dados['data_nascimento_pessoa'] = date(2024, 4, 12)
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.assertNotContains(resposta, 'CPF inválido')
        self.assertNotContains(resposta, 'Nome inválido')
        self.assertContains(resposta, 'É necessário ser maior de idade')
        self.assertNotContains(resposta, 'Senha inválida')
        self.assertNotContains(resposta, 'Número de telefone inválido')
    def test_cadastro_telefone_invalido(self):
        self.dados['cpf_pessoa'] = '08883681002'
        self.dados['telefone_pessoa'] = '123'
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.assertNotContains(resposta, 'CPF inválido')
        self.assertNotContains(resposta, 'Nome inválido')
        self.assertNotContains(resposta, 'É necessário ser maior de idade')
        self.assertNotContains(resposta, 'Senha inválida')
        self.assertContains(resposta, 'Número de telefone inválido')
    def test_cadastro_senha_invalida(self):
        self.dados['cpf_pessoa'] = '08883681002'
        self.dados['senha_login_pessoa'] = '123'
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.assertNotContains(resposta, 'CPF inválido')
        self.assertNotContains(resposta, 'Nome inválido')
        self.assertNotContains(resposta, 'É necessário ser maior de idade')
        self.assertContains(resposta, 'Senha inválida')
        self.assertNotContains(resposta, 'Número de telefone inválido')
