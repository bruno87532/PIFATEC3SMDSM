from django.shortcuts import redirect

def login_empresa_requerido(view):
    def verifica_login_empresa(request, *args, **kwargs):
        if 'id_empresa' in request.session:
            return view(request, *args, **kwargs)
        else:
            return redirect('login')
    return verifica_login_empresa