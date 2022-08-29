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


  _id = time.time() *100
  _id = int(_id)
  #sn = "test-sn%s" % _id
  money = random.randint(200,10000)

  save_data = {
    "tid": _id,
    "tmoney": money,
    "create_time": now_tw_time(),

    #0 -success
    #1 -fail
    "api_success": 1, 
    "api_id": None, 
    #"api_money": None, 
    "api_status": None, 
    "api_remark": "CASH", 
  }
  print ("save_data = ", save_data)
  cli = new_cli()

  #get store info 
  store_info = cli.call("LIST_STORE", sid )
  store_id = store_info.get("pid")
  store_key = store_info.get("key")
  callback_url = store_info.get("cash_callback_url", "http://127.0.0.1")
  callback_url += "?q=%s" % sid 

  #req api
  api_post = cash_api(API_URL_CASH_ADD, store_id, store_key, money, _id, callback_url)
  #api_post = pay_api(API_URL_CASH_ADD, store_id, store_key, money, _id, callback_url)
  print("api_post = ", api_post)
  if api_post["code"] == 0:

    #save post remark.
    save_data["api_remark"] = api_post["data"]
    json_post_data = json.loads(api_post["data"])

    if json_post_data["code"] == 1:
      print("json_post_data = ", json_post_data)
      api_data = json_post_data["data"]
      #sn = api_data["sn"]
      #amount = api_data["amount"]

      #save api post data.
      #save_data["api_id"] = sn
      #save_data["api_money"] = amount
      save_data["api_success"] = 0

  #save order info.
  rtn = cli.call("UPDATE_CASH_ORDER", sid, _id, save_data)
  print("rtn = ", rtn)
  
  redirect_to = reverse_url("detail") +"?q=%s"%sid
  #print ("redirect_to = ", redirect_to)
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

  cli = new_cli()
  store_info = cli.call("LIST_STORE", sid )
  store_id = store_info.get("pid")
  store_key = store_info.get("key")

  order_info = cli.call("LIST_CASH", sid, oid)[0]
  print ("order_info = " , order_info)
  #order_money = '%.2f' % order_info.get("tmoney")
  #print ("order_money = " , order_money)

  api_query_post = cash_query_api(API_URL_CASH_QUERY, store_id, store_key, oid)
  print("api_query_post = ", api_query_post)

  api_info = None
  if api_query_post.has_key("data"):
    api_info = api_query_post["data"]
    json_api_info = json.loads(api_info)
    fmt_api_info = json_api_info["data"]

    #status 0 
    #status 1 
    #status 2 success 
    #status 3 
    #status 4 
    #status 5 
    if json_api_info["code"] == 1 and json_api_info["msg"] == "success":
      update_data = {
        "tid": oid,
        "api_status": fmt_api_info["status"], 
      }
      #o_status = fmt_api_info["status"]
      #if o_status != 2 and o_status != 3:
      if order_info.get("api_status") != 2 and order_info.get("api_status") != 3:
        rtn = cli.call("UPDATE_CASH_ORDER", sid, oid, update_data)
        print("rtn = ", rtn)

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

  if oid is None or sid is None:
    print("*** -Readd order error.   no oid or no sid.")
    redirect_to = reverse_url("store_index")
    return HttpResponseRedirect(redirect_to)

  cli = new_cli()
  store_info = cli.call("LIST_STORE", sid )
  store_id = store_info.get("pid")
  store_key = store_info.get("key")
  callback_url = store_info.get("cash_callback_url", "http://127.0.0.1")
  callback_url += "?q=%s" % sid 

  order_info = cli.call("LIST_CASH", sid, oid)[0]
  print("order_info = ", order_info)
  order_tid = order_info.get("tid")
  order_money = order_info.get("tmoney")

  #0 -success
  #1 -fail
  #3 -default
  if order_info.get("api_success", 3) != 1:
    print("*** -Readd order error.")

    redirect_to = reverse_url("detail") +"?q=%s"%sid
    return HttpResponseRedirect(redirect_to)
  
  #req api
  api_post = cash_api(API_URL_CASH_ADD, store_id, store_key, order_money, order_tid, callback_url)
  print("re_cash_api_post = ", api_post)

  if api_post["code"] == 0:
    update_data = {
      "tid": oid,
    }  
      
    #save post remark.
    update_data["api_remark"] = api_post["data"]
    json_post_data = json.loads(api_post["data"])

    if json_post_data["code"] == 1:
      print("json_post_data = ", json_post_data)
      api_data = json_post_data["data"]
      #sn = api_data["sn"]
      #amount = api_data["amount"]

      ##save api post data.
      #update_data["api_id"] = sn
      #update_data["api_money"] = amount
      update_data["api_success"] = 0
      update_data["api_send_count"] = order_info.get("api_send_count", 0)+1

    #save order info.
    rtn = cli.call("UPDATE_CASH_ORDER", sid, oid, update_data)
    print("update_rtn = ", rtn)

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

  cli = new_cli()
  s_info = cli.call("LIST_STORE", sid )
  #s_pay_list = cli.call("LIST_PAY", sid )
  s_cash_list = cli.call("LIST_CASH", sid )
  s_cash_list.reverse()
  
  api_cash_list = []

  cash_success_coin = 0 
  cash_success_len = 0 
  cash_fail_coin = 0
  cash_fail_len = 0

  for order in s_cash_list:
    print("order -", order)
    if order.get("api_success",3) == 0:
      api_cash_list.append(order)

      #if order.get("api_status") == "success":
      if order.get("api_status") == 2:
        cash_success_coin += order.get("tmoney")
        cash_success_len += 1
      else:
        cash_fail_coin += order.get("tmoney")
        cash_fail_len += 1

  return TemplateResponse(request, 'store/cash_report.html', {
    's_info':s_info,
    'cash_list':api_cash_list,

    'success_coin':cash_success_coin,
    'success_len':cash_success_len,
    'fail_coin':cash_fail_coin,
    'fail_len':cash_fail_len,
  })



