from __future__ import print_function

from io import StringIO
#from cStringIO import StringIO
import json
import time
import uuid


from django import forms
from django.urls import reverse as reverse_url
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.html import mark_safe

from fcworks.conf import settings as _settings
from store_site.models import System, AntUser
from . import tools



class AntForm(forms.Form):
  mobile =  forms.CharField( label='mobile' )
  password = forms.CharField( label='password' )
  remark = forms.CharField( label='remark', required=False )


def list_view(request):
  ant_user_objs = list( AntUser.objects.values() )
  print(ant_user_objs)

  #print( "index", tools.get_ant_index())
  return TemplateResponse(request, 'ant/list.html', {
    'ant_user_objs': ant_user_objs,
  })


def add_view(request):

  return TemplateResponse(request, 'ant/create.html', {
      'form':AntForm()
    })



def edit_view(request):
  try:
    a_id = int(request.GET['q'])
  except:
    a_id = None

  if a_id is None:
    redirect_to = reverse_url("ant_list")
    return HttpResponseRedirect(redirect_to)

  _data = AntUser.objects.get( id = a_id )
  _ant_form = AntForm(
           initial = {
             'mobile':_data.mobile,
             'password':_data.password,
           }        
         )

  return TemplateResponse(request, 'ant/edit.html', {
    'data':_data,
    'form':_ant_form
  })




def save_view(request):
  if request.method == 'GET':
    redirect_to = reverse_url("ant_list")
    return HttpResponseRedirect(redirect_to)

  #POST
  try:
    _id = request.POST['id']
  except:
    _id = None

  form = AntForm(request.POST)
  if form.is_valid():
    data = form.cleaned_data
    print( data )

    if _id is None:
    #is-add
      #_sys = System.objects.get( id = 0 )
      #_n = _sys.ant_index + 1
      _n = tools.get_ant_index()
      _num = "%05d" % _n
      _ant_id = "A_"+str(_num)
      _key = uuid.uuid4()
      _key2 = str(_key.hex) 
      _mobile = data['mobile']
      _password = data['password']
      _remark = data['remark']
      now_time = int(time.time()) 
      ant = AntUser(
              ant_id = _ant_id, 
              #ant_id = str(_ant_id.hex), 
              mobile = _mobile,
              password = str(tools.hashlib_password( _key, _password )),
              remark = _remark,
              key = _key2, 
              create_time = now_time)
      ant.save()

      tools.save_ant_index(_n)
      #system = System.objects.get( id = 0 )
      #system.ant_index = _n
      #system.save()

    else:
    #is-edit
      #_remark = request.POST['remark']
      print( "_id =", _id )
      ant = AntUser.objects.get( id = _id )
      _password = data['password']
      new_password = str(tools.hashlib_password( ant.key, _password )) 

      if len(_password ) == 64 or len(_password ) == 0:
        new_password = ant.password

      ant.mobile = data['mobile']
      ant.password = new_password 
      ant.remark = data['remark']
      ant.save()

    print("save", ant.id)
    #tools.cache_ant_list()
    ant_list = tools.cache_ant_list()
    print("save ant_list", ant_list)

  redirect_to = reverse_url("ant_list")
  return HttpResponseRedirect(redirect_to)
