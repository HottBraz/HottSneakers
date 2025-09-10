from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

class Login(View):

    def get(self, request):
        contexto = {}
        return render(request, 'login.html', contexto)