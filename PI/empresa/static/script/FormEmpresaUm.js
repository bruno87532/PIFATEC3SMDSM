import Form from './Form.js';
import Api from './Api.js'

class FormEmpresaUm extends Form{
    para_json(){
        const dados_um = JSON.stringify({
            nome_empresa: document.getElementById('id_nome_empresa').value,
            cnpj_empresa: document.getElementById('id_cnpj_empresa').value,
            tipo_empresa: document.getElementById('id_tipo_empresa').value,
            email_login_empresa: document.getElementById('id_email_login_empresa').value,
            senha_login_empresa: document.getElementById('id_senha_login_empresa').value
        }) 
        this.api = new Api();
        this.api.envia_etapa(dados_um)
    }
}

const form_um = new FormEmpresaUm('form_um')