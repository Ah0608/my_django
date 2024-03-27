import datetime
import random
import re
import time

from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app_01.forms import LoginForm, RegisterForm
from app_01.models import User,EmailVerify
from my_site_01.settings import EMAIL_HOST_USER
from rest_framework.views import APIView
from django.contrib.auth.models import User

'''
上方工具方法，下方视图函数
'''

class IndexView(View):
    def get(self,request):
        if not request.session.get('is_login',None):
            return redirect('/login/')
        return render(request,'index.html',locals())

class sendmeail(View):
    def post(self,request):
        email = request.POST.get('email')
        email_object = User.objects.filter(email=email)
        if email_object:
            message = '您填写的邮箱已注册'
            return JsonResponse({'flag':False,'message':message})
        random_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        subject = 'Awesome后台系统用户注册'
        message = '''
        您好！
            欢迎注册Awesome后台系统，您的注册验证码为：{}
            该验证码有效时间为五分钟，请及时进行验证。

        Awesome开发团队
        '''.format(random_code)
        try:
            send_mail(subject=subject,message=message,from_email=EMAIL_HOST_USER,recipient_list=[email,])
            EmailVerify.objects.filter(email_add=email).update(is_used=False)
            current_time = datetime.datetime.now()
            five_minutes_later = current_time + datetime.timedelta(minutes=5)
            five_minutes_later_timestamp = int(five_minutes_later.timestamp())
            EmailVerify.objects.create(email_add=email,verify_code=random_code,expiration_time=five_minutes_later_timestamp,is_used=True)
            message = '验证码发送成功'
            return JsonResponse({'flag':True,'message':message})
        except Exception as e:
            print(e)
            message = '验证码发送失败'
            return JsonResponse({'flag':False,'message':message})

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())
    def post(self,request):
        register_form = RegisterForm(request.POST)  # 把注册表单的数据引过来
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            confirm_pwd = register_form.cleaned_data.get('confirm_pwd')
            email = register_form.cleaned_data.get('email')
            verifycode = register_form.cleaned_data.get('verifycode')
            sex = register_form.cleaned_data.get('sex')
            email_object = EmailVerify.objects.filter(email_add=email, verify_code=verifycode, is_used=True)
            if email_object:
                current_timestamp = int(time.time())
                if email_object.expiration_time - current_timestamp < 0:
                    messages.error(request, '验证码失效，请重新发送')
                    return render(request, 'register.html', locals())
            else:
                messages.error(request, '验证码有误，请重新输入')
                return render(request, 'register.html', locals())
            new_user = User()
            new_user.name = username
            new_user.password = make_password(password,salt='sc')
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            EmailVerify.objects.filter(email_add=email).update(is_used=False)
            time.sleep(1)
            return redirect('login')
        else:
            return render(request, 'register.html', locals())

# 后端用户登录验证
class LoginView(View):
    def get(self,request):
        login_form = LoginForm()
        return render(request,'login.html',locals())
    def post(self,request):
        login_form = LoginForm(request.POST)#从Usr表单中获取信息
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password_new = login_form.cleaned_data.get('password')
            user = User.objects.filter(name=username)
            if not user:
                # messages.error(request, '您输入的账号不存在')
                message = '您输入的账号不存在'
                return render(request, 'login.html',{'login_form':login_form,'message':message})
            if check_password(password_new,user.password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session.set_expiry(1 * 12 * 3600)
                time.sleep(2)
                return redirect('index')
            else:
                # messages.error(request, '您的输入密码有误')
                message = '您的输入密码有误'
                return render(request, 'login.html',{'login_form':login_form,'message':message})
        else:
            # 处理表单验证失败的情况
            return render(request, 'login.html', {'login_form': login_form})


class Logoutview(View):
    def get(self,request):
        request.session.flush() # 清除session数据
        return redirect('/login/')


class CheckUsernameView(View):
    def get(self,request):
        username = request.GET.get('username', None)
        pattern = r'^[\u4e00-\u9fa5a-zA-Z0-9]{1,30}$'
        data = dict()
        if re.search(pattern, username):
            if User.objects.filter(name=username).exists():
                data['flag'] = False
                data['message'] = '该用户名已存在'
            else:
                data['flag'] = True
                data['message'] = '该用户名可用'
        else:
            data['flag'] = False
            data['message'] = '用户名只能包含汉字、数字和英文'
        return JsonResponse(data)

