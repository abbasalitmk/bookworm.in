from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser as User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.conf import settings
from twilio.rest import Client
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from django.contrib.auth.forms import PasswordResetForm
import pyotp


def send_otp(request, phone):

    otp = random.randint(1000, 9999)
    request.session['otp'] = otp
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=('+91{}'.format(phone))
    )


def resend_otp(request, phone):
    phone = request.session['phone']
    otp = random.randint(1000, 9999)
    request.session['otp'] = otp
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=('+91{}'.format(phone))
    )
    return redirect('verifi-otp')


@never_cache
def register(request):

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if name == '' or email == '' or phone == '' or password == '':
            messages.error(request, "Fields can't be blank")
            return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exist!')

            elif User.objects.filter(phone=phone).exists():
                messages.error(request, 'Phone already exist!')
            else:
                user = User.objects.create_user(phone=phone, password=password)
                user.first_name = name
                user.email = email
                user.save()

                if user.is_verified:
                    messages.success(request, 'Phone verified')
                    return redirect('login')
                else:
                    send_otp(request, phone)
                    request.session['phone'] = phone
                    return redirect('verify-otp')

    return render(request, 'register.html')


@never_cache
def verify_otp(request):
    if 'otp' not in request.session:
        return redirect('home')

    if request.user.is_authenticated:
        return redirect('profile')

    error = ''
    if request.method == 'POST':
        otp = request.session['otp']
        print(f'otp is{otp}')
        user_otp = request.POST['user_otp']

        if user_otp != '':
            phone = request.session['phone']

            if 'otp' in request.session and int(user_otp) == int(request.session['otp']):
                print(f'user otp is{user_otp}')

                user = User.objects.get(phone=phone)
                user.is_verified = True
                user.save()
                del request.session['otp']
                del request.session['phone']
                messages.success(
                    request, 'Phone verified, please login to continue')
                return redirect('login')
            else:
                return render(request, 'verify-otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verify-otp.html', {'error': error})


@ never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = ''
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        if phone == '' or password == '':
            messages.error(request, "Fields can't be blank")
            return redirect('login')
        else:
            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    return redirect('profile')
                else:
                    send_otp(request, user.phone)
                    return redirect('verify-otp')
            else:
                messages.error(request, 'Invalid login details!')

    return render(request, 'login.html', {'error': error})


@ never_cache
def signout(request):
    logout(request)
    return redirect('home')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if email == '':
            messages.error(request, "Fields can't be blank")
            return redirect('forgot_password')
        else:
            if User.objects.filter(email=email).exists():
                totp = pyotp.TOTP(settings.OTP_SECRET)
                otp = totp.now()
                msg_html = render_to_string(
                    'accounts/templates/email.html', {'otp': otp})

                send_mail(f'Please verify your E-mail', f'Your One-Time Verification Password is {otp}', settings.EMAIL_HOST_USER, [
                    email], html_message=msg_html, fail_silently=False)

                request.session['otp'] = otp
                request.session['email'] = email
                return redirect('verify-email')
            else:
                messages.error(request, 'email does not exist')

    return render(request, 'forgot_password.html')


@never_cache
def verify_email(request):
    if 'otp' not in request.session:
        return redirect('home')

    if request.user.is_authenticated:
        return redirect('profile')

    error = ''
    if request.method == 'POST':
        otp = request.session['otp']
        user_otp = request.POST['user_otp']

        if user_otp != '':
            email = request.session['email']

            if 'otp' in request.session and int(user_otp) == int(request.session['otp']):

                user = User.objects.get(email=email)

                return render(request, 'reset_password.html')
            else:
                return render(request, 'verify-email.html', {'error': 'Invalid OTP'})
    return render(request, 'verify-email.html', {'error': error})


@never_cache
def reset_password(request):
    if 'otp' not in request.session:
        return redirect('home')

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('conf-password')
        if not password or not confirm:
            messages.error(request, "Fields can't be blank")
        else:
            email = request.session['email']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            del request.session['otp']
            del request.session['email']
            messages.success(request, 'Password reset successfuly')
            return redirect('login')

    return render(request, 'reset_password.html')
