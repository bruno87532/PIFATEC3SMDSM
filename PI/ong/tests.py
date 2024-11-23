from django.test import TestCase
from django.urls import reverse
from ong.models import Ong

class GET_redireciona_correto_cadastro(TestCase):
    def test_rota_1(self):
        resposta = self.client.get(reverse('onggetcad', kwargs={'etapa': 1}))
        self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
    def test_rota_2_redireciona_1(self):
        resposta = self.client.get(reverse('onggetcad', kwargs={'etapa': 2}), follow=True)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois_ong.html')
        self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
    def test_rota_2_redireciona_1(self):
        resposta = self.client.get(reverse('onggetcad', kwargs={'etapa': 3}), follow=True)
        self.assertTemplateNotUsed(resposta, 'cadastro_tres_ong.html')
        self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
 
class cadastra_dados_correto_cadastro(TestCase):
    def test_cadastro(self):
        self.dados = {'nome': 'Cruz Vermelha', 'cnpj': '33651803000165', 'email_login': 'cruzvermelhacontato@gmail.com', 'senha_login': '123456789', 'objetivo_ong': 'Salvar vidas ao redor do mundo', 'etapa1': '1'}
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('onggetcad', kwargs={'etapa': 2}))
        self.dados = {'cep': '13610827', 'estado': 'SP', 'cidade': 'Leme', 'bairro': 'Jardim do Sol', 'rua': 'Maria Fercem', 'numero': '232', 'complemento': 'bloco 8 ap 104', 'etapa2': '2'}
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('onggetcad', kwargs={'etapa': 3}))
        self.dados = {'nome_representante': 'Bruno Henrique Guinerio', 'cpf_representante': '53165382000', 'telefone_representante': '19982869853', 'email_representante': 'teste@gmail.com', 'etapa3': '3'}
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('login'))
        self.assertEqual(Ong.objects.count(), 1)
 
class cadastra_dados_errado_etapa_1_cadastro(TestCase):
    def setUp(self):
        self.dados = {'nome': 'Cruz Vermelha', 'cnpj': '123', 'email_login': 'cruzvermelhacontato@gmail.com', 'senha_login': '123456789', 'objetivo_ong': 'Salvar vidas ao redor do mundo', 'etapa1': '1'}
    def test_errado_etapa_1_cnpj(self):
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois_ong.html')
        self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
        self.assertContains(resposta, 'CNPJ inválido', status_code=400)
        self.assertNotContains(resposta, 'Senha inválida', status_code=400)
    def test_errado_etapa_1_senha(self):
        self.dados['senha_login'] = '123'
        self.dados['cnpj'] = '45997418001710'
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois_ong.html')
        self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
        self.assertContains(resposta, 'Senha inválida', status_code=400)
        self.assertNotContains(resposta, 'CNPJ inválido', status_code=400)
    def test_errado_etapa_1_cnpj_senha(self):
        self.dados['senha_login'] = '123'
        self.dados['cnpj'] = '123'
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois_ong.html')
        self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
        self.assertContains(resposta, 'Senha inválida', status_code=400)
        self.assertContains(resposta, 'CNPJ inválido', status_code=400)
 
class cadastra_dados_errado_etapa_2_cadastro(TestCase):
    def test_errado_etapa_2_cep(self):
        self.dados = {'cep': '11111111', 'estado': 'SP', 'cidade': 'Leme', 'bairro': 'Jardim do Sol', 'rua': 'Maria Fercem', 'numero': '232', 'complemento': 'bloco 8 ap 104', 'etapa2': '2'}
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertTemplateNotUsed('cadastro_tres_ong.html')               
        self.assertTemplateUsed('cadastro_dois_ong.html') 
        self.assertContains(resposta, 'CEP inválido', status_code=400)              

class cadastra_dados_errado_etapa_3_cadastro(TestCase):
    def setUp(self):
        self.dados =  {'nome_representante': 'Gabriel Cardoso Schranck', 'cpf_representante': '123', 'telefone_representante': '19982869853', 'email_representante': 'teste@gmail.com', 'etapa3': '3'}
    def test_errado_etapa_3_cpf(self):
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres_ong.html')
        self.assertContains(resposta, 'CPF do representante inválido', status_code=400)
        self.assertNotContains(resposta, 'Telefone do representante inválido', status_code=400)
    def test_errado_etapa_3_telefone(self):
        self.dados['cpf_representante'] = '33787357084'
        self.dados['telefone_representante'] = '123'
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres_ong.html')
        self.assertNotContains(resposta, 'CPF do representante inválido', status_code=400)
        self.assertContains(resposta, 'Telefone do representante inválido', status_code=400)
    def test_errado_etapa_3_cpf_telefone(self):
        self.dados['telefone_representante'] = '123'
        resposta = self.client.post(reverse('ongpostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres_ong.html')
        self.assertContains(resposta, 'CPF do representante inválido', status_code=400)
        self.assertContains(resposta, 'Telefone do representante inválido', status_code=400)