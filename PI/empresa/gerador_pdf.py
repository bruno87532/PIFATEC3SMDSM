from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class GeraPDF():
    def __init__(self, tipo_folha, eixo_y):
        self.tipo_folha = tipo_folha
        self.eixo_y = eixo_y
        self.canva = canvas.Canvas('Relatório de doação', pagesize=self.tipo_folha)

    def insere_titulo(self, titulo, fonte, tamanho_fonte, centralizacao):
        self.canva.setFont(fonte, tamanho_fonte)
        if centralizacao == 'esquerda':
            self.canva.drawString(50, self.eixo_y, titulo)
        elif centralizacao == 'centro':
            self.canva.drawString((self.tipo_folha[0] - self.canva.stringWidth(titulo))/2, self.eixo_y, titulo)
        self.eixo_y = (self.eixo_y - 10) - tamanho_fonte

    def insere_texto(self, texto, fonte, tamanho_fonte, largura_maxima, y_menos):
        linhas = []
        linha = ''
        palavras = texto.split()
        self.canva.setFont(fonte, tamanho_fonte)
        TextoFormatado = self.canva.beginText((self.tipo_folha[0] - largura_maxima)/2, self.eixo_y)
        TextoFormatado.setFont(fonte, tamanho_fonte)

        for palavra in palavras:
            if (self.canva.stringWidth(linha + palavra + ' ') <= largura_maxima):
                linha += palavra + ' '
            else:
                linhas.append(linha)
                linha = palavra + ' '
        linhas.append(linha)
        for linha in linhas:
            TextoFormatado.textLine(linha)
        self.canva.drawText(TextoFormatado)
        self.eixo_y = (self.eixo_y - y_menos) - len(linhas) * tamanho_fonte
    
    def subtrai_eixo_y(self, y):
        self.eixo_y -= y

    def insere_linha(self, x_inicio, x_fim):
        self.canva.line(x_inicio, self.eixo_y, x_fim, self.eixo_y)
    
    def salvar(self):
        self.canva.save()


def monta_pdf(nome_empresa, cnpj_empresa, categoria_produto, data_doado_produto, hora_doado_produto, nome_produto, descricao_produto, quantidade_produto, nome_representante_legal, cpf_representante_legal):
    MontaPDF = GeraPDF(A4, 801)
    MontaPDF.insere_titulo('Certificado de doação', 'Helvetica-Bold', 25, 'centro')
    texto = f'Certificamos que a empresa {nome_empresa}, inscrita sob o CNPJ {cnpj_empresa}, realizou uma doação de {categoria_produto} na data {data_doado_produto} as {hora_doado_produto} para a instituição Solidariedade do Campo, inscrita sob o CNPJ 67016422000126.'
    MontaPDF.insere_texto(texto, 'Helvetica', 12, 495, 30)
    MontaPDF.insere_titulo('Detalhes da doação', 'Helvetica-Bold', 19, 'esquerda')
    MontaPDF.insere_titulo('Item doado', 'Helvetica-Bold', 16, 'esquerda')
    MontaPDF.insere_texto(f'• Nome do produto: {nome_produto}', 'Helvetica', 14, 470, 10)
    MontaPDF.insere_texto(f'• Descrição do produto: {descricao_produto}', 'Helvetica', 14, 470, 10)
    MontaPDF.insere_texto(f'• Quantidade doada: {quantidade_produto}', 'Helvetica', 14, 470, 30)
    MontaPDF.insere_titulo('Declaração', 'Helvetica-Bold', 19, 'esquerda')
    texto = 'Esta doação foi realiza com o objetivo de contribuir com ONGS carentes. Este documento dedica-se a registrar a vericidade desta doação para questões legais.'
    MontaPDF.insere_texto(texto, 'Helvetica', 14, 495, 15)
    texto = 'Assinamos este certificado para fins de registros e documentação.'
    MontaPDF.insere_texto(texto, 'Helvetica', 14, 495, 10)
    MontaPDF.insere_linha(50, 545)
    MontaPDF.subtrai_eixo_y(30)
    MontaPDF.insere_titulo('Representante legal da empresa', 'Helvetica-Bold', 19, 'esquerda')
    MontaPDF.insere_texto(f'Nome: {nome_representante_legal}', 'Helvetica', 16, 495, 10)
    MontaPDF.insere_texto(f'CPF: {cpf_representante_legal}', 'Helvetica', 16, 495, 10)
    MontaPDF.insere_texto(f'Data: {data_doado_produto}', 'Helvetica', 16, 495, 25)
    MontaPDF.insere_linha(150, 450)
    MontaPDF.subtrai_eixo_y(20)
    MontaPDF.insere_texto('Assinatura do representante legal', 'Helvetica', 16, 250, 20)
    MontaPDF.insere_linha(50, 545)
    MontaPDF.subtrai_eixo_y(30)
    MontaPDF.insere_titulo('Representante legal da instituição', 'Helvetica-Bold', 19, 'esquerda')
    MontaPDF.insere_texto('Nome: Bruno Henrique Guinerio', 'Helvetica', 16, 495, 10)
    MontaPDF.insere_texto('CPF: 78316354080', 'Helvetica', 16, 495, 10)
    MontaPDF.insere_texto(f'Data: {data_doado_produto}', 'Helvetica', 16, 495, 25)
    MontaPDF.insere_linha(150, 450)
    MontaPDF.subtrai_eixo_y(20)
    MontaPDF.insere_texto('Assinatura do representante legal', 'Helvetica', 16, 250, 20)
    MontaPDF.salvar()