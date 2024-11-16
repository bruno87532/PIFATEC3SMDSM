from django.test import TestCase
from django.urls import reverse
from empresa.models import Empresa


class GET_redireciona_correto_cadastro(TestCase):
    def test_rota_1(self):
        resposta = self.client.get(reverse('empresagetcad', kwargs={'etapa': 1}))
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
    def test_rota_2_redireciona_1(self):
        resposta = self.client.get(reverse('empresagetcad', kwargs={'etapa': 2}), follow=True)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
    def test_rota_2_redireciona_1(self):
        resposta = self.client.get(reverse('empresagetcad', kwargs={'etapa': 3}), follow=True)
        self.assertTemplateNotUsed(resposta, 'cadastro_tres.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
 
class cadastra_dados_correto_cadastro(TestCase):
    def test_cadastro(self):
        self.dados = {'nome': 'Coca-Cola', 'cnpj': '45997418002601', 'email_login': 'cocacolacontato@gmail.com', 'senha_login': '123456789', 'tipo_empresa': 'sociedade de capital fechado', 'etapa1': '1'}
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('empresagetcad', kwargs={'etapa': 2}))
        self.dados = {'cep': '13610827', 'estado': 'SP', 'cidade': 'Leme', 'bairro': 'Jardim do Sol', 'rua': 'Maria Fercem', 'numero': '232', 'complemento': 'bloco 8 ap 104', 'etapa2': '2'}
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('empresagetcad', kwargs={'etapa': 3}))
        self.dados = {'nome_representante': 'Gabriel Cardoso Schranck', 'cpf_representante': '85700565080', 'telefone_representante': '19982869853', 'email_representante': 'teste@gmail.com', 'etapa3': '3'}
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('login'))
 
class cadastra_dados_errado_etapa_1_cadastro(TestCase):
    def setUp(self):
        self.dados = {'nome': 'Coca-Cola', 'cnpj': '123', 'email_login': 'cocacolacontato@gmail.com', 'senha_login': '123456789', 'tipo_empresa': 'sociedade de capital fechado', 'etapa1': '1'}
    def test_errado_etapa_1_cnpj(self):
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.assertContains(resposta, 'CNPJ inválido')
        self.assertNotContains(resposta, 'Senha inválida')
    def test_errado_etapa_1_senha(self):
        self.dados['senha_login'] = '123'
        self.dados['cnpj'] = '45997418001710'
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.assertContains(resposta, 'Senha inválida')
        self.assertNotContains(resposta, 'CNPJ inválido')
    def test_errado_etapa_1_cnpj_senha(self):
        self.dados['senha_login'] = '123'
        self.dados['cnpj'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.assertContains(resposta, 'Senha inválida')
        self.assertContains(resposta, 'CNPJ inválido')
 
class cadastra_dados_errado_etapa_2_cadastro(TestCase):
    def test_errado_etapa_2_cep(self):
        self.dados = {'cep': '11111111', 'estado': 'SP', 'cidade': 'Leme', 'bairro': 'Jardim do Sol', 'rua': 'Maria Fercem', 'numero': '232', 'complemento': 'bloco 8 ap 104', 'etapa2': '2'}
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertTemplateNotUsed('cadastro_tres.html')               
        self.assertTemplateUsed('cadastro_dois.html') 
        self.assertContains(resposta, 'CEP inválido')              

class cadastra_dados_errado_etapa_3_cadastro(TestCase):
    def setUp(self):
        self.dados =  {'nome_representante': 'Gabriel Cardoso Schranck', 'cpf_representante': '123', 'telefone_representante': '19982869853', 'email_representante': 'teste@gmail.com', 'etapa3': '3'}
    def test_errado_etapa_3_cpf(self):
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres.html')
        self.assertContains(resposta, 'CPF do representante inválido')
        self.assertNotContains(resposta, 'Telefone do representante inválido')
    def test_errado_etapa_3_telefone(self):
        self.dados['cpf_representante'] = '33787357084'
        self.dados['telefone_representante'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres.html')
        self.assertNotContains(resposta, 'CPF do representante inválido')
        self.assertContains(resposta, 'Telefone do representante inválido')
    def test_errado_etapa_3_cpf_telefone(self):
        self.dados['telefone_representante'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres.html')
        self.assertContains(resposta, 'CPF do representante inválido')
        self.assertContains(resposta, 'Telefone do representante inválido')

class GET_redireciona_correto_doacao(TestCase):
    def test_rota_sem_login(self):
        resposta = self.client.get(reverse('empresa_doacao'), follow=True)
        self.assertTemplateNotUsed(resposta, 'doacao_empresa.html')
        self.assertTemplateUsed(resposta, 'login.html')
    def test_rota_com_login(self):
        empresa = Empresa.objects.create(email_login='teste@gmail.com')
        empresa.set_senha('123456789')
        empresa.save()
        self.dados = {'email': 'teste@gmail.com', 'senha': '123456789'}
        resposta = self.client.post(reverse('login'), self.dados)
        resposta = self.client.get(reverse('empresa_doacao'), follow=True)
        self.assertTemplateUsed(resposta, 'doacao_empresa.html')
        self.assertTemplateNotUsed(resposta, 'login.html')

class cadastra_dados_errado_doacao(TestCase):
    def setUp(self):
        empresa = Empresa.objects.create(email_login='teste@gmail.com')
        empresa.set_senha('123456789')
        empresa.save()
        self.dados = {'email': 'teste@gmail.com', 'senha': '123456789'}
        resposta = self.client.post(reverse('login'), self.dados)
        self.dados = {'nome_produto': 'Feijão', 'descricao_produto': 'Feijão broto legal 1kg', 'quantidade_produto': '5.5', 'unidade_medida_produto': 'gramas', 'categoria_produto': 'mercearia'}
    def test_errado_quantidade(self):
        self.dados['quantidade_produto'] = '5.5.5'
        resposta = self.client.post(reverse('empresa_doacao'), self.dados)
        self.assertContains(resposta, 'Quantidade inválida', status_code=400)
        self.assertNotContains(resposta, 'O valor deve ser inteiro para medidas unitária', status_code=400)
    def test_errado_unidade(self):
        self.dados['unidade_medida_produto'] = 'unidade'
        resposta = self.client.post(reverse('empresa_doacao'), self.dados)
        self.assertContains(resposta, 'O valor deve ser inteiro para medidas unitária', status_code=400)
        self.assertNotContains(resposta, 'Quantidade inválida', status_code=400)
    def test_errado_quantidade_unidade(self):
        self.dados['unidade_medida_produto'] = 'unidade'
        self.dados['quantidade_produto'] = '5,5,5'
        resposta = self.client.post(reverse('empresa_doacao'), self.dados)
        self.assertContains(resposta, 'O valor deve ser inteiro para medidas unitária', status_code=400)
        self.assertContains(resposta, 'Quantidade inválida', status_code=400)

class cadastra_dados_correto_doacao(TestCase):
    def test_doacao(self):
        self.dados = {'nome_produto': 'Feijão', 'descricao_produto': 'Feijão broto legal', 'quantidade_produto': '80', 'unidade_medida_produto': 'unidade', 'categoria_produto': 'mercearia'}
        resposta = self.client.post(reverse('empresa_doacao'), self.dados)
        self.assertTemplateNotUsed('doacao_empresa.html')
        self.assertTemplateUsed('index.html')
        ## DPS FAZER TESTE PARA TESTAR GERAÇÃO DE PDF

class cadastra