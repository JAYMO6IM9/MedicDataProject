from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, 'account/index.html')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect ('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render (request, 'account/register.html', {'form': form, 'msg':msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_patient:
                login(request, user)
                return redirect('patient')
            elif user is not None and user.is_doctor:
                login(request, user)
                return redirect('doctor')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'account/login.html', {'form': form, 'msg': msg})

def admin(request):
    return render (request, 'account/adminpage.html')

def patient(request):
    return render (request, 'account/patient.html')

def doctor(request):
    return render (request, 'account/doctor.html')

def logoutUser (request):
    logout (request)
    return redirect('login_view')

def editorg(request):
    expgid = int(request.GET.get('expgid', 0))
    expedientesg = ExpedienteG.objects.all()

    if request.method == 'POST':
        expgid = int(request.POST.get('expgid', 0))
        nombreG = request.POST.get('nombreG')
        peso = request.POST.get('peso')
        operaciones = request.POST.get('operaciones')
        lesiones = request.POST.get('lesiones')
        alergias = request.POST.get('alergias')
        enfermedades = request.POST.get('enfermedades')
        tipoSangre = request.POST.get('tipoSangre')
    
        if expgid > 0:
            expedienteg = ExpedienteG.objects.get(pk=expgid)
            expedienteg.nombreG = nombreG
            expedienteg.peso = peso
            expedienteg.operaciones = operaciones
            expedienteg.lesiones = lesiones
            expedienteg.alergias = alergias
            expedienteg.enfermedades = enfermedades
            expedienteg.tipoSangre = tipoSangre
            expedienteg.save()

            return redirect('/?expgid=%i' % expgid)
        else:
            expedienteg = ExpedienteG.objects.create(nombreG=nombreG, peso=peso, operaciones=operaciones, lesiones=lesiones, alergias=alergias, enfermedades=enfermedades, tipoSangre=tipoSangre) 

            return redirect('/?expgid=%i' % expedienteg.id)

    if expgid > 0:
        expedienteg = ExpedienteG.objects.get(pk=expgid)
    else:
        expedienteg = ''

    context = {
        'expgid': expgid,
        'expedientesg' : expedientesg,
        'expedienteg' : expedienteg,
    }
    return render(request, 'account/expedienteg.html', context)

def delete_expedienteg(request, expgid):
    expedienteg = ExpedienteG.objects.get(pk=expgid)
    expedienteg.delete()

    return redirect('/?expgid=0')

