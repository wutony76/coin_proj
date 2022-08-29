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
from store_site.models import System, CashOrder
from store_site.decorators import past_get_request 
from . import tools

# status   -1    新單
# status   0    成功 
# status   1    已過期
# status   2    等待付款中
# status   3    取消(admin)
# status   4    取消(ant)
# status   5    已付款待確認
CASH_NEW = -1 
CASH_SUCCESS = 0 
CASH_ORDERDUE = 1
CASH_WAITING_PAY = 2
CASH_CANCEL_ADMIN = 3 
CASH_CANCEL_ANT = 4 
CASH_PAYING = 5 



class CashOrderForm(forms.Form):
  #mobile =  forms.CharField( label='mobile' )
  #password = forms.CharField( label='password' )
  whose_id = forms.CharField( label='whose_id', initial = "test_ttt" )
  out_sn = forms.CharField( label='out_sn', initial = "-1" )
  sn = forms.CharField( label='sn', initial = "snc%s"% str(int(time.time()*1000)) )

  bank_code = forms.CharField( label='bank_code', initial="000" )
  bank_number = forms.CharField( label='bank_number', initial="0000000000" )
  money = forms.CharField( label='money', initial="1000" )
  remark = forms.CharField( label='remark', required=False )


class EditForm(forms.Form):
  bank_code = forms.CharField( label='bank_code', initial="000" )
  bank_number = forms.CharField( label='bank_number', initial="0000000000" )
  remark = forms.CharField( label='remark', required=False )


def list_view(request):
  print( "cash_list")
  cash_objs = list( CashOrder.objects.order_by('-id').values() )

  #print( cash_objs )

  ant_list = tools.data_cache.get("ant", None)
  if len(ant_list) == 0:
    ant_list = tools.cache_ant_list()
  print( "ant_list =", ant_list )


  return TemplateResponse(request, 'cash/list.html', {
    'cash_objs': cash_objs,
    'ants': ant_list,
  })


def add_view(request):
  return TemplateResponse(request, 'cash/create.html', {
      'form':CashOrderForm()
    })



def edit_view(request):
  try:
    c_id = int(request.GET['q'])
  except:
    c_id = None

  if c_id is None:
    redirect_to = reverse_url("cash_list")
    return HttpResponseRedirect(redirect_to)


  _data = CashOrder.objects.get( id = c_id )
  _form = EditForm(
           initial = {
             'bank_code':_data.bank_code,
             'bank_number':_data.bank_number,
             'remark':_data.remark,
           }        
         )
  return TemplateResponse(request, 'cash/edit.html', {
    'data':_data,
    'form':_form
  })




@past_get_request
def appoint_view(request):
  try:
    _id = request.POST['cash_id']
  except:
    _id = None
  if _id is None:
    redirect_to = reverse_url("cash_list")
    return HttpResponseRedirect(redirect_to)


  _ant = request.POST['ant']
  ####
  # status   -1   新單
  # status   0    成功 
  # status   1    已過期
  # status   2    等待付款中
  # status   3    取消(admin)
  # status   4    取消(ant)

  cash = CashOrder.objects.get( id = _id )
  #print("ttt appoint_view status.", cash.status, type(cash.status))
  this_cash = cash.status

  if this_cash is CASH_SUCCESS or this_cash is CASH_ORDERDUE or this_cash is CASH_CANCEL_ADMIN or this_cash is CASH_CANCEL_ANT:
    #print("ttt status1. is return." )

    msg = u"%s 訂單無法指派" % cash.sn 
    return HttpResponse(msg)

    #redirect_to = reverse_url("cash_list")
    #return HttpResponseRedirect(redirect_to)

  cash.ant_id = _ant
  cash.status = CASH_WAITING_PAY
  cash.save()
  #print("ttt appoint_view save.")

  redirect_to = reverse_url("cash_list")
  return HttpResponseRedirect(redirect_to)



@past_get_request
def save_view(request):
  #if request.method == 'GET':
  #  redirect_to = reverse_url("cash_list")
  #  return HttpResponseRedirect(redirect_to)

  #POST
  try:
    _id = request.POST['id']
  except:
    _id = None
  print( "save_id =", _id )


  if _id is None:
    form = CashOrderForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      print( "data ", data )

      #is-add
      #_sys = System.objects.get( id = 0 )
      #_n = _sys.ant_index + 1
      _n = tools.get_cash_index()
      _num = "%08d" % _n
      #_cash_id = "C_"+str(_num)

      #_key = uuid.uuid4()
      #_key2 = str(_key.hex) 
      #_mobile = data['mobile']
      #_password = data['password']

      _remark = data['remark']
      now_time = int(time.time()) 

      cash = CashOrder(
               #id = _cash_id,
               whose_id = data['whose_id'],
               out_sn = data['out_sn'],
               sn = "%s%s"%( data['sn'], str(_num) ),
               bank_code = data['bank_code'],
               bank_number = data['bank_number'],
               money = data['money'],

               status = CASH_NEW, # -1,
               remark = _remark,
               create_time = now_time)
      cash.save()
      tools.save_cash_index(_n)


  else:
    form = EditForm(request.POST)
    if form.is_valid():
      #is-edit
      #_remark = request.POST['remark']
      print( "cash _id =", _id )
      cash = CashOrder.objects.get( id = _id )

      if cash.status is not CASH_NEW:
        #redirect_to = reverse_url("cash_list")
        msg = u'訂單無法修改資訊, 請如需修改請重新加單'
        return HttpResponse(msg)


      data = form.cleaned_data
      cash.bank_code = data['bank_code']
      cash.bank_number = data['bank_number']
      cash.remark = data['remark']
      cash.save()

    print("CASH_SAVE SUCCESS.", cash.id)

  redirect_to = reverse_url("cash_list")
  return HttpResponseRedirect(redirect_to)



def cancel_view(request):

  try:
    _id = request.GET['q']
  except:
    _id = None
  print( "click cancel.", _id)


  cash = CashOrder.objects.get( id = _id )
  print( "click cash.", cash)
  if cash is None:
    msg = u'訂單錯誤'
    return HttpResponse(msg)

  if cash.status is CASH_CANCEL_ADMIN or cash.status is CASH_CANCEL_ANT:
    msg = u'訂單已取消'
    return HttpResponse(msg)

  cash.status = CASH_CANCEL_ADMIN
  cash.save()

  redirect_to = reverse_url("cash_list")
  return HttpResponseRedirect(redirect_to)




def success_view(request):
  try:
    _id = request.GET['q']
  except:
    _id = None
  print( "success.", _id)

  cash = CashOrder.objects.get( id = _id )
  if cash is None:
    msg = u'訂單錯誤'
    return HttpResponse(msg)

  if cash.status is CASH_NEW or cash.ant_id is None or len(cash.ant_id) == 0:
    msg = u'訂單未指派'
    return HttpResponse(msg)

  if cash.status is CASH_SUCCESS:
    msg = u'訂單已完成'
    return HttpResponse(msg)


  cash.status = CASH_SUCCESS
  cash.save()

  redirect_to = reverse_url("cash_list")
  return HttpResponseRedirect(redirect_to)






