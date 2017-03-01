# encoding=utf-8
from django.conf import settings
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard_view, name='dashboard'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^site/$', views.site_view, name='site'),
    url(r'^site/remove/$', views.site_remove_ajax, name='site_remove'),
    url(r'^site/update/$', views.site_update_view, name='site_update'),
    url(r'^site/(?P<site_id>\d+)/$', views.site_product_view, name='site_product'),
    url(r'^site/remove/product/(?P<product_id>\d+)/$', views.site_product_remove_view, name='site_product_remove'),
    url(r'^site/category/json/(?P<site_id>\d+)/$', views.site_category_json, name='site_category_json'),
    url(r'^site/category/product/json/$', views.site_category_product_json, name='site_category_product_json'),
    url(r'^task/$', views.task_view, name='task'),
    url(r'^task/remove/$', views.task_remove_ajax, name='task_remove'),
    url(r'^task/progress/(?P<task_id>\d+)/$', views.task_detail, name='task_progress'),
    url(r'^task/progress/json/(?P<task_id>\d+)/$', views.task_category_progress_json, name='task_progress_json'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^statistics/(?P<day>\w+)/$', views.statistics, name='statistics_with_day'),
    url(r'^init/site/category/(?P<site_id>\d+)/$', views.init_site_category, name='init_site_category'),
    url(r'^start/task/(?P<task_id>\d+)/$', views.start_task, name='start_task'),
    url(r'^category/update/$', views.update_category, name='update_category')
]
