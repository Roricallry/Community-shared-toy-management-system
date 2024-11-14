from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.template.loader import get_template
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from future.backports.http.server import HTTPServer

from toy_type.models import Toy_type
from .models import Borrow
from user.models import *
from toy.models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime
import openpyxl
from django.db import connection

# Create your views here.
@login_required
@require_POST
def borrow_create(request):
    toy_id = request.POST.get('toy_id')
    username = request.POST.get('username')
    try:
        toy = Toy.objects.get(id=toy_id)
        if toy.status == "0":  # 确认玩具是未借出状态
            toy.status = "1"  # 更新玩具状态为已借出
            toy.save()
            record = Borrow(toy_id=toy_id, type=toy.type, name=toy.name, toy_borrow=username)
            record.save()
        else:
            return HttpResponse("已被借用")

    except Toy.DoesNotExist:
        return HttpResponse("玩具不存在")


    return redirect('toy_list')

@login_required
def borrow_query(request):
    user = request.user
    query = Q()
    toy_id = request.GET.get('toy_id')
    toy_name = request.GET.get('toy_name')
    toy_type = request.GET.get('toy_type')
    username = request.GET.get('username')
    advance_year = request.GET.get('advance_year')
    advance_month = request.GET.get('advance_month')
    advance_day = request.GET.get('advance_day')
    is_borrowed = request.GET.get('is_borrowed')
    is_returned = request.GET.get('is_returned')
    if toy_id:
        query &= Q(toy_id=toy_id)
    if toy_name:
        query &= Q(name__contains=toy_name)
    if toy_type:
        query &= Q(type=toy_type)
    if username and user.type == 1:
        query &= Q(toy_borrow__icontains=username)
    if advance_year:
        query &= Q(advance_time__year=advance_year)
    if advance_month:
        query &= Q(advance_time__month=advance_month)
    if advance_day:
        query &= Q(advance_time__day=advance_day)
    if is_borrowed:
        query &= Q(borrow_time__isnull=(is_borrowed.lower() != 'true'))
    if is_returned:
        query &= Q(return_time__isnull=(is_returned.lower() != 'true'))
    toy_types = Toy_type.objects.all()
    if user.type == 1:
        borrows = Borrow.objects.filter(query).order_by('-advance_time')
        return render(request, 'borrow/admin_query.html', {
            'borrows': borrows, 'toy_types': toy_types})
    else:
        borrows = Borrow.objects.filter(Q(toy_borrow=user) & query).order_by('-advance_time')
        return render(request, 'borrow/query.html', {'borrows': borrows, 'toy_types': toy_types})

@login_required
@require_POST
def borrow_cancel(request):
    user = request.user
    toy_id = request.POST.get('toy_id')
    advance_time = request.POST.get('advance_time')

    try:
        print(advance_time)
        if user.type == 0:  # 普通用户
            borrow = Borrow.objects.get(toy_id=toy_id, advance_time=advance_time, borrow_time__isnull=True, toy_borrow=user)
        else:  # 管理员
            borrow = Borrow.objects.get(toy_id=toy_id, advance_time=advance_time)
            print(borrow.advance_time)
        # 删除借阅记录
        borrow.delete()

        # 更新相关玩具状态
        toy = get_object_or_404(Toy, id=toy_id)  # 对象不存在则报404
        toy.status = "0"
        toy.save()

        return redirect('borrow_query')

    except (Borrow.DoesNotExist, ValueError) as e:
        return HttpResponse(f"Error: {e}")

@login_required
@require_POST
def borrow_update(request):
    user = request.user
    toy_id = request.POST.get('toy_id')
    advance_time = request.POST.get('advance_time')
    borrow_time = request.POST.get('borrow_time')
    print(borrow_time)
    if user.type == 1:
        if borrow_time == 'None':
            borrow = Borrow.objects.get(toy_id=toy_id, advance_time=advance_time)
            borrow.borrow_time = datetime.now()
            borrow.save()

        else:
            borrow = Borrow.objects.get(toy_id=toy_id, advance_time=advance_time)
            borrow.return_time = datetime.now()
            toy = Toy.objects.get(id=borrow.toy_id)
            toy.status = 0
            toy.save()
            borrow.save()

    return redirect("borrow_query")

