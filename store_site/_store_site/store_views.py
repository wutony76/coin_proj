#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import pytz
import time
import random
import json
from datetime import datetime, timedelta 
#from datetime.datetime import astimezone
from cStringIO import StringIO
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse as reverse_url
from django.views.decorators.csrf import csrf_exempt
#from dipay.models import OrderInfo, LowerhairInfo
#from fdpays import time_utils

from fatcat.conf import settings as _settings
from spider.rpcclient import RPCClient

from site_utils import timestamp_to_datetime as ts_to_dt
from pay_api import pay_api, pay_query_api




API_DOMAIN = "http://54.95.200.135:8080/"
API_URL_PAY_ADD = "%s%s"%(API_DOMAIN, "pay")
API_URL_PAY_QUERY = "%s%s"%(API_DOMAIN, "order_query")

API_CALLBACK_URL = "http://3.115.201.240:9321/store/pay_callback"


### DB_CLI ###
def new_cli():
  #return  RPCClient(_settings.PAY_VPS_INFO_ADDR)
  return  RPCClient(_settings.TEST_STORE_DB_ADDR)

def now_tw_time():
  ts = time.time()
  twdt = ts_to_dt(ts)
  return twdt.strftime("%Y/%m/%d %H:%M:%S"),



#####################################################################
### ALL_STORE_LIST ###
def index_view(request):
  print ("STORE-INDEX")
  cli = new_cli()

  q = {'limit': 1024, 'offset': 0}
  rtn = cli.call("SCAN_STORE", None, q)
  print( "rtn=", rtn)

  for k, v in rtn.items():
    pass

  return TemplateResponse(request, 'store/index.html', {
    'list': rtn,
  })



### CREATE_NEW_STORE ###
def create_view(request):
  print ("CREATE-INDEX")
  if request.method == "POST":
    #ts = time.time()
    #twdt = ts_to_dt(ts)

    save_data={
      "name": request.POST['name'],
      "pid": request.POST['pid'],
      "key": request.POST['key'],
      "remark": request.POST['remark'],
      "type": request.POST['type'],
      "callback_url": request.POST['callback_url'],
      "cash_callback_url": request.POST['cash_callback_url'],
      #"update_time":twdt.strftime("%Y/%m/%d %H:%M:%S"),
      "update_time":now_tw_time(),
    }

    cli = new_cli()
    out = cli.call("UPDATE_STORE_INFO", save_data)
    print( "out = ", out )

    redirect_to = reverse_url("store_index")
    return HttpResponseRedirect(redirect_to)

  detail = None
  return TemplateResponse(request, 'store/create.html', {
    'detail': detail,
  })



### EDIT_STORE_INFO ###
### EDIT_API_INFO ###
def edit_view(request):
  print ("EDIT-INDEX")
  redirect_to = reverse_url("store_index")

  try:
    sid = int(request.GET['q'])
  except:
    sid = None
  if sid is None:
    return HttpResponseRedirect(redirect_to)
    
  cli = new_cli()
  detail = cli.call("GET_STORE", sid )
  #print ("detail = ", detail)
  if request.method == "POST":
    #print ("POST = ", request.POST)
    save_data={
      "sid": int(request.POST['sid']),
      "name": request.POST['name'],
      "pid": request.POST['pid'],
      "key": request.POST['key'],
      "remark": request.POST['remark'],
      "type": request.POST['type'],
      "callback_url": request.POST['callback_url'],
      "cash_callback_url": request.POST['cash_callback_url'],
    }
    out = cli.call("UPDATE_STORE_INFO", save_data)
    print( "out = ", out )
    return HttpResponseRedirect(redirect_to)

  return TemplateResponse(request, 'store/create.html', {
    'detail': detail,
  })



#####################################################################
### SYS_ORDER_LIST  ###
def detail_view(request):
  print ("DETAIL-INDEX")
  redirect_to = reverse_url("store_index")

  try:
    sid = int(request.GET['q'])
  except:
    sid = None
  if sid is None:
    print("*** -Order list error.   no sid.")
    return HttpResponseRedirect(redirect_to)

  #-- detail --
  cli = new_cli()
  s_info = cli.call("LIST_STORE", sid )
  s_pay_list = cli.call("LIST_PAY", sid )
  s_pay_list.reverse()
  
  return TemplateResponse(request, 'store/detail.html', {
    's_info':s_info,
    'pay_list':s_pay_list,
  })



### CREATE_SYS_ORDER  ###
### CREATE_API_ORDER  ###
def pay_add_view(request):
  print ("pay_add_test")

  try:
    sid = int(request.GET['q'])
  except:
    sid = None
  if sid is None:
    print("*** -Pay add error.   no sid.")
    redirect_to = reverse_url("store_index")
    return HttpResponseRedirect(redirect_to)


  _id = time.time() *100
  _id = int(_id)
  #sn = "test-sn%s" % _id
  money = random.randint(200,10000)

  save_data={
    "tid": _id,
    "tmoney": money,
    "create_time": now_tw_time(),

    #0 -success
    #1 -fail
    "api_success": 1, 

    "api_id": None, 
    "api_money": None, 
    "api_status": None, 
    "api_remark": None, 
  }
  print ("save_data = ", save_data)
  cli = new_cli()

  #get store info 
  store_info = cli.call("LIST_STORE", sid )
  store_id = store_info.get("pid")
  store_key = store_info.get("key")
  callback_url = store_info.get("callback_url", "http://127.0.0.1")
  callback_url += "?q=%s" % sid 

  #req api
  api_post = pay_api(API_URL_PAY_ADD, store_id, store_key, money, _id, callback_url)
  print("api_post = ", api_post)
  if api_post["code"] == 0:

    #save post remark.
    save_data["api_remark"] = api_post["data"]
    json_post_data = json.loads(api_post["data"])

    if json_post_data["code"] == 1:
      print("json_post_data = ", json_post_data)
      api_data = json_post_data["data"]
      sn = api_data["sn"]
      amount = api_data["amount"]

      #save api post data.
      save_data["api_id"] = sn
      save_data["api_money"] = amount
      save_data["api_success"] = 0

  #save order info.
  rtn = cli.call("UPDATE_PAY_ORDER", sid, _id, save_data)
  print("rtn = ", rtn)
  
  redirect_to = reverse_url("detail") +"?q=%s"%sid
  #print ("redirect_to = ", redirect_to)
  return HttpResponseRedirect(redirect_to)



