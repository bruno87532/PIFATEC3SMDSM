class Api {
    async envia_etapa(dados, etapa = undefined) {
        try {
            console.log('teste')
            const resposta = await fetch(url_empresa_post, {
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
            if(resposta_json.status === 'sucesso'){
                const url_empresa_get_dinamico = url_empresa_get.replace('0', etapa)
                if (etapa == undefined) {
                    window.location.href = url_empresa_get;
                }
                window.location.href = url_empresa_get_dinamico
            }
        } catch (error) {
            console.error('Erro ao enviar dados', error);
        }
    }
}

export default Api;
