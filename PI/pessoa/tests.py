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