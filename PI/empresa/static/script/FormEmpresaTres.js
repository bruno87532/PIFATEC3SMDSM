import Form from './Form.js';
import Api from './Api.js';

class FormEmpresaTres extends Form{
    para_json(){
        const dados = JSON.stringify({
            nome_representante_empresa: document.getElementById('id_nome_representante_empresa').value,
            cpf_representante_empresa: document.getElementById('id_cpf_representante_empresa').value,
            telefone_representante_empresa: document.getElementById('id_telefone_representante_empresa').value,
            email_representante_empresa: document.getElementById('id_email_representante_empresa').value,
        }) 
        this.api = new Api();
        this.api.envia_etapa(dados)
    }
}

document.addEventListener('DOMContentLoaded', function(){
    const form = new FormEmpresaTres('form_tres')
});