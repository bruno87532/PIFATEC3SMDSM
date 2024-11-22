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
            this.olhoIcone.innerHTML = '<i class="fas fa-eye"></i>';
        } else {
            this.senha.type = 'password';
            this.olhoIcone.innerHTML = '<i class="fas fa-eye-slash"></i>';
        }
    }

    static inicializar() {
        document.addEventListener('DOMContentLoaded', () => {
            const senhas = document.querySelectorAll('input[type="password"]');
            senhas.forEach(senha => {
                const olhoIcone = senha.closest('.input-group').querySelector('.input-group-text');
                if (olhoIcone) {
                    new Password(senha, olhoIcone);
                }
            });
        });
    }
}

Password.inicializar();