@login_required
def export_borrow_to_excel(request):
    user = request.user
    if user.type == 1:
        # 创建工作簿和工作表
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Borrow'

        # 添加表头
        headers = ['玩具ID', '借用人姓名', '预借时间', '领取时间', '归还时间']
        worksheet.append(headers)

        # 从数据库中获取数据并写入工作表
        borrows = Borrow.objects.all()
        for borrow in borrows:
            worksheet.append(
                [borrow.toy_id, borrow.toy_borrow, borrow.advance_time, borrow.borrow_time, borrow.return_time])

        # 创建HttpResponse对象并设置内容类型
        response = HttpResponse(content_type='application/vnd.malformations-office document.spreadsheet.sheet')
        response['Content-Disposition'] = 'attachment; filename=borrows.xlsx'

        # 将工作簿保存到响应对象
        workbook.save(response)
        return response
    return HttpResponse("权限不足！！！")

def most_borrowed_toys(request):
    # 获取每种玩具类型的借用次数
    borrow_counts = Borrow.objects.values('type').annotate(borrow_count=Count('id')).order_by('-borrow_count')
    print(borrow_counts)

    # 获取每种玩具类型的个数
    toy_counts = Toy.objects.values('type').annotate(toy_count=Count('id')).order_by('-toy_count')
    print(toy_counts)

    # 创建一个字典来存储玩具类型的个数
    toy_type_count_dict = {item['type']: item['toy_count'] for item in toy_counts}
    print(toy_type_count_dict)

    # 将玩具数量信息合并到借用次数信息中
    for item in borrow_counts:
        item['toy_count'] = toy_type_count_dict.get(item['type'], 0)
    print(borrow_counts)


    # 获取玩具详细信息
    toy_borrow_counts = (Borrow.objects
                         .values('toy_id')
                         .annotate(borrow_count=Count('id'))
                         .order_by('-borrow_count'))
    toy_details = []
    for record in toy_borrow_counts:
        try:
            toy = Toy.objects.get(id=record['toy_id'])
            toy_details.append({
                'name': toy.name,
                'type': toy.type,
                'borrow_count': record['borrow_count']
            })
        except Toy.DoesNotExist:
            # 如果玩具不存在，可以选择忽略或处理这个异常
            continue

    return render(request, 'borrow/most_borrowed_toys.html', {
        'toy_details': toy_details,
        'borrow_counts': borrow_counts
    })

def test(request):
    # 获取每种玩具类型的借用次数
    borrow_counts = Borrow.objects.values('type').annotate(borrow_count=Count('id')).order_by('-borrow_count')

    # 获取每种玩具类型的个数，并按玩具数量降序排列
    toy_counts = Toy.objects.values('type').annotate(toy_count=Count('id')).order_by('-toy_count')
    print(toy_counts)

    # 创建一个字典来存储玩具类型的个数
    toy_type_count_dict = {item['type']: item['toy_count'] for item in toy_counts}
    print(toy_type_count_dict)

    # 将玩具数量信息合并到借用次数信息中
    borrow_counts_with_toy_counts = []
    for item in borrow_counts:
        borrow_type = item['type']
        item['toy_count'] = toy_type_count_dict.get(borrow_type, 0)
        borrow_counts_with_toy_counts.append(item)

    # 按玩具数量从高到低排序
    borrow_counts_with_toy_counts = sorted(borrow_counts_with_toy_counts, key=lambda x: x['toy_count'], reverse=True)

    print(borrow_counts_with_toy_counts)

    # 获取玩具详细信息
    toy_borrow_counts = (Borrow.objects
                         .values('toy_id')
                         .annotate(borrow_count=Count('id'))
                         .order_by('-borrow_count'))
    print(toy_borrow_counts)
    toy_details = []
    for record in toy_borrow_counts:
        try:
            toy = Toy.objects.get(id=record['toy_id'])
            toy_details.append({
                'name': toy.name,
                'type': toy.type,
                'borrow_count': record['borrow_count']
            })
        except Toy.DoesNotExist:
            # 如果玩具不存在，可以选择忽略或处理这个异常
            continue

    return render(request, 'borrow/test.html', {
        'toy_details': toy_details,
        'borrow_counts': borrow_counts_with_toy_counts
    })

def test2(request):
    user = request.user
    if user.type == 0:
        return HttpResponse("权限不足！")
