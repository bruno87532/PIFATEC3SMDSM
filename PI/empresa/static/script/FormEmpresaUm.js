import Form from '/static/script/Form.js';
import Api from '/static/script/Api.js'

class FormEmpresaUm extends Form{
    para_json(){
        const dados = JSON.stringify({
            nome_empresa: document.getElementById('id_nome_empresa').value,
            cnpj_empresa: document.getElementById('id_cnpj_empresa').value,
            tipo_empresa: document.getElementById('id_tipo_empresa').value,
            email_login_empresa: document.getElementById('id_email_login_empresa').value,
            senha_login_empresa: document.getElementById('id_senha_login_empresa').value,
            etapa: 1,
        }) 
        this.api = new Api();
        this.api.envia_etapa(dados, '2')
    }
}

document.addEventListener('DOMContentLoaded', function(){
    const form = new FormEmpresaUm('form_um')
})