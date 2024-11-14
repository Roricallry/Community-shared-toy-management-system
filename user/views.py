from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyexpat.errors import messages

from announce.models import Announcement
from toy.models import Toy
from .forms import *
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
import openpyxl
from .models import CustomUser


def user_login(request):
    if request.method == "GET":
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 使用Django的身份验证系统验证用户
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session["name"] = user.name
            # 确定用户类型并相应地重定向
            if user.type == 0:
                # 重定向到普通用户页面(将“user_dashboard”替换为您的URL名称)
                try:
                    toy_show = Toy.objects.all()
                except Toy.DoesNotExist:
                    toy_show = None
                return render(request, 'toy/home.html', context={'toy_show': toy_show})
            elif user.type == 1:
                # 重定向到管理页面(用你的URL名替换'admin_dashboard')
                return redirect('/login/admin/')
            else:
                # 处理其他用户类型
                return render(request, 'user/login.html', {"error": "User type not recognized"})
        else:
            return render(request, 'user/login.html', {"error": "Invalid username or password"})

def user_login_admin(request):
    return render(request, 'user/admin_dashboard.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # 获取表单数据但不保存到数据库
            user.type = 0  # 设置类型字段为0
            user.password = make_password(user.password)  # 哈希存储密码
            user.save()  # 现在保存到数据库
            return redirect('/login/')  # 注册成功后跳转到登录页面
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def personal_homepage(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'user/personal_homepage.html', context)

def view_donations(request):
    user = request.user
    donations = Toy.objects.filter(toy_donor=user.username)  # 假设 donations 是用户的一个关联字段
    context = {
        'donations': donations
    }
    return render(request, 'user/view_donations.html', context)

@login_required
def admin_info(request):
    users=request.user
    return render(request, 'user/admin_info.html', {'users': users})

@login_required
def change_contact_information(request):
    if request.method == 'POST':
        form = ChangeContactInformationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('personal_homepage')
    else:
        form = ChangeContactInformationForm(instance=request.user)
    return render(request, 'user/personal_homepage.html', {'form': form})

def about_us(request):
    return render(request, 'user/about_us.html')

@login_required  # 导出excel表格
def export_users_to_excel(request):
    user = request.user
    if user.type == 1:  # 涉及到捐赠人，需管理员才有权限打印
        # 创建工作簿和工作表
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Users'

        # 添加表头
        headers = ['用户姓名', '用户名', '邮箱', '电话']
        worksheet.append(headers)

        # 从数据库中获取数据并写入工作表
        users = CustomUser.objects.filter(type=0)
        for user in users:
            worksheet.append(
                [user.name, user.username, user.email, user.phone])

        # 创建HttpResponse对象并设置内容类型
        response = HttpResponse(content_type='application/vnd.malformations-office document.spreadsheet.sheet')
        response['Content-Disposition'] = 'attachment; filename=users.xlsx'

        # 将工作簿保存到响应对象
        workbook.save(response)
        return response
    else:
        return HttpResponse("权限不足！！！")

def manage_owners(request):
    query = request.GET.get('q', '')
    if query:
        users = CustomUser.objects.filter(Q(type=0) & (Q(username__icontains=query) | Q(name__icontains=query)))
    else:
        users = CustomUser.objects.filter(type=0)
    return render(request, 'user/admin_manage.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.telephone = request.POST.get('telephone')
        user.save()
        return redirect('manage_owners')
    return render(request, 'user/edit_user.html', {'user': user})

def reset_password(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        user.set_password('123456')
        user.save()
        return redirect('manage_owners')
    return JsonResponse({'status': 'failed'}, status=400)


def confirm_reset_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user/confirm_reset_password.html', {'user': user})

def default_announce(request):
    announcements = Announcement.objects.all()
    return render(request, 'announce/announcement_default.html',{'announcements': announcements})

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, '用户已成功删除')
    return redirect('manage_owners')
