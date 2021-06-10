from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from .forms import RegisterForm

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

def login(request):
    pass