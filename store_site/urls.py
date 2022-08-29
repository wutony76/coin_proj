from django.conf.urls import url, include
from django.contrib import admin

from store_site import views
from store_site import ant_views, cash_views, pay_views
from store_site import ants_store_views
from store_site import api_views




ant_urls = [
  url(r'^list$', ant_views.list_view, name='ant_list'),
  url(r'^add$', ant_views.add_view, name='ant_create'),
  url(r'^edit$', ant_views.edit_view, name='ant_edit'),
  url(r'^save$', ant_views.save_view, name='ant_save'),
]

cash_urls = [
  url(r'^list$', cash_views.list_view, name='cash_list'),
  url(r'^add$', cash_views.add_view, name='cash_create'),
  url(r'^edit$', cash_views.edit_view, name='cash_edit'),
  url(r'^cancel$', cash_views.cancel_view, name='cash_cancel'),
  url(r'^success$', cash_views.success_view, name='cash_success'),

  url(r'^save$', cash_views.save_view, name='cash_save'),
  url(r'^appoint$', cash_views.appoint_view, name='cash_appoint'),
]

pay_urls = [
  url(r'^list$', pay_views.list_view, name='pay_list'),
  url(r'^add$', pay_views.add_view, name='pay_create'),
  url(r'^edit$', pay_views.edit_view, name='pay_edit'),
  url(r'^cancel$', pay_views.cancel_view, name='pay_cancel'),
  url(r'^success$', pay_views.success_view, name='pay_success'),

  url(r'^save$', pay_views.save_view, name='pay_save'),
  url(r'^appoint$', pay_views.appoint_view, name='pay_appoint'),
  url(r'^check_pay$', pay_views.check_view, name='pay_check'),

  url(r'^bank$', pay_views.bank_view, name='pay_bank'),
]

api_urls = [
  url(r'^api$', api_views.index, name='api_index'),
  url(r'^api_pay$', api_views.paying_pay, name='api_pay'),
  url(r'^api_cash$', api_views.cash_add, name='api_cash'),
]

antstore_urls = [
  url(r'^cash_list$', ants_store_views.cash_list, name='ant_cash_list'),
  url(r'^pay_list$', ants_store_views.pay_list, name='ant_pay_list'),
  url(r'^paying_cash$', ants_store_views.paying_cash, name='paying_cash'),
  url(r'^paying_pay$', ants_store_views.paying_pay, name='paying_pay'),
]



urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^login_ant$', views.login_ant, name='login_ant'),

  url(r'^ant/', include(ant_urls)),
  url(r'^cash/', include(cash_urls)),
  url(r'^pay/', include(pay_urls)),

  url(r'^api/', include(api_urls)),
  url(r'^antstore/', include(antstore_urls)),
]
