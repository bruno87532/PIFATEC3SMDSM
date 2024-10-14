import Form from '/static/script/Form.js';
import Api from '/static/script/Api.js'

class FormPessoa extends Form{
    para_json(){
        const dados = JSON.stringify({
            nome_pessoa: document.getElementById('id_nome_pessoa').value,
            cpf_pessoa: document.getElementById('id_cpf_pessoa').value,
            email_login_pessoa: document.getElementById('id_email_login_pessoa').value,
            senha_login_pessoa: document.getElementById('id_senha_login_pessoa').value,
            data_nascimento_pessoa: document.getElementById('id_data_nascimento_pessoa').value,
            telefone_pessoa: document.getElementById('id_telefone_pessoa').value,
        }) 
        this.api = new Api();
        this.api.envia_etapa(dados)
    }
}

document.addEventListener('DOMContentLoaded', function(){
    const form = new FormPessoa('form_pessoa')
});