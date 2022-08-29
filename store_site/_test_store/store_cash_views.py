#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import pytz
import time
import random
import json
from datetime import datetime, timedelta 
from cStringIO import StringIO
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse as reverse_url

from fatcat.conf import settings as _settings
from spider.rpcclient import RPCClient
from site_utils import timestamp_to_datetime as ts_to_dt
#from pay_api import pay_api, pay_query_api
from cash_api import cash_api, cash_query_api


API_DOMAIN = "http://54.95.200.135:8080/"
API_URL_CASH_ADD = "%s%s"%(API_DOMAIN, "cash/add")
API_URL_CASH_QUERY = "%s%s"%(API_DOMAIN, "cash/order_query")
API_CALLBACK_URL = "http://3.115.201.240:9321/store/pay_callback"



### DB_CLI ###
def new_cli():
  return  RPCClient(_settings.TEST_STORE_DB_ADDR)

def now_tw_time():
  ts = time.time()
  twdt = ts_to_dt(ts)
  return twdt.strftime("%Y/%m/%d %H:%M:%S"),



#####################################################################
### CREATE_SYS_ORDER  ###
### CREATE_API_ORDER  ###
def cash_add_view(request):
  print ("cash_add_test")
  try:
    sid = int(request.GET['q'])
  except:
    sid = None
  if sid is None:
    print("*** -Cash add error.   no sid.")
    redirect_to = reverse_url("store_index")
    return HttpResponseRedirect(redirect_to)

  # code something ... #


  # code something ...end. #
  
  redirect_to = reverse_url("detail") +"?q=%s"%sid
  return HttpResponseRedirect(redirect_to)



### QUERY_API_ORDER  ###
def cash_query_view(request):
  print ("cash_query_test")
  try:
    sid = int(request.GET['sid'])
    oid = int(request.GET['oid'])
  except:
    sid = None
    oid = None
  if oid is None or sid is None:
    print("*** -Query order error.   no oid or no sid.")
    redirect_to = reverse_url("store_index")
    return HttpResponseRedirect(redirect_to)

  # code something ... #
  order_info = None
  api_info = None




  # code something ...end. #

  
  return TemplateResponse(request, 'store/query.html', {
    'order_info':order_info,
    'api_info':api_info,
  })


  
### RE_SPEND_API_ORDER  ###
def cash_readd_view(request):
  print ("cash_readd_order")
  try:
    sid = int(request.GET['sid'])
    oid = int(request.GET['oid'])
  except:
    sid = None
    oid = None

  # code something ... #



  # code something ...end. #

  redirect_to = reverse_url("detail") +"?q=%s"%sid
  return HttpResponseRedirect(redirect_to)



### REPORT_CALC_ORDER  ###
def cash_report_view(request):
  print ("cash_report_order")
  try:
    sid = int(request.GET['q'])
  except:
    sid = None

  if sid is None:
    print("*** -Report order error. no sid.")
    redirect_to = reverse_url("detail") +"?q=%s"%sid
    return HttpResponseRedirect(redirect_to)

  # code something ... #
  api_cash_list = []
  cash_success_coin = 0 
  cash_success_len = 0 
  cash_fail_coin = 0
  cash_fail_len = 0


  # code something ...end. #

  return TemplateResponse(request, 'store/cash_report.html', {
    's_info':s_info,
    'cash_list':api_cash_list,

    'success_coin':cash_success_coin,
    'success_len':cash_success_len,
    'fail_coin':cash_fail_coin,
    'fail_len':cash_fail_len,
  })



