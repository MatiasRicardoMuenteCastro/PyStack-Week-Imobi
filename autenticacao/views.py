from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request,'cadastro.html')
    elif request.method == "POST":
        user = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("senha")

        if(len(user.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0):
            messages.add_message(request,constants.ERROR,"Preencha todos os campos.")
            return redirect('/auth/cadastro')
        
        userFind = User.objects.filter(username = user)
        
        if (userFind.exists()):
            messages.add_message(request,constants.ERROR,"Usuário já existe.")
            return redirect('/auth/cadastro')
        
        try:
            user = User.objects.create_user(username = user, email = email, password = password)
            user.save()
            messages.add_message(request,constants.SUCCESS,"Usuário criado com sucesso")
            return redirect('/auth/logar')
        except:
            messages.add_message(request,constants.ERROR, "Erro interno do sistema.")
            return redirect('/auth/cadastro')

        

def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request,'logar.html')
    elif request.method == "POST":
        user = request.POST.get("username")
        password = request.POST.get("senha")

        authentication = auth.authenticate(username = user, password = password)

        if (not authentication):
            messages.add_message(request,constants.ERROR,'Usuário e/ou senha incorretos')
            return redirect('/auth/logar')
        else:
            auth.login(request,authentication)
            return redirect('/')

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')