### QUERY_API_ORDER  ###
def pay_query_view(request):
  print ("pay_query_test")
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

  order_info = cli.call("LIST_PAY", sid, oid)[0]
  #print ("order_info = " , order_info)
  order_money = '%.2f' % order_info.get("tmoney")
  #print ("order_money = " , order_money)

  api_query_post = pay_query_api(API_URL_PAY_QUERY, store_id, store_key, order_money, oid)
  print("api_query_post = ", api_query_post)

  api_info = None
  if api_query_post.has_key("data"):
    api_info = api_query_post["data"]
    json_api_info = json.loads(api_info)
    fmt_api_info = json_api_info["data"]
    #print("json_api_info = ", json_api_info)
    #print("json_code = ", json_api_info["code"])
    #print("json_status = ", fmt_api_info["status"])
    if json_api_info["code"] == 1 and fmt_api_info["status"] == "success":
      update_data = {
        "tid": oid,
        "api_status": fmt_api_info["status"], 
      }
      if order_info.get("api_status") != 'success':
        #update order info status.
        rtn = cli.call("UPDATE_PAY_ORDER", sid, oid, update_data)
        print("rtn = ", rtn)

  return TemplateResponse(request, 'store/query.html', {
    'order_info':order_info,
    'api_info':api_info,
  })



### RE_SPEND_API_ORDER  ###
def pay_readd_view(request):
  print ("pay_readd_order")
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
  #get store info 
  store_info = cli.call("LIST_STORE", sid )
  store_id = store_info.get("pid")
  store_key = store_info.get("key")
  callback_url = store_info.get("callback_url", "http://127.0.0.1")
  callback_url += "?q=%s" % sid 

  order_info = cli.call("LIST_PAY", sid, oid)[0]
  order_money = order_info.get("tmoney")

  #0 -success
  #1 -fail
  #3 -default
  if order_info.get("api_success", 3) != 1:
    print("*** -Readd order error.")
    #redirect_to = reverse_url("store_index")
    #return HttpResponseRedirect(redirect_to)

    redirect_to = reverse_url("detail") +"?q=%s"%sid
    return HttpResponseRedirect(redirect_to)

  #req api
  api_post = pay_api(API_URL_PAY_ADD, store_id, store_key, order_money, oid, callback_url)
  print("api_post = ", api_post)

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
      sn = api_data["sn"]
      amount = api_data["amount"]

      #save api post data.
      update_data["api_id"] = sn
      update_data["api_money"] = amount
      update_data["api_success"] = 0
      update_data["api_send_count"] = order_info.get("api_send_count", 0)+1

    #save order info.
    rtn = cli.call("UPDATE_PAY_ORDER", sid, oid, update_data)
    print("rtn = ", rtn)

  redirect_to = reverse_url("detail") +"?q=%s"%sid
  return HttpResponseRedirect(redirect_to)



### REPORT_CALC_ORDER  ###
def pay_report_view(request):
  print ("pay_report_order")
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
  s_pay_list = cli.call("LIST_PAY", sid )
  s_pay_list.reverse()
  
  api_pay_list = []

  pay_success_coin = 0 
  pay_success_len = 0 
  pay_fail_coin = 0
  pay_fail_len = 0

  for order in s_pay_list:
    print("order -", order)
    if order.get("api_success",3) == 0:
      api_pay_list.append(order)

      if order.get("api_status") == "success":
        pay_success_coin += order.get("api_money")
        pay_success_len += 1
      else:
        pay_fail_coin += order.get("api_money")
        pay_fail_len += 1
      
  return TemplateResponse(request, 'store/pay_report.html', {
    's_info':s_info,
    'pay_list':api_pay_list,

    'success_coin':pay_success_coin,
    'success_len':pay_success_len,
    'fail_coin':pay_fail_coin,
    'fail_len':pay_fail_len,
  })


### API_CALLBACK  ###
@csrf_exempt
def pay_callback_view(request):
  print ("pay_callback")
  try:
    sid = int(request.GET['q'])
  except:
    sid = None
  
  callback_data = []

  if sid is None:
    callback_data.append(u"無商戶資訊")
  
  if request.method == "POST":
    print("request POST = ", request.POST)
    print("request BODY = ", request.body, type(request.body))
    data_list = request.body.split('&')
    print("data_list = ", data_list)

    #print("json_data = ", type(request.body))
    #decodebody = request.body.decode('utf-8')
    #json_data = json.loads(decodebody)
    #print("json_data = ", json_data, type(json_data))
  
  return HttpResponse("success")
  

#####################################################################
