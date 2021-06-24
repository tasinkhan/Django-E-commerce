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
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.http import HttpResponse

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

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
            current_site    = get_current_site(request)
            mail_subject    = ('Activate your account using this link')
            message_body    = render_to_string('accounts/account_activation_email.html',context={
                'user'      :user,
                'domain'    :current_site,
                'uid'       :urlsafe_base64_encode(force_bytes(user.pk)),
                'token'     :default_token_generator.make_token(user),
            })
            email_to = email
            send_mail = EmailMessage(mail_subject, message_body, to=[email_to])
            send_mail.send()
            # messages.success(request,'Registration Successfull')
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegisterForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)

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

def login_view(request):
    if request.method == 'POST':
        email       = request.POST['email']
        password    = request.POST['password']
        user        = authenticate(request, email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            login(request, user)
            messages.success(request,'You are now logged in ')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def forgot_password(request):
    if request.method == 'POST':
        email       = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user            = Account.objects.get(email__exact=email)
            # Password reset email
            current_site    = get_current_site(request)
            mail_subject    = ('Reset your password')
            message_body    = render_to_string('accounts/password_reset_email.html',context={
                'user'      :user,
                'domain'    :current_site,
                'uid'       :urlsafe_base64_encode(force_bytes(user.pk)),
                'token'     :default_token_generator.make_token(user),
            })
            email_to        = email
            send_mail       = EmailMessage(mail_subject, message_body, to=[email_to])
            send_mail.send()
            messages.success(request,'Password reset email sent successfully')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('accounts:forgot_password')

    return render(request,'accounts/forgot_password.html')

def reset_password_validation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(ValueError,TypeError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('accounts:reset_password')
    else:
        messages.error(request,'this link has been expired')
        return redirect('accounts:login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('accounts:login')
        else:
            messages.error(request,'Password does not match')    
    return render(request,'accounts/reset_password.html')