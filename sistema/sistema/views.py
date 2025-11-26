from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class Login(View):

    def get(self, request):
        contexto = {}
        if request.user.is_authenticated:
            return redirect("/tenis")
        else:
            return render(request, 'login.html', contexto)
    
    def post(self, request):
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)

        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/tenis")
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')
        
class Logout(View):
    
    def get(self, request):
        logout(request)
        return redirect('login')
    
class LoginAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # Log para debug
        print(f"Dados recebidos: {request.data}")
        
        serializer = self.serializer_class(
            data=request.data, 
            context={
                'request': request
            }
        )

        if not serializer.is_valid():
            print(f"Erros de validação: {serializer.errors}")
            
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        })
        