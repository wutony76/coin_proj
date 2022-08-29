from __future__ import print_function

import json
import time
import uuid
from io import StringIO

from django.urls import reverse as reverse_url
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django import forms

from fcworks.conf import settings as _settings
from store_site.models import System, PayOrder
from store_site.decorators import past_get_request 
from . import tools

# status   -1    新單
# status   0    成功 
# status   1    已過期
# status   2    等待付款中
# status   3    取消(admin)
# status   4    取消(ant)
# status   5    已付款待確認
PAY_NEW = -1 
PAY_SUCCESS = 0 
PAY_ORDERDUE = 1
PAY_WAITING_PAY = 2
PAY_CANCEL_ADMIN = 3 
PAY_CANCEL_ANT = 4 
PAY_PAYING = 5 



class PayOrderForm(forms.Form):
  #mobile =  forms.CharField( label='mobile' )
  #password = forms.CharField( label='password' )
  whose_id = forms.CharField( label='whose_id', initial = "test_ttt" )
  out_sn = forms.CharField( label='out_sn', initial = "-1" )
  sn = forms.CharField( label='sn', initial = "snp%s"% str(int(time.time()*1000)) )

  bank_code = forms.CharField( label='bank_code', initial="000" )
  bank_number = forms.CharField( label='bank_number', initial="0000000000" )
  bank_name = forms.CharField( label='bank_name', initial="test" )
  money = forms.CharField( label='money', initial="1000" )

  remark = forms.CharField( label='remark', required=False )


class EditForm(forms.Form):
  bank_code = forms.CharField( label='bank_code', initial="000" )
  bank_number = forms.CharField( label='bank_number', initial="0000000000" )
  remark = forms.CharField( label='remark', required=False )


def list_view(request):
  print( "pay_list")
  pay_objs = list( PayOrder.objects.order_by('-id').values() )

  #print( cash_objs )

  ant_list = tools.data_cache.get("ant", None)
  if len(ant_list) == 0:
    ant_list = tools.cache_ant_list()
  print( "ant_list =", ant_list )


  return TemplateResponse(request, 'pay/list.html', {
    'pay_objs': pay_objs,
    'ants': ant_list,
  })


def add_view(request):
  return TemplateResponse(request, 'pay/create.html', {
      'form':PayOrderForm()
    })



def edit_view(request):
  try:
    p_id = int(request.GET['q'])
  except:
    p_id = None

  if p_id is None:
    redirect_to = reverse_url("pay_list")
    return HttpResponseRedirect(redirect_to)


  _data = PayOrder.objects.get( id = p_id )
  _form = EditForm(
           initial = {
             'bank_code':_data.bank_code,
             'bank_number':_data.bank_number,
             'remark':_data.remark,
           }        
         )
  return TemplateResponse(request, 'pay/edit.html', {
    'data':_data,
    'form':_form
  })




@past_get_request
def appoint_view(request):
  try:
    _id = request.POST['pay_id']
  except:
    _id = None
  if _id is None:
    redirect_to = reverse_url("pay_list")
    return HttpResponseRedirect(redirect_to)


  _ant = request.POST['ant']
  ####
  # status   -1   新單
  # status   0    成功 
  # status   1    已過期
  # status   2    等待付款中
  # status   3    取消(admin)
  # status   4    取消(ant)

  pay = PayOrder.objects.get( id = _id )
  #print("ttt appoint_view status.", cash.status, type(cash.status))
  _status = pay.status

  if _status is PAY_SUCCESS or _status is PAY_ORDERDUE or _status is PAY_CANCEL_ADMIN or _status is PAY_CANCEL_ANT:
    #print("ttt status1. is return." )

    msg = u"%s 訂單無法指派" % pay.sn 
    return HttpResponse(msg)

    #redirect_to = reverse_url("cash_list")
    #return HttpResponseRedirect(redirect_to)

  pay.ant_id = _ant
  pay.status = PAY_WAITING_PAY
  pay.pair_time = int(time.time()) 
  pay.save()
  #print("ttt appoint_view save.")

  redirect_to = reverse_url("pay_list")
  return HttpResponseRedirect(redirect_to)


