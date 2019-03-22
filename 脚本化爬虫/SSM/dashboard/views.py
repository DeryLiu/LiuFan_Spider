# encoding=utf-8
from celery import chain
from celery import chord
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.conf import settings
from django.db.models import F
from django.template import RequestContext
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from dashboard.models import Website, Category, Product, Task
from dashboard.forms import SiteForm, TaskForm
from dashboard.tasks import initial_categories, initial_category_children, group_categories, finish_init_category, crawl_product_urls, finish_get_category_products, group_tasks, \
    crawl_product_info
import logging
logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        usr = request.POST['username']
        psw = request.POST['password']
        user = authenticate(username=usr, password=psw)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                pass
        else:
            pass
        return redirect('dashboard')
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    sites = Website.objects.all()
    ctx = {'sites': []}
    for site in sites:
        data = {
            'name': site.name,
            'url': site.url,
            'logo': site.logo,
            'level_one_count': site.category_set.filter(parent_id=None).count(),
            'level_leaf_count': site.category_set.filter(is_leaf=True).count(),
            'product_count': site.get_products().count(),
            'today_add': site.get_products(1, 'new').count(),
            'today_update': site.get_products(1, 'update').count(),
            'today_off': site.get_products(1, 'off').count()
        }
        ctx['sites'].append(data)
    return render_to_response('dashboard/dashboard.html', context=ctx, context_instance=RequestContext(request))


@login_required
def site_view(request):
    if request.method == 'POST':
        form = SiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            request.session['errors'] = form.errors
        return redirect('site')
    errors = request.session.get('errors')
    request.session['errors'] = None
    ctx = {'sites': Website.objects.all(), 'errors': errors}
    return render_to_response('dashboard/site.html', context=ctx, context_instance=RequestContext(request))


@login_required
def site_remove_ajax(request):
    data = {}
    if request.method == 'POST' and request.is_ajax():
        site_names = request.POST.getlist('site_names[]')
        Website.objects.filter(name__in=site_names).delete()
        data.update({'state': 'success'})
    else:
        data.update({'state': 'failed', 'msg': 'Method not allowed.'})
    return JsonResponse(data)


@login_required
def site_update_view(request):
    if request.method == 'POST':
        site_id = request.POST.get('id')
        site = get_object_or_404(Website, pk=site_id)
        form = SiteForm(request.POST, request.FILES, instance=site)
        if form.is_valid():
            form.save()
        else:
            request.session['errors'] = form.errors
        return redirect('site')
    else:
        form = SiteForm()
    request.session.update({'errors': form.errors})
    return redirect('site')


@login_required
def site_product_view(request, site_id):
    site = get_object_or_404(Website, pk=site_id)
    page_count = settings.PRODUCT_PER_PAGE
    products = Product.objects.filter(category__in=site.category_set.all())
    ctx = {
        'site': site,
        'products': products.order_by('id')[:page_count],
        'total': (products.count() - 1) / page_count + 1
    }
    return render_to_response('dashboard/site_product.html', context=ctx, context_instance=RequestContext(request))


@login_required
def site_product_remove_view(request, product_id):
    Product.objects.filter(pk=product_id).delete()
    return redirect('site')


@login_required
def site_category_json(request, site_id):
    data = {}
    if request.method == 'GET' and request.is_ajax():
        categories = Category.objects.filter(site=site_id).select_related('parent')
        if categories is not None:
            datas = [{'id': cat.id, 'pId': cat.parent and cat.parent.id or None, 'name': cat.name} for cat in categories]
            data.update({'state': 'success', 'datas': datas})
        else:
            data.update({'state': 'failed', 'msg': 'Data not found.'})
    else:
        data.update({'state': 'failed', 'msg': 'Method not allowed.'})
    return JsonResponse(data)


@login_required
def site_category_product_json(request):
    data = {}
    if request.method == 'POST' and request.is_ajax():
        ids = request.POST.getlist('ids[]')
        page = request.POST.get('page', 1)
        keyword = request.POST.get('keyword')
        try:
            page = int(page)
        except ValueError as e:
            page = 1
        page_count = settings.PRODUCT_PER_PAGE
        offset = page_count * (page - 1)
        limit = offset + page_count
        products = Product.objects.filter(category_id__in=ids)
        if keyword is not None:
            products = products.filter(name__icontains=keyword)
        total = (products.count() - 1) / page_count + 1
        products = products.order_by('id')[offset:limit]
        if products:
            datas = [{'id': product.id,
                         'name': product.name,
                         'categoryName': product.category.name,
                         'server': product.server,
                         'status': product.get_status()
                         } for product in products]
            data.update({'state': 'success', 'datas': datas, 'page': page, 'total': total, 'keyword': keyword})
        else:
            data.update({'state': 'failed', 'msg': 'Products not found.'})
    else:
        data.update({'state': 'failed', 'msg': 'Method not allowed.'})
    return JsonResponse(data)


@login_required
def task_view(request):
    if request.method == 'POST':
        try:
            task_id = int(request.POST.get('taskId', ''))
            task = get_object_or_404(Task, pk=task_id)
        except ValueError as e:
            logger.error(e.message)
            task = None
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        else:
            request.session['errors'] = form.errors
        return redirect('task')
    errors = request.session.get('errors')
    request.session['errors'] = None
    sites = Website.objects.all()
    tasks = Task.objects.all()
    ctx = {
        'sites': sites,
        'tasks': tasks,
        'errors': errors
    }
    return render_to_response('dashboard/task.html', context=ctx, context_instance=RequestContext(request))


