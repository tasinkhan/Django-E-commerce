from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name       = form.cleaned_data['first_name']
            last_name        = form.cleaned_data['last_name']
            email            = form.cleaned_data['email']
            contact_no       = form.cleaned_data['contact_no']
            password         = form.cleaned_data['password']
            username         = email.split('@')[0]
            user             = Account.objects.create_user(
                            first_name=first_name, last_name=last_name,  email=email, username=username, password=password
                            )
            user.contact_no  = contact_no
            user.save()
            messages.success(request,'Registration Successfull')
            return redirect('accounts:register')

    else:
        form = RegisterForm()
    context={
        'form':form
    }
    return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')