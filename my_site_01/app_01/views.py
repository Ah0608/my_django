import datetime
import random
import re
import time

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from captcha.models import CaptchaStore
from app_01.forms import LoginForm, RegisterForm
from app_01.models import User,EmailVerify
from my_site_01.settings import EMAIL_HOST_USER

'''
上方工具方法，下方视图函数
'''

def index(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    return render(request,'index.html',locals())


@csrf_exempt
def sendmeail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        email_object = User.objects.filter(email=email)
        if email_object:
            message = '您填写的邮箱已注册'
            return render(request, 'register.html', {'message':message})
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
            tip = '验证码发送成功'
            return render(request, 'register.html', {'tip':tip})
        except Exception as e:
            print(e)
            tip = '验证码发送失败'
            return render(request, 'register.html', {'tip':tip})


def register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})  # 显示验证码框
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)  # 把注册表单的数据引过来
        message = "请仔细检查填写内容"
        if register_form.is_valid():  # 若注册表单的数据是有效的
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            confirm_pwd = register_form.cleaned_data.get('confirm_pwd')
            email = register_form.cleaned_data.get('email')
            verifycode = register_form.cleaned_data.get('verifycode')
            sex = register_form.cleaned_data.get('sex')

            if password != confirm_pwd:
                message = '您两次密码输入不同'
                return render(request, 'register.html', locals())


            try:
                email_object = EmailVerify.objects.get(email_add=email,verify_code=verifycode,is_used=True)
                if email_object:
                    current_timestamp = int(time.time())
                    if email_object.expiration_time - current_timestamp < 0:
                        message = '验证码失效，请重新发送'
                        return render(request, 'register.html', locals())
            except:
                message = '验证码有误，请重新尝试'
                return render(request, 'register.html', locals())
            new_user = User()
            new_user.name = username
            new_user.password = make_password(password,salt='sc')
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            EmailVerify.objects.filter(email_add=email).update(is_used=False)
            message = '成功注册'
            time.sleep(3)
            return redirect('/login/')
        else:
            return render(request, 'register.html', locals())
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def Login(request):
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request,'login.html',{'login_form':login_form})
    if request.method=='POST':
        login_form = LoginForm(request.POST)#从Usr表单中获取信息
        message = '请仔细检查您的输入！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password_new = login_form.cleaned_data.get('password')
            try:
                user= User.objects.get(name=username) #验证模板中的已存在用户与当前登录的用户是否一样
            except:
                message='您的账号不存在!'
                return render(request,'login.html',locals()) #若为不同，则继续在此页面进行登录
            if check_password(password_new,user.password):#若密码也正确的话，就跳转至主页
                request.session['is_login'] = True #将当前登录状态写入session字典
                request.session['user_id'] = user.id #将当前登录数据写入session字典
                request.session['user_name'] = user.name #将当前登录数据写入session字典
                request.session.set_expiry(1 * 12 * 3600)
                time.sleep(2)
                return redirect('/index/')
            else:
                message = '您的密码输入有误!'
                return render(request, 'login.html',locals())
    login_form = LoginForm()
    return render(request,'login.html',locals())


def logout(request):
    request.session.flush() # 清除session数据
    return redirect('/login/')


def checkusername(request):
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

def verifypassword(request):
    password = request.GET.get('password', None)
    data = dict()
    if re.search(r'\d', password) and re.search(r'[a-zA-Z]', password):
        if 8 <= len(password) <= 16:
            data['flag'] = True
            data['message'] = '密码合法'
        else:
            data['flag'] = False
            data['message'] = '密码长度应在8到16之间'
    else:
        data['flag'] = False
        data['message'] = '密码须同时包含至少一个字母和一个数字'
    return JsonResponse(data)

