from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from.models import Pet

@login_required(login_url='/login/')
def register_pet(request):
    return render(request, 'register-pet.html')

@login_required(login_url='/login/')
def set_pet(request):
    city = request.POST.get('city')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    description = request.POST.get('description')
    photo = request.FILES.get('file')
    user = request.user
    pet = Pet.objects.create(email=email, phone=phone, description=description,
                            photo=photo, user=user, city=city)
    return redirect('/')

@login_required(login_url='/login/')
def list_all_pets(request):
    pet  = Pet.objects.filter(active=True)
    return render(request, 'list.html', {'pet':pet})

def list_user_pets(request):
    pet = Pet.objects.filter(active=True, user=request.user)
    return render(request, 'list.html', {'pet':pet})

def pet_detail(request, id):
    pet=Pet.objects.get(active=True, id=id)
    return render (request, 'pet.html',{'pet':pet})

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    print(request.user)
    logout(request)
    return redirect ('/login/')
@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,'Usuario ou senha inválido.')
    return redirect('/login/')