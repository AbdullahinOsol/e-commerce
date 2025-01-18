from django.contrib import messages
from payment.forms import ShippingForm
from . token import user_tokenizer_generate
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string
from payment.models import ShippingAddress, OrderItem
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from . forms import CreateUserForm, LoginForm, UpdateUserForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def register(request):
    form = CreateUserForm()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('account/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),

            })

            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')

    context = {'form': form, 'page': 'register'}

    return render(request, 'account/registration/register.html', context=context)

def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('email-verification-success')
    
    else:
        return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')

def my_login(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('home')


        else:
            messages.error(request, 'Invalid username or password.')
            
    context = {'form': form, 'page': 'login'}

    return render(request, 'account/my-login.html', context=context)

def my_logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')

@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')

@login_required(login_url='my-login')
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your username was successfully updated!')
            return redirect('profile-management')
        
    context = {'user_form': user_form}

    return render(request, 'account/profile-management.html', context=context)

@login_required(login_url='my-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Your account was deleted successfully!')
        return redirect('home')

    return render(request, 'account/delete-account.html')

@login_required(login_url='my-login')
def manage_shipping(request):
    try:
        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()

            messages.success(request, 'Your shipping address was successfully updated!')
            return redirect('profile-management')
        
    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context=context)

@login_required(login_url='my-login')
def track_orders(request):

    try:
        orders = OrderItem.objects.filter(user=request.user)
        context = {'orders': orders}
        return render(request, 'account/track-orders.html', context=context)

    except:
        return render(request, 'account/track-orders.html')
    

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile-management')  # Redirect to your account settings page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'account/password/change-password.html', {'form': form})