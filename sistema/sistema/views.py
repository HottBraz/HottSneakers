from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

class Login(View):

    def get(self, request):
        contexto = {}
        return render(request, 'login.html', contexto)
    
    def post(self, request):
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)

        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Login realizado com sucesso!')
                #return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')
        
        