@login_required
def task_remove_ajax(request):
    data = {}
    if request.method == 'POST' and request.is_ajax():
        task_names = request.POST.getlist('task_names[]')
        tasks = Task.objects.filter(name__in=task_names).all()
        for task in tasks:
            Category.objects.filter(pk__in=task.category_keys.split(',')).update(status='done')
        tasks.delete()
        # Task.objects.filter(name__in=task_names).delete()
        data.update({'state': 'success', 'redirect': reverse('task')})
    else:
        data.update({'state': 'failed', 'msg': 'Method not allowed.'})
    return JsonResponse(data)


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    ctx = {'task': task}
    return render_to_response('dashboard/task_progress.html', context=ctx, context_instance=RequestContext(request))


@login_required
def task_category_progress_json(request, task_id):
    data = {}
    if request.method == 'GET' and request.is_ajax():
        task = Task.objects.get(id=task_id)
        cats = Category.objects.filter(pk__in=task.category_keys.split(',')).select_related('parent').all()
        # cats = Category.objects.filter(pk__in=task.category_keys.split(',')).all()
        data = {
            'state': 'success',
            'datas': [
                {'category_id': cat.pk,
                 'category_path': cat.get_name_path(),
                 'success': cat.product_success,
                 'failed': cat.product_failed,
                 'total': cat.product_total,
                 'page_progress': cat.get_progress()
                 } for cat in cats]
        }
    else:
        data.update({'state': 'failed', 'msg': 'Method not allowed.'})
    return JsonResponse(data)


@login_required
def statistics(request, day='today'):
    if day not in ['today', 'this_week', 'this_month']:
        return redirect(statistics)
    if day == 'today':
        d = 1
    elif day == 'this_week':
        d = 7
    else:
        d = 30
    data = []
    for site in Website.objects.all():
        data.append({
            'name': site.name,
            'category_count': site.category_set.count(),
            'product_count': site.get_products().count(),
            'new_count': site.get_products(d, 'new').count(),
            'update_count': site.get_products(d, 'update').count(),
            'off_count': site.get_products(d, 'off').count()
        })
    ctx = {'sites': data, 'day': day}
    return render_to_response('dashboard/statistics.html', context=ctx, context_instance=RequestContext(request))


@login_required
def init_site_category(request, site_id):
    data = {}
    if request.method == 'GET' and request.is_ajax():
        try:
            site = Website.objects.get(pk=site_id)
        except ObjectDoesNotExist:
            site = None
        data = {}
        if site is None:
            data.update({
                'state': 'failed',
                'msg': u'站点不存在，请刷新当前页面'
            })
        else:
            if not site.spider_class:
                data.update({
                    'state': 'failed',
                    'msg': u'初始化站点失败，请设置爬虫'
                })
            elif site.status == 'pending':
                data.update({
                    'state': 'failed',
                    'msg': u'正在初始化站点，请等待'
                })
            elif site.status == 'failed':
                data.update({
                    'state': 'failed',
                    'msg': u'初始化站点失败，请重试'
                })
            else:
                site.status = 'pending'
                site.save()
                task = chord([chain(initial_categories.s(site.pk), group_categories.s(initial_category_children.s(), site_id))])(finish_init_category.s(site.pk))
                task.delay()
                data.update({
                    'state': 'success',
                })
    else:
        data.update({'state': 'failed', 'msg': 'Method not allowed.'})
    return JsonResponse(data)


@login_required
def start_task(request, task_id):
    data = {}
    if request.method == 'GET' and request.is_ajax():
        task = Task.objects.get(pk=task_id)
        if task.status == 'done':
            categories = Category.objects.filter(pk__in=task.category_keys.split(','), status='done')
            print(task.category_keys)
            categories.update(product_success=0, product_failed=0)
            if task.task_type == 'crawl':
                urls = [cat.url for cat in categories]
                chord(chain(crawl_product_urls.s(u), group_tasks.s(crawl_product_info.s(u, '%s.txt' % task.name))) for u in urls)(finish_get_category_products.s(task.id))
                categories.update(status='pending')
            else:
                products = Product.objects.filter(category_id__in=categories)
                chord(crawl_product_info.s(product.url, product.category.url, '%s.txt' % task.name) for product in products)(finish_get_category_products.s(task.id))
            task.status = 'pending'
            task.save()
            data = {'state': 'success'}
        elif task.status == 'pending':
            data = {'state': 'failed', 'msg': u'任务执行中，请稍后再试'}
        else:
            data = {'state': 'failed', 'msg': u'任务执行错误'}
    else:
        data.update({'state': 'failed', 'msg': 'Method not allowed.'})
    return JsonResponse(data)


@login_required
def update_category(request):
    data = {}
    if request.method == 'POST' and request.is_ajax():
        if 'category_ids[]' not in request.POST:
            data.update({'state': 'failed', 'msg': '请选择需要更新的品类'})
        else:
            ids = request.POST.getlist('category_ids[]')
            categories = Category.objects.filter(pk__in=ids, status='done')
            print(categories)
            products = Product.objects.filter(category_id__in=categories)
            chord(crawl_product_info.s(product.url, product.category.url, 'category_update.txt') for product in products)(finish_get_category_products.s(1))
            data.update({'state': 'success'})
    else:
        data.update({'state': 'failed', 'msg': 'Method not allowed.'})
    return JsonResponse(data)
