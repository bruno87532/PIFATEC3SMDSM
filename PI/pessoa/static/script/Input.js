document.addEventListener('DOMContentLoaded', () => {
    class Input {
        constructor(){
            this.senha = document.getElementById('id_senha_login_pessoa')
        }
        MostraSenha() {
            if (this.senha.type === 'password'){
                this.senha.type = 'text'
            }else{
                this.senha.type = 'password'
            }
        }
    }

    const input = new Input()
    document.getElementById('img_olho').addEventListener('click', () => {
        input.MostraSenha()
    })
})