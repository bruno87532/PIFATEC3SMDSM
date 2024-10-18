// cep.js
document.getElementById('id_cep_empresa').addEventListener('blur', function() {
    var cep = this.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    document.getElementById('id_rua_empresa').value = data.logradouro;
                    document.getElementById('id_bairro_empresa').value = data.bairro;
                    document.getElementById('id_cidade_empresa').value = data.localidade;
                    document.getElementById('id_estado_empresa').value = data.uf;
                } else {
                    alert('CEP não encontrado.');
                }
            })
            .catch(error => {
                console.error('Erro ao buscar o CEP:', error);
            });
    } else {
        alert('CEP inválido. Deve conter 8 dígitos.');
    }
});