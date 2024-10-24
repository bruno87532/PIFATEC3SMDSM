class Cep {
    constructor(cep){
        this.cep_invalido = document.getElementById('cep_invalido');
        if (cep.length === 8) {
            fetch (`https://viacep.com.br/ws/${cep}/json/`) 
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    if (data.erro) {
                        this.cep_invalido.style.visibility = 'visible';
                        return;
                    }      
                    this.preenche_dados(data)     
                })
        } else {
            this.cep_invalido.style.visibility = 'visible'
        }   
    }
    preenche_dados(dados) {
        if(this.cep_invalido && this.cep_invalido.style.visibility == 'visible') {
            this.cep_invalido.style.visibility = 'hidden'
        }
        rua.value = dados.logradouro;
        bairro.value = dados.bairro;
        cidade.value = dados.localidade;
        estado.value = dados.uf
    }
}
