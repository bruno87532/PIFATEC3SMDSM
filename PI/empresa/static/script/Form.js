class Form {
    constructor(form){
        this.form = document.getElementById(form);
        this.iniciar_form()
    }
    iniciar_form(){
        this.form.addEventListener('submit', (event) => this.api(event))
    }
    para_json(){
    }
    api(event){
        event.preventDefault()
        this.para_json()
    }
}

export default Form