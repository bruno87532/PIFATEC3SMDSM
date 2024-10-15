class Api {
    async envia_etapa(dados, etapa = undefined) {
        try {
            console.log('teste')
            const resposta = await fetch(url_post, {
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
                if (etapa == undefined) {
                    window.location.href = url_get;
                }
                const url_get_dinamico = url_get.replace('0', etapa)
                window.location.href = url_get_dinamico
            }else{
                
            }
        } catch (error) {
            console.error('Erro ao enviar dados', error);
        }
    }
}

export default Api;