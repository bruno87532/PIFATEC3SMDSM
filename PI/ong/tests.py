# from django.test import TestCase
# from django.urls import reverse
# from ong.models import Ong

# class BaseTestCase(TestCase):
#     def setUp(self):
#         self.dados_etapa_1 = {
#             'nome': 'Cruz Vermelha',
#             'cnpj': '04359688000151',
#             'email_login': 'cruzvermelhacontato@gmail.com',
#             'senha_login': '123456789',
#             'objetivo_ong': 'Salvar vidas',
#             'etapa1': '1'
#         }
#         self.dados_etapa_2 = {
#             'cep': '13610827', 
#             'estado': 'SP', 
#             'cidade': 'Leme', 
#             'bairro': 'Jardim do Sol', 
#             'rua': 'Maria Fercem', 
#             'numero': '232',
#             'complemento': 'bloco 8 ap 104',
#             'etapa2': '2'
#         }
#         self.dados_etapa_3 = {
#             'nome_representante': 'Bruno Henrique Guinerio',
#             'cpf_representante': '85700565080',
#             'telefone_representante': '19982869853',
#             'email_representante': 'brunoguinerio@gmail.com',
#             'etapa3': '3'
#         }
#         return super().setUp()
#     def nao_contem_conteudo(self, resposta, conteudos, status):
#         for conteudo in conteudos:
#             self.assertNotContains(resposta, conteudo, status_code=status)
#     def contem_conteudo(self, resposta, conteudos, status):
#         for conteudo in conteudos:
#             self.assertContains(resposta, conteudo, status_code=status)
#     def cria_ong(self):
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_2)
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_3) 

#     def login_ong(self):
#         self.cria_ong()
#         self.login = {
#             'email': self.dados_etapa_1['email_login'],
#             'senha': self.dados_etapa_1['senha_login']
#         }
#         self.client.post(reverse('login'), self.login)

# class GET_redireciona_correto_cadastro(BaseTestCase):
#     def test_rota_1(self):
#         resposta = self.client.get(reverse('onggetcad', kwargs={'etapa': 1}))
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
#     def test_rota_2_redireciona_1(self):
#         resposta = self.client.get(reverse('onggetcad', kwargs={'etapa': 2}), follow=True)
#         self.assertTemplateNotUsed(resposta, 'cadastro_dois_ong.html')
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
#     def test_rota_2_redireciona_1(self):
#         resposta = self.client.get(reverse('onggetcad', kwargs={'etapa': 3}), follow=True)
#         self.assertTemplateNotUsed(resposta, 'cadastro_tres_ong.html')
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
 
# class cadastra_dados_correto_cadastro(BaseTestCase):
#     def test_cadastro(self):
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.assertEqual(resposta.status_code, 302)
#         self.assertRedirects(resposta, reverse('onggetcad', kwargs={'etapa': 2}))
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_2)
#         self.assertEqual(resposta.status_code, 302)
#         self.assertRedirects(resposta, reverse('onggetcad', kwargs={'etapa': 3}))
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_3)
#         self.assertEqual(resposta.status_code, 302)
#         self.assertRedirects(resposta, reverse('login'))
#         self.assertEqual(Ong.objects.count(), 1)
 
# class cadastra_dados_errado_etapa_1_cadastro(BaseTestCase):
#     def test_errado_etapa_1_cnpj(self):
#         self.dados_etapa_1['cnpj'] = '123'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.assertTemplateNotUsed(resposta, 'cadastro_dois_ong.html')
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
#         self.contem_conteudo(resposta, ['CNPJ inválido'], 400)
#         self.nao_contem_conteudo(resposta, ['Senha inválida'], 400)
#     def test_errado_etapa_1_senha(self):
#         self.dados_etapa_1['senha_login'] = '123'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.assertTemplateNotUsed(resposta, 'cadastro_dois_ong.html')
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
#         self.nao_contem_conteudo(resposta, ['CNPJ inválido'], 400)
#         self.contem_conteudo(resposta, ['Senha inválida'], 400)
#     def test_errado_etapa_1_cnpj_senha(self):
#         self.dados_etapa_1['senha_login'] = '123'
#         self.dados_etapa_1['cnpj'] = '123'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.assertTemplateNotUsed(resposta, 'cadastro_dois_ong.html')
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
#         self.contem_conteudo(resposta, ['Senha inválida', 'CNPJ inválido'], 400)
 
