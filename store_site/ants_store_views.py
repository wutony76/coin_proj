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



def cash_list(request):
  try:
    _ant = request.GET['q']
  except:
    _ant = None

  if _ant is None:
    redirect_to = reverse_url("index")
    return HttpResponseRedirect(redirect_to)

  cash_objs = list( CashOrder.objects.order_by('-id').filter(ant_id = _ant) )
  return TemplateResponse(request, 'ant_block/cash/list.html', {
    'ant_id': _ant,
    'cash_objs': cash_objs,
  })


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
