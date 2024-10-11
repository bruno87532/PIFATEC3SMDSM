class Api {
    async envia_etapa(dados) {
        try {
            console.log('teste')
            const resposta = await fetch('/empresa', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: dados,
            });
            if (!resposta.ok) {
                throw new Error(`Erro: ${resposta.status}`);
            }
            const resposta_json = await resposta.json();
            console.log(resposta_json)
        } catch (error) {
            console.error('Erro ao enviar dados', error);
        }
    }
}

export default Api;
