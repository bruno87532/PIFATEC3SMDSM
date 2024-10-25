class Password {
    constructor(campo){
        this.senha = campo
    }
    MostraSenha() {
        if (this.senha.type === 'password'){
            this.senha.type = 'text'
        }else{
            this.senha.type = 'password'
        }
    }
}