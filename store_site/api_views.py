from __future__ import print_function

from io import StringIO
#from cStringIO import StringIO
import json
import time

from django.urls import reverse as reverse_url
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from fcworks.conf import settings as _settings


from store_site.models import CashOrder, PayOrder
from . import tools
from . import cash_views, pay_views 

def index(request):
  res = {
    "msg":"start coin api."
  } 
  return HttpResponse(res)


def past_get_request(fn):
  def inner(request, *args, **kwargs):
    #print("inner", request)
    if request.method == 'GET':
      #redirect_to = reverse_url("index")
      msg = "Errors mothed."
      res = {
        "code":1,
        "reason":msg
      } 
      return HttpResponse(res)

    return fn(request, *args, **kwargs)
  return inner


@past_get_request
def cash_add(request):

  _n = tools.get_cash_index()
  _num = "%08d" % _n
  _sn = "snc%s"% str(int(time.time()*1000))
  new_sn = "%s%s"%( _sn, str(_num) )

  _whose_id = request.POST['whose_id']
  _out_sn = request.POST['out_sn']

  _bank_code = request.POST['bank_code'],
  _bank_number = request.POST['bank_number'],
  _bank_name = request.POST['bank_name'],
  _money = request.POST['money'],

  _remark = data['remark']
  _status = cash_views.CASH_NEW, # -1, 
  now_time = int(time.time()) 

  cash = CashOrder(
           #id = _cash_id,
           whose_id = _whose_id,
           out_sn = _out_sn,
           sn = new_sn,
           bank_code = _bank_code,
           bank_number = _bank_number,
           bank_name = _bank_name,
           money = _money,
           status = _status, 
           remark = _remark,
           create_time = now_time
           )
  cash.save()
  tools.save_cash_index(_n)


  _data = {
    "sn": new_sn,
    "out_sn": _out_sn,
    "status": _status,
  }

  respone = {
    "code":0,
    "data":_data
  } 
  return HttpResponse(respone)







def paying_cash(request):
  try:
    _q = request.GET['q']
    _ant = request.GET['a']
  except:
    _q = None
    _ant = None

  print( "Paying q.", _q)
  cash = CashOrder.objects.get( id = _q ) 
  if cash.status == cash_views.CASH_PAYING:
    msg = u"訂單已付款" 
    return HttpResponse(msg)

  cash.status = cash_views.CASH_PAYING
  cash.pay_time = int(time.time())
  cash.save()

  redirect_to = reverse_url("ant_cash_list")+"?q="+_ant
  return HttpResponseRedirect(redirect_to)







def pay_list(request):
  try:
    _ant = request.GET['q']
  except:
    _ant = None

  if _ant is None:
    redirect_to = reverse_url("index")
    return HttpResponseRedirect(redirect_to)

  pay_objs = list( PayOrder.objects.order_by('-id').filter(ant_id = _ant) )
  return TemplateResponse(request, 'ant_block/pay/list.html', {
    'ant_id': _ant,
    'pay_objs': pay_objs,
  })


def paying_pay(request):
  try:
    _q = request.GET['q']
    _ant = request.GET['a']
  except:
    _q = None
    _ant = None

  print( "Paying q.", _q)
  pay = PayOrder.objects.get( id = _q ) 
  if pay.status == pay_views.PAY_PAYING:
    msg = u"訂單已收款" 
    return HttpResponse(msg)

  pay.status = pay_views.PAY_PAYING
  pay.pay_time = int(time.time())
  pay.save()

  redirect_to = reverse_url("ant_pay_list")+"?q="+_ant
  return HttpResponseRedirect(redirect_to)
