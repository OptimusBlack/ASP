from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, RegistrationTokenForm, LoginForm
from .models import RegistrationToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as UserDjango
from clinic_manager.models import ClinicManager
from dispatcher.models import Dispatcher
from warehouse.models import WarehousePersonnel


def index(request):
    template = 'home/index.html'
    return HttpResponse(render(request, template))


def logout_page(request):
    logout(request)
    return HttpResponse()


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if ClinicManager.objects.get(user=user) is not None:
                    return HttpResponseRedirect('/clinic_manager/home')
                elif Dispatcher.objects.get(user=user) is not None:
                    return HttpResponseRedirect('/dispatcher/home')
                elif WarehousePersonnel.objects.get(user=user) is not None:
                    return HttpResponseRedirect('/warehouse/home')

            else:
                print("Not authenticated")
            return HttpResponseRedirect('/')

    else:
        form = LoginForm()

    return render(request, 'home/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            import uuid

            token = str(uuid.uuid1())
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            RegistrationToken(token=token, email=email, role=role).save()

            return HttpResponseRedirect('/')

    else:
        form = RegistrationForm()

    return render(request, 'home/register.html', {'form': form})


def register_with_token(request):
    if request.method == 'POST':
        form = RegistrationTokenForm(request.POST)
        if form.is_valid():
            import uuid

            token = form.cleaned_data['token']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            clinic_name = form.cleaned_data['clinic_name']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            auth_user = RegistrationToken.objects.get(token=token)

            # Handle user registration to different types here
            # Note that there will be a switch to django.auth required first

            user_django = UserDjango.objects.create_user(username=username, email=auth_user.email, password=password,
                                                         first_name=first_name, last_name=last_name)
            if auth_user.role == "Clinic Manager":
                clinic_manager = ClinicManager(user=user_django, clinic_name=clinic_name)
                clinic_manager.save()
            elif auth_user.role == "Dispatcher":
                dispatcher = Dispatcher(user=user_django)
                dispatcher.save()
            elif auth_user.role == "Warehouse Personnel":
                warehouse_personnel = WarehousePersonnel(user=user_django)
                warehouse_personnel.save()

            return HttpResponseRedirect('/')

    else:
        form = RegistrationTokenForm()

    return render(request, 'home/register_token.html', {'form': form})
