from django import forms
from empresa.models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome_empresa',
            'cnpj_empresa',
            'tipo_empresa',
            'email_login_empresa',
            'senha_login_empresa',
            'cep_empresa',
            'estado_empresa',
            'cidade_empresa',
            'bairro_empresa',
            'rua_empresa',
            'numero_empresa',
            'complemento_empresa',
            'nome_representante_empresa',
            'cpf_representante_empresa',
            'telefone_representante_empresa',
            'email_representante_empresa',
        ]
        