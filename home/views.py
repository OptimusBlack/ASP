from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, RegistrationTokenForm
from .models import RegistrationToken
from django.contrib.auth.models import User
from clinic_manager.models import ClinicManager

def index(request):
    template = 'home/index.html'
    return HttpResponse(render(request, template))


def login_page(request):
    return HttpResponse("Still under development")


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

            authUser = RegistrationToken.objects.get(token=token)

            # Handle user registration to different types here
            # Note that there will be a switch to django.auth required first

            print(authUser)
            user = User.objects.create_user(username=username, email=authUser.email, password=password, first_name=first_name, last_name=last_name)
            clinic_manager = ClinicManager(user=user, clinic_name=clinic_name)
            user.save()
            clinic_manager.save()

            return HttpResponseRedirect('/')

    else:
        form = RegistrationTokenForm()

    return render(request, 'home/register_token.html', {'form': form})
