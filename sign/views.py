from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from sign.models import BaseRegisterForm, OneTimeCode
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from sign.forms import VerifyForm
from string import ascii_letters, digits
from random import choice
from django.contrib import messages

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            allowed_chars = ''.join((ascii_letters, digits))
            otp_code = ''.join(choice(allowed_chars) for _ in range(5))
            print(user)
            print(otp_code)
            OneTimeCode.objects.create(user=user, code=otp_code)
            return redirect('verify')
    return render(request, 'sign/login.html', {'form': form})

def verify_view(request):
    form = VerifyForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        try:
            user_code = OneTimeCode.objects.get(user=user)
        except:
            messages.error(request, 'Ваш код устарел')
            return redirect('login')

        if not request.POST:
            email = user.email
            message_body = f'Уважаемый {user.username}, ваш одноразовый пароль для входа {user_code}. Используйте этот пароль для проверки.'
            send_mail(message=message_body, from_email='romanags@yandex.ru', subject='Одноразовый код', recipient_list=[email])
        if form.is_valid():
            enter_code = form.cleaned_data.get('code')
            if str(user_code) == enter_code:
                user_code.save()
                login(request, user)
                OneTimeCode.objects.get(user=user).delete()
                return redirect('/')
            else:
                return redirect('login')
    return render(request, 'sign/verify.html', {'form': form})

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
