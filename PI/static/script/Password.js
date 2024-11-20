// Password.js
class Password {
    constructor(campo, olhoIcone) {
        this.senha = campo;
        this.olhoIcone = olhoIcone;

        if (this.senha && this.olhoIcone) {
            this.olhoIcone.addEventListener('click', () => this.MostraSenha());
        }
    }

    MostraSenha() {
        if (this.senha.type === 'password') {
            this.senha.type = 'text';
        } else {
            this.senha.type = 'password';
        }
    }

    static inicializar() {
        document.addEventListener('DOMContentLoaded', () => {
            const campoSenhaCadastro = document.getElementById('id_senha_login_pessoa');
            const olhoIconeCadastro = document.getElementById('img_olho');

            const campoSenhaModal = document.getElementById('id_senha_login_modal');
            const olhoIconeModal = document.getElementById('img_olho_login');

            if (campoSenhaCadastro && olhoIconeCadastro) {
                new Password(campoSenhaCadastro, olhoIconeCadastro);
            }

            if (campoSenhaModal && olhoIconeModal) {
                new Password(campoSenhaModal, olhoIconeModal);
            }
        });
    }
}

Password.inicializar();