@past_get_request
def save_view(request):
  #if request.method == 'GET':
  #  redirect_to = reverse_url("cash_list" _data = PayOrder.objects.get( id = p_id ))
  #  return HttpResponseRedirect(redirect_to)

  #POST
  try:
    _id = request.POST['id']
  except:
    _id = None
  print( "save_id =", _id )


  if _id is None:
    form = PayOrderForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      print( "data ", data )

      #is-add
      #_sys = System.objects.get( id = 0 )
      #_n = _sys.ant_index + 1
      _n = tools.get_pay_index()
      _num = "%08d" % _n
      #_cash_id = "C_"+str(_num)

      #_key = uuid.uuid4()
      #_key2 = str(_key.hex) 
      #_mobile = data['mobile']
      #_password = data['password'] _data = PayOrder.objects.get( id = p_id )

      _remark = data['remark']
      now_time = int(time.time()) 

      pay = PayOrder(
               #id = _cash_id,
               whose_id = data['whose_id'],
               out_sn = data['out_sn'],
               order_key = tools.get_order_key(),   

               sn = "%s%s"%( data['sn'], str(_num) ),
               bank_code = data['bank_code'],
               bank_number = data['bank_number'],
               money = data['money'],

               status = PAY_NEW, # -1,
               remark = _remark,
               create_time = now_time
               #pay_time = -1
               )
      pay.save()
      tools.save_pay_index(_n)


  else:
    form = EditForm(request.POST)
    if form.is_valid():
      #is-edit
      #_remark = request.POST['remark']
      print( "pay_id =", _id )
      pay = PayOrder.objects.get( id = _id )

      if pay.status is not PAY_NEW:
        #redirect_to = reverse_url("cash_list")
        msg = u'訂單無法修改資訊, 請如需修改請重新加單'
        return HttpResponse(msg)


      data = form.cleaned_data
      pay.bank_code = data['bank_code']
      pay.bank_number = data['bank_number']
      pay.remark = data['remark']
      pay.save()

    print("PAY_SAVE SUCCESS.", pay.id)

  redirect_to = reverse_url("pay_list")
  return HttpResponseRedirect(redirect_to)



def cancel_view(request):

  try:
    _id = request.GET['q']
  except:
    _id = None
  print( "click cancel.", _id)

  pay = PayOrder.objects.get( id = _id )
  print( "click pay.", pay)
  if pay is None:
    msg = u'訂單錯誤'
    return HttpResponse(msg)

  if pay.status is PAY_CANCEL_ADMIN or pay.status is PAY_CANCEL_ANT:
    msg = u'訂單已取消'
    return HttpResponse(msg)

  pay.status = PAY_CANCEL_ADMIN
  pay.cancel_time = int(time.time()) 
  pay.save()

  redirect_to = reverse_url("pay_list")
  return HttpResponseRedirect(redirect_to)




def success_view(request):
  try:
    _id = request.GET['q']
  except:
    _id = None
  print( "success.", _id)

  pay = PayOrder.objects.get( id = _id )
  if pay is None:
    msg = u'訂單錯誤'
    return HttpResponse(msg)

  if pay.status is PAY_NEW or pay.ant_id is None or len(pay.ant_id) == 0:
    msg = u'訂單未指派'
    return HttpResponse(msg)

  if pay.status is PAY_SUCCESS:
    msg = u'訂單已完成'
    return HttpResponse(msg)


  pay.status = PAY_SUCCESS
  pay.save()

  redirect_to = reverse_url("pay_list")
  return HttpResponseRedirect(redirect_to)




def bank_view(request):
  try:
    _key = request.GET['q']
  except:
    _key = None
  if _key is None or _key is "-1" :
    msg = u'訂單錯誤'
    return HttpResponse(msg)

  _data = PayOrder.objects.get( order_key = _key )
  if _data.status is PAY_NEW or _data.ant_id is None or len(_data.ant_id) == 0:
    msg = u'訂單未指派'
    return HttpResponse(msg)

  return TemplateResponse(request, 'bank/index.html', {
    'title': u'代收資訊',
    'data': _data,
  })


def check_view(request):
  try:
    _key = request.GET['q']
  except:
    _key = None
  if _key is None:
    msg = u'訂單錯誤'
    return HttpResponse(msg)

  pay = PayOrder.objects.get( order_key = _key )

  if pay.status is PAY_NEW or pay.ant_id is None or len(pay.ant_id) == 0:
    msg = u'訂單未指派'
    return HttpResponse(msg)

  if pay.status is PAY_SUCCESS:
    msg = u'訂單已完成'
    return HttpResponse(msg)

  pay.status = PAY_PAYING
  pay.pay_time = int(time.time())
  pay.save()

  redirect_to = reverse_url("pay_list")
  return HttpResponseRedirect(redirect_to)
