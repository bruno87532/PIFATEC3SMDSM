from django.test import TestCase
from empresa.models import Empresa 
from ong.models import Ong
from pessoa.models import Pessoa
from django.urls import reverse

class GET_redireciona_login(TestCase):
    def test_redireciona_login(self):
        resposta = self.client.get(reverse('login'))
        self.assertTemplateUsed('login.html')

class test_login_empresa(TestCase):
    def setUp(self):
        empresa = Empresa.objects.create(email_login = 'teste_empresa@gmail.com')
        empresa.set_senha('123456789')
        empresa.save()
        return super().setUp()
    def test_errado_login_empresa(self):
        self.login = {'email': 'teste_empresa@gmail.com', 'senha': '12345678910'}
        resposta = self.client.post(reverse('login'), self.login)
        self.assertTemplateNotUsed(resposta, 'index.html')
        self.assertTemplateUsed(resposta, 'login.html')
        self.assertContains(resposta, 'Email ou senha inválidos.', status_code=400)
    def test_correto_login_empresa(self):
        self.login = {'email': 'teste_empresa@gmail.com', 'senha': '123456789'}
        resposta = self.client.post(reverse('login'), self.login) 
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('home'))
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertIn('id_empresa', self.client.session)
    def test_logout_pessoa(self):
        self.login = {'email': 'teste_empresa@gmail.com', 'senha': '123456789'}
        self.client.post(reverse('login'), self.login)
        resposta = self.client.get(reverse('logout'))
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('home'))
        self.assertNotIn('id_empresa', self.client.session)


class test_login_ong(TestCase):
    def setUp(self):
        ong = Ong.objects.create(email_login = 'teste_ong@gmail.com')
        ong.set_senha('123456789')
        ong.save()
        return super().setUp()
    def test_errado_login_ong(self):
        self.login = {'email': 'teste_ong@gmail.com', 'senha': '12345678910'}
        resposta = self.client.post(reverse('login'), self.login)
        self.assertTemplateNotUsed(resposta, 'index.html')
        self.assertTemplateUsed(resposta, 'login.html')
        self.assertContains(resposta, 'Email ou senha inválidos.', status_code=400)
    def test_correto_login_ong(self):
        self.login = {'email': 'teste_ong@gmail.com', 'senha': '123456789'}
        resposta = self.client.post(reverse('login'), self.login)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('home'))
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertIn('id_ong', self.client.session)
    def test_logout_pessoa(self):
        self.login = {'email': 'teste_ong@gmail.com', 'senha': '123456789'}
        self.client.post(reverse('login'), self.login)
        resposta = self.client.get(reverse('logout'))
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('home'))
        self.assertNotIn('id_ong', self.client.session)

class test_login_pessoa(TestCase):
    def setUp(self):
        pessoa = Pessoa.objects.create(email_login_pessoa = 'teste_pessoa@gmail.com')
        pessoa.set_senha('123456789')
        pessoa.save()
        return super().setUp()
    def test_errado_login_pessoa(self):
        self.login = {'email': 'teste_pessoa@gmail.com', 'senha': '12345678910'}
        resposta = self.client.post(reverse('login'), self.login)
        self.assertTemplateNotUsed(resposta, 'index.html')
        self.assertTemplateUsed(resposta, 'login.html')
        self.assertContains(resposta, 'Email ou senha inválidos.', status_code=400)
    def test_correto_login_pessoa(self):
        self.login = {'email': 'teste_pessoa@gmail.com', 'senha': '123456789'}
        resposta = self.client.post(reverse('login'), self.login)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('home'))
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertIn('id_pessoa', self.client.session)
    def test_logout_pessoa(self):
        self.login = {'email': 'teste_pessoa@gmail.com', 'senha': '123456789'}
        self.client.post(reverse('login'), self.login)
        resposta = self.client.get(reverse('logout'))
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('home'))
        self.assertNotIn('id_pessoa', self.client.session)