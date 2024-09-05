from django.shortcuts import render
from django.contrib import messages
from .database import register_user, login_user

def index_view(request):
    user_data = None

    if request.method == 'POST':
        form_type = request.POST.get('type')

        if form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = login_user(email, password)

            if user:
                # Armazenar informações do usuário na sessão
                user_data = {
                    'name': user.get('name'),
                    'email': user.get('email'),
                    #'role': user.get('role') or 'user'
                    'isAdmin': user.get('isAdmin')
                }
                request.session['user'] = user_data
                messages.success(request, 'Login efetuado com sucesso')
            else:
                messages.error(request, 'Erro ao efetuar login')
        
        elif form_type == 'register':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Passwords não coincidem')
            else:
                try:
                    register_user(name, email, password)
                    messages.success(request, 'Registo efetuado com sucesso')
                except Exception as e:
                    messages.error(request, f'Erro ao efetuar registo: {e}')
        else:
            messages.error(request, 'Tipo de pedido inválido')

    return render(request, 'login/index.html', {'user': user_data})
