from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from scrapy.spidermiddlewares.httperror import HttpError

from borrow.models import Borrow
from toy_type.models import Toy_type
from .models import Toy
from django.db.models import Q, Count
from django.core.paginator import Paginator
# Create your views here.
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import openpyxl

def index(request):  # 首页
    user = request.user
    if user.is_authenticated:
        if (user.type == 1):
            return render(request, 'user/admin_dashboard.html')
        # 获取玩具详细信息
    # 先执行查询，并将结果转换为列表
    toy_borrow_counts = list(Borrow.objects
                             .values('toy_id')
                             .annotate(borrow_count=Count('id'))
                             .order_by('-borrow_count')[:3])

    # 提取 toy_id 列表
    toy_ids = [item['toy_id'] for item in toy_borrow_counts]

    # 使用 toy_id 列表进行过滤
    toy_show = Toy.objects.filter(id__in=toy_ids)
    return render(request, 'toy/home.html', context={'toy_show': toy_show})


def toy_list(request):
    user = request.user
    toy_types = Toy_type.objects.all()  # 查询所有玩具类型
    toy_ages = Toy.objects.values_list('applicable_age', flat=True).distinct()  # 查询所有玩具适用年龄，并去重
    selected_type = request.GET.get('type', '')
    selected_age = request.GET.get('age', '')
    status = request.GET.get('status', '')

    toys = Toy.objects.all()

    # 筛选条件
    if selected_type:
        toys = toys.filter(type=selected_type)
    if selected_age:
        try:
            # selected_age 转换为整数并使用 applicable_age__gte=selected_age 作为过滤条件，
            selected_age = int(selected_age)
            # __gte 是 Django ORM 中的一个查询运算符，表示 "大于或等于"。
            toys = toys.filter(applicable_age__gte=selected_age) # toys = toys.filter(applicable_age=selected_age)
        except ValueError:
            pass  # 如果selected_age不能转换为整数，则不做过滤
    if status:
        toys = toys.filter(status=status)

    # 分页
    paginator = Paginator(toys, 10)  # 每页显示10个玩具
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) # page_obj是一个玩具对象的集合，它表示当前页面的玩具列表

    context = {
        'toy_types': toy_types,
        'toy_ages': toy_ages,
        'selected_type': selected_type,
        'selected_age': selected_age,
        'status': status,
        'page_obj': page_obj,
    }
    if user.is_authenticated:
        if user.type == 1:
            return render(request, 'toy/admin_toy_list.html', context)
        else:
            return render(request, 'toy/toy_list.html', context)
    return redirect('login')

@login_required
def toy_add(request):
    user = request.user
    if user.type != 1:
        return HttpResponse("权限不足！！！")

    if request.method == 'POST':
        name = request.POST.get('name')
        type_ = request.POST.get('type')
        toy_type = Toy_type.objects.get(id=type_)
        toy_donor = request.POST.get('donor')
        applicable_age = request.POST.get('applicable_age')
        image_path = request.FILES.get('image_path')
        if image_path:
            image_path = f"image/{image_path}"
        try:
            toy = Toy.objects.create(
                name=name,
                type=toy_type.name,
                status=0,
                toy_donor=toy_donor,
                applicable_age=applicable_age,
                image_path=image_path
            )
            toy.save()
            return redirect('toy_list')
        except Exception as r:
            return HttpResponse(str(r))
    else:
        toy_types = Toy_type.objects.all()
        context = {
            'toy_types': toy_types
        }
        return render(request, 'toy/toy_add.html', context)

@require_POST
@login_required
def toy_delete(request):
    user = request.user
    if user.type == 1:
        id_ = request.POST.get('id')
        toy = Toy.objects.get(id=id_)
        if toy.status == 0:
            toy.delete()
            return redirect('toy_list')
        else:
            return HttpResponse("玩具正在被借用！！！")
    else:
        return HttpResponse("权限不足")

@login_required
def toy_edit(request, toy_id):
    user = request.user
    if user.type != 1:
        return HttpResponse("权限不足！！！")

    toy = get_object_or_404(Toy, id=toy_id)
    if request.method == 'POST':
        toy.name = request.POST.get('name')
        toy.type = request.POST.get('type')
        toy.toy_donor = request.POST.get('donor')
        toy.applicable_age = request.POST.get('applicable_age')
        image_path = request.POST.get('image_path')
        if image_path:
            toy.image_path = f"image/{image_path}"
        toy.save()
        return redirect('toy_list')
    else:
        context = {'toy': toy}
        return render(request, 'toy/toy_edit.html', context)

@login_required
def export_toys_to_excel(request):
    user = request.user
    if user.type == 1:  # 涉及到捐赠人，需管理员才有权限打印
        # 创建工作簿和工作表
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Toys'

        # 添加表头
        headers = ['玩具ID', '玩具名', '玩具类型', '状态', '捐赠人', '适用年龄', '图片路径']
        worksheet.append(headers)

        # 从数据库中获取数据并写入工作表
        toys = Toy.objects.all()
        for toy in toys:
            worksheet.append(
                [toy.id, toy.name, toy.type, toy.status, toy.toy_donor, toy.applicable_age, toy.image_path])

        # 创建HttpResponse对象并设置内容类型
        response = HttpResponse(content_type='application/vnd.malformations-office document.spreadsheet.sheet')
        response['Content-Disposition'] = 'attachment; filename=toys.xlsx'

        # 将工作簿保存到响应对象
        workbook.save(response)
        return response
    else:
        return HttpResponse("权限不足！！！")
