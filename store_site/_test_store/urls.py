from django.conf.urls import url, include
from django.contrib import admin

from test_store import views, test_views, debug_views, log_views
from test_store import stats_views
from test_store import query_views

from test_store import info_views
from test_store import store_views, store_cash_views
from test_store import db_views

db_urls = [
  url(r'^tables$', db_views.table_list_view),
  url(r'^table_page$', db_views.table_page_view, name='db_table_query'),

]

test_urls = [
  url(r'^calc_task_confirm$', test_views.calc_task_confirm),
]

debug_urls = [
  url(r'^calc_robtask$', debug_views.calc_robtask_view),
]

log_urls = [
  url(r'^$', log_views.index_view, name='log_index'),
  url(r'^hour_seq$', log_views.hour_seq_index_view, name='log_hour_seq_index'),
  url(r'^seq_logs$', log_views.seq_items_view, name='log_seq_items'),
  url(r'^find_out_sn$', log_views.find_out_sn_view, name='log_find_out_sn'),
  url(r'^find$', log_views.find_view, name='log_find'),
  url(r'^scan$', log_views.scan_view, name='log_scan'),
]

stats_urls = [
  url(r'^$', stats_views.index_view, name='stats_index'),
]


infos_urls = [
  url(r'^$', info_views.index_view, name='info_index'),
  url(r'^test$', info_views.add_test_data, name='test'),
  url(r'^post$', info_views.post_vps_info, name='post'),
]

store_urls = [
  url(r'^$', store_views.index_view, name='store_index'),
  url(r'^create$', store_views.create_view, name='create'),
  url(r'^edit$', store_views.edit_view, name='edit'),
  url(r'^detail$', store_views.detail_view, name='detail'),

  #pay_order
  url(r'^pay_add$', store_views.pay_add_view, name='pay_add'),
  url(r'^pay_query$', store_views.pay_query_view, name='pay_query'),
  url(r'^pay_readd$', store_views.pay_readd_view, name='pay_readd'),
  url(r'^pay_report$', store_views.pay_report_view, name='pay_report'),

  #cash_order
  url(r'^cash_add$', store_cash_views.cash_add_view, name='cash_add'),
  url(r'^cash_query$', store_cash_views.cash_query_view, name='cash_query'),
  url(r'^cash_readd$', store_cash_views.cash_readd_view, name='cash_readd'),
  url(r'^cash_report$', store_cash_views.cash_report_view, name='cash_report'),

  #url(r'^cash_readd$', store_views.pay_readd_view, name='pay_readd'),
  #url(r'^cash_report$', store_views.pay_report_view, name='pay_report'),
  url(r'^pay_callback$', store_views.pay_callback_view, name='pay_callback'),
]

query_urls = [
  url(r'^ix$', query_views.query_ix_view, name='query_ix'),
]

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^admin_user$', views.admin_user_list, name='admin_user_list'),
  url(r'^ant_user$', views.ant_user_list, name='ant_user_list'),
  url(r'^orders$', views.order_list, name='order_list'),
  url(r'^tasks$', views.task_list, name='task_list'),
  url(r'^lowerhairs$', views.lowerhairs_list),
  url(r'^account_set$', views.account_set_list),
  url(r'^account_item$', views.account_item_list),
  #url(r'^req_log$', views.req_log_view),
  #url(r'^admin/', admin.site.urls),

  url(r'^db/', include(db_urls)),
  url(r'^test/', include(test_urls)),
  url(r'^debug/', include(debug_urls)),
  url(r'^log/', include(log_urls)),
  url(r'^stats/', include(stats_urls)),
  url(r'^info/', include(infos_urls)),
  url(r'^store/', include(store_urls)),
  url(r'^query/', include(query_urls)),
]
