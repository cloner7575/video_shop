import datetime
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from django.utils.crypto import get_random_string
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout
from django.db.models import Q
from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ConfirmOtpForm, \
    ResendOtpForm
import requests
from dotenv import load_dotenv
import os

load_dotenv()
SMS_API_KEY = os.getenv("SMS_API_KEY")

def send_otp_sms(phone_number, otp):
    header = {
        'ACCEPT': 'application/json',
        'X-API-KEY':SMS_API_KEY
    }
    body = {
        "mobile": phone_number,
        "templateId": 901688,
        "parameters": [
            {
                "name": "CODE",
                "value": otp
            }
        ]
    }

    url = 'https://api.sms.ir/v1/send/verify'
    response = requests.post(url=url, json=body, headers=header)
    res = json.loads(response.text)
    status = res['status']
    return status


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_phone = register_form.cleaned_data.get('phone')
            user_password = register_form.cleaned_data.get('password')

            user: bool = User.objects.filter(phone_number__iexact=user_phone).exists()

            if user:
                register_form.add_error('phone', 'این شماره قبلا ثبت شده است')
                context = {
                    'register_form': register_form
                }
                return render(request, 'account_module/register.html', context)
            else:
                new_user = User(
                    phone_number=user_phone,
                    username=user_phone,
                    is_active=False,
                    otp=get_random_string(length=6, allowed_chars='1234567890'),
                    otp_expire_time=datetime.datetime.now() + datetime.timedelta(minutes=2),
                    otp_sent_block_time=datetime.datetime.now() + datetime.timedelta(minutes=2)
                )
                new_user.set_password(user_password)
                new_user.save()
                status = send_otp_sms(new_user.phone_number, new_user.otp)
                if status:
                    return redirect('confirm_otp_page', phone_number=user_phone)
                else:
                    register_form.add_error('phone', 'خطا در ارسال کد فعال سازی')
                    context = {
                        'register_form': register_form
                    }
                    return render(request, 'account_module/register.html', context)
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_phone = login_form.cleaned_data.get('phone')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(phone_number__iexact=user_phone).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('phone', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('password', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('phone', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)


class ConfirmOtpView(View):
    def get(self, request: HttpRequest, phone_number: str):
        confirm_otp_form = ConfirmOtpForm()
        context = {
            'confirm_otp_form': confirm_otp_form,
            'phone_number': phone_number
        }

        return render(request, 'account_module/confirm_otp.html', context)

    def post(self, request: HttpRequest, phone_number: str):
        confirm_otp_form = ConfirmOtpForm(request.POST)
        if confirm_otp_form.is_valid():
            otp_code = confirm_otp_form.cleaned_data.get('otp')
            date_condition = Q(otp_expire_time__gt=datetime.datetime.now())
            phone_number_condition = Q(phone_number__iexact=phone_number)
            user: User = User.objects.filter(date_condition & phone_number_condition).first()
            if user is not None:
                if user.otp == otp_code:
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return redirect(reverse('home_page'))
                else:
                    confirm_otp_form.add_error('otp', 'کد اشتباه است ')
            else:
                confirm_otp_form.add_error('otp', 'کد تایید منقضی شده است')

        context = {
            'confirm_otp_form': confirm_otp_form,
            'phone_number': phone_number
        }
        return render(request, 'account_module/confirm_otp.html', context)


class ResendOtpView(View):
    def get(self, request: HttpRequest):
        resend_otp_form = ResendOtpForm()
        context = {
            'resend_otp_form': resend_otp_form
        }

        return render(request, 'account_module/resend_otp.html', context)

    def post(self, request: HttpRequest):
        resend_otp_form = ResendOtpForm(request.POST)
        if resend_otp_form.is_valid():
            phone_number = resend_otp_form.cleaned_data.get('phone_number')
            user: User = User.objects.filter(phone_number__iexact=phone_number).first()
            if user is not None:
                if user.is_active:
                    resend_otp_form.add_error('phone_number', 'حساب کاربری شما فعال است')
                else:

                    if user.otp_sent_block_time.strftime('%Y-%m-%d %H:%M:%S') > datetime.datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S'):
                        resend_otp_form.add_error('phone_number',
                                                  'کد تایید برای شما ارسال شده است لطفا بعد از 2 دقیقه دوباره امتحان کنید')

                        context = {
                            'resend_otp_form': resend_otp_form
                        }
                        return render(request, 'account_module/resend_otp.html', context)
                    else:
                        user.otp = get_random_string(length=6, allowed_chars='1234567890')
                        user.otp_expire_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
                        user.otp_sent_block_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
                        user.save()
                        status = send_otp_sms(user.phone_number, user.otp)
                        if status:
                            return redirect(reverse('confirm_otp_page', kwargs={'phone_number': user.phone_number}))
                        else:
                            resend_otp_form.add_error('phone_number', 'خطا در ارسال کد تایید')
                            context = {
                                'resend_otp_form': resend_otp_form
                            }
                            return render(request, 'account_module/resend_otp.html', context)
            else:
                resend_otp_form.add_error('phone_number', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'resend_otp_form': resend_otp_form
        }

        return render(request, 'account_module/resend_otp.html', context)



class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_phone_number = forget_pass_form.cleaned_data.get('phone_number')
            user: User = User.objects.filter(phone_number__iexact=user_phone_number).first()
            if user is not None:
                if user.is_active:
                    if user.otp_sent_block_time.strftime('%Y-%m-%d %H:%M:%S') > datetime.datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S'):
                        forget_pass_form.add_error('phone_number',
                                                  'کد تایید برای شما ارسال شده است لطفا بعد از 2 دقیقه دوباره امتحان کنید')

                        context = {
                            'forget_pass_form': forget_pass_form
                        }
                        return render(request, 'account_module/forgot_password.html', context)
                    else:
                        user.otp = get_random_string(length=6, allowed_chars='1234567890')
                        user.otp_expire_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
                        user.otp_sent_block_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
                        user.save()
                        status = send_otp_sms(user.phone_number, user.otp)
                        if status:

                            return redirect(reverse('reset_password_page', kwargs={'phone_number': user.phone_number}))
                        else:
                            forget_pass_form.add_error('phone', 'خطا در ارسال کد تایید')
                            context = {
                                'forget_pass_form': forget_pass_form
                            }
                            return render(request, 'account_module/forgot_password.html', context)
                else:
                    forget_pass_form.add_error('phone', 'حساب کاربری شما فعال نیست')
            else:

                forget_pass_form.add_error('phone', 'کاربری با مشخصات وارد شده یافت نشد')
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'account_module/forgot_password.html', context)



class ResetPasswordView(View):
    def get(self, request: HttpRequest, phone_number: str):
        user: User = User.objects.filter(phone_number__iexact=phone_number).first()
        if user is None:
            return redirect(reverse('forgot_password_page'))

        reset_pass_form = ResetPasswordForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, phone_number):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(phone_number__iexact=phone_number).first()
        if reset_pass_form.is_valid():
            otp_code = reset_pass_form.cleaned_data.get('otp')
            date_condition = Q(otp_expire_time__gt=datetime.datetime.now())
            phone_number_condition = Q(phone_number__iexact=phone_number)
            user: User = User.objects.filter(date_condition & phone_number_condition).first()
            if user is not None:
                if user.otp == otp_code:
                    user.set_password(reset_pass_form.cleaned_data.get('password'))
                    user.save()
                    return redirect(reverse('login_page'))

                else:
                    reset_pass_form.add_error('otp', 'کد اشتباه است ')
            else:
                reset_pass_form.add_error('otp', 'کد تایید منقضی شده است')

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home_page'))
