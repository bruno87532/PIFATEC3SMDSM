import Form from '/static/script/Form.js';
import Api from '/static/script/Api.js'

class FormEmpresaDois extends Form{
    para_json(){
        const dados = JSON.stringify({
            cep_empresa: document.getElementById('id_cep_empresa').value,
            estado_empresa: document.getElementById('id_estado_empresa').value,
            cidade_empresa: document.getElementById('id_cidade_empresa').value,
            bairro_empresa: document.getElementById('id_bairro_empresa').value,
            rua_empresa: document.getElementById('id_rua_empresa').value,
            numero_empresa: document.getElementById('id_numero_empresa').value,
            complemento_empresa: document.getElementById('id_complemento_empresa').value,
            etapa: 2,
        }) 
        this.api = new Api();
        this.api.envia_etapa(dados, '3')
    }
}

document.addEventListener('DOMContentLoaded', function(){
    const form = new FormEmpresaDois('form_dois')
});