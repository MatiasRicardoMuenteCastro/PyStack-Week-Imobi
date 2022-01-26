from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Imovei,Cidade,Visitas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

@login_required(login_url = "/auth/logar")
def home(request):
    minPrice = request.GET.get("preco_minimo")
    maxPrice = request.GET.get("preco_maximo")
    city = request.GET.get("cidade")
    ty = request.GET.getlist("tipo")

    cidadesFind = Cidade.objects.all()

    if minPrice or maxPrice or city or ty:
        if not minPrice:
            minPrice = 0
        if not maxPrice:
            maxPrice = 99999999999999
        if not ty:
            ty = ["A","C"]
        
        imoveisFind = Imovei.objects.filter(valor__gte = minPrice).filter(valor__lte = maxPrice).filter(tipo_imovel__in = ty).filter(cidade = city)

    else:
        imoveisFind = Imovei.objects.all()

    return render(request,'home.html',{'imoveis':imoveisFind,'cidades':cidadesFind})

def imovel(request,id):
    imovel = get_object_or_404(Imovei,id=id)
    sugestoes = Imovei.objects.filter(cidade = imovel.cidade).exclude(id = id)[:2]
    return render(request,'imovel.html',{'imovel':imovel,'sugestoes':sugestoes})

def agendarVisitas(request):
    user = request.user
    day = request.POST.get("dia")
    hour = request.POST.get("horario")
    id_imovel =  request.POST.get("id_imovel")

    visitas = Visitas(
        imovel_id = id_imovel,
        usuario = user,
        dia = day,
        horario = hour
    )

    visitas.save()

    return redirect('/agendamentos')

def agendamentos(request):
    visitas = Visitas.objects.filter(usuario = request.user)
    return render(request,'agendamentos.html',{'visitas':visitas})

def cancelarAgendamento(request, id):
    visitas = get_object_or_404(Visitas, id = id)
    visitas.status = "C"
    visitas.save()
    return redirect('/agendamentos')