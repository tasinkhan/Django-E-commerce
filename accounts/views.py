from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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

            # User Activation
            current_site = get_current_site(request)
            mail_subject = ('Activate your account using this link')
            message_body = render_to_string('accounts/account_activation_email.html',context={
                'user'      :user,
                'domain'    :current_site,
                'uid'       :urlsafe_base64_encode(force_bytes(user.pk)),
                'token'     :default_token_generator.make_token(user),
            })
            email_to = email
            send_mail = EmailMessage(mail_subject, message_body, to=[email_to])
            send_mail.send()
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

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(ValueError,TypeError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Activation Successfull")
        return redirect('accounts:login')
    else:
        messages.error(request, 'Inavlid activation link')
        return redirect('accounts:register')