# class cadastra_dados_errado_etapa_2_cadastro(BaseTestCase):
#     def test_errado_etapa_2_cep(self):
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.dados_etapa_2['cep'] = '123'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_2)
#         self.assertTemplateNotUsed('cadastro_tres_ong.html')               
#         self.assertTemplateUsed('cadastro_dois_ong.html') 
#         self.contem_conteudo(resposta, ['CEP inválido'], 400)              

# class cadastra_dados_errado_etapa_3_cadastro(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_2)
#     def test_errado_etapa_3_cpf(self):
#         self.dados_etapa_3['cpf_representante'] = '123'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_3)
#         self.assertTemplateNotUsed(resposta, 'login.html')
#         self.assertTemplateUsed(resposta, 'cadastro_tres_ong.html')
#         self.contem_conteudo(resposta, ['CPF do representante inválido'], 400)
#         self.nao_contem_conteudo(resposta, ['Telefone do representante inválido'], 400)              
#     def test_errado_etapa_3_telefone(self):
#         self.dados_etapa_3['telefone_representante'] = '123'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_3)
#         self.assertTemplateNotUsed(resposta, 'login.html')
#         self.assertTemplateUsed(resposta, 'cadastro_tres_ong.html')
#         self.nao_contem_conteudo(resposta, ['CPF do representante inválido'], 400)
#         self.contem_conteudo(resposta, ['Telefone do representante inválido'], 400)
#     def test_errado_etapa_3_cpf_telefone(self):
#         self.dados_etapa_3['telefone_representante'] = '123'
#         self.dados_etapa_3['cpf_representante'] = '123'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_3)
#         self.assertTemplateNotUsed(resposta, 'login.html')
#         self.assertTemplateUsed(resposta, 'cadastro_tres_ong.html')
#         self.contem_conteudo(resposta, ['Telefone do representante inválido', 'CPF do representante inválido'], 400)

# class cadastra_dados_repetidos_cadastro(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.cria_ong()
#     def test_dado_cnpj_repetido(self):
#         self.dados_etapa_1['email_login'] = 'teste@gmail.com'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
#         self.nao_contem_conteudo(resposta, ['Email já cadastrado'], 400)
#         self.contem_conteudo(resposta, ['CNPJ já cadastrado'], 400)
#     def test_dado_email_repetido(self):
#         self.dados_etapa_1['cnpj'] = '6322637700018'
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
#         self.contem_conteudo(resposta, ['Email já cadastrado'], 400)
#         self.nao_contem_conteudo(resposta, ['CNPJ já cadastrado'], 400)
#     def test_dado_cnpj_email_repetido(self):
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
#         self.assertTemplateUsed(resposta, 'cadastro_um_ong.html')
#         self.contem_conteudo(resposta, ['Email já cadastrado', 'CNPJ já cadastrado'], 400)

# class cadastra_dados_vazio_cadastro(BaseTestCase):
#     def test_dados_vazio_etapa_1(self):
#         for i in self.dados_etapa_1:
#             self.dados_etapa_1[i] = ''
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.assertEqual(302, resposta.status_code)
#         self.assertRedirects(resposta, reverse('home'))
#     def test_dados_vazio_etapa_2(self):
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         for i in self.dados_etapa_2:
#             self.dados_etapa_2[i] = ''
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_2)
#         self.assertEqual(302, resposta.status_code)
#         self.assertRedirects(resposta, reverse('home'))
#     def test_dados_vazio_etapa_3(self):
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_1)
#         self.client.post(reverse('ongpostcad'), self.dados_etapa_2)
#         for i in self.dados_etapa_3:
#             self.dados_etapa_3[i] = ''        
#         resposta = self.client.post(reverse('ongpostcad'), self.dados_etapa_3)
#         self.assertEqual(302, resposta.status_code)
#         self.assertRedirects(resposta, reverse('home'))