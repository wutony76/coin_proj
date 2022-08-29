from __future__ import print_function

from io import StringIO
#from cStringIO import StringIO
import json
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from fcworks.conf import settings as _settings
#from fatcat.conf import settings as _settings
from siya.models import Account, AccountSet, AccountItem, LowerhairInfo
from dipay.models import OrderInfo, TaskInfo, AdminUser, AntUser
from spider.rpcclient import RPCClient
from spider.consts import LogMsgOpts
from spider import time_utils


def index(request):
  return TemplateResponse(request, 'index.html', {
  })

def account_set_list(request):

  objs = list(AccountSet.objects.order_by('-oid').all())

  return TemplateResponse(request, 'account_set.html', {
    'objs': objs,
  })

def account_item_list(request):

  objs = list(AccountItem.objects.order_by('-oid').all())

  return TemplateResponse(request, 'account_item.html', {
    'objs': objs,
  })

def task_list(request):
  offset = 0
  limit = 1024

  qs = TaskInfo.objects.order_by('-id')
  qs = qs[offset:(offset+limit)]
  order_objs = list(qs.values())

  return TemplateResponse(request, 'task_list.html', {
    'task_objs': order_objs,
  })

def order_list(request):
  offset = 0
  limit = 1024

  qs = OrderInfo.objects.order_by('-id')

  _filter = {}

  if 'remark' in request.GET:
    remark = request.GET['remark']
    _filter = {
      'remark__icontains': remark,
    }

  if _filter:
    qs = qs.filter(**_filter)

 

  qs = qs[offset:(offset+limit)]
  order_objs = list(qs.values())
  order_ids = []
  for order in order_objs: 
    order_ids.append(order["id"])

  task_infos = TaskInfo.objects.filter(orders_id__in=order_ids).values()
  task_info_by_order_id = {}
  for task_info in task_infos:
    
    task_info_by_order_id[task_info["orders_id"]] = task_info

  for order in order_objs: 
    task_info = task_info_by_order_id.get(order["id"], None)

    if task_info is not None:
      order["task_info"] = task_info
      

  return TemplateResponse(request, 'order_list.html', {
    'order_objs': order_objs,
  })

def ant_user_list(request):
  ant_user_objs = list(AntUser.objects.values())

  return TemplateResponse(request, 'ant_user_list.html', {
    'ant_user_objs': ant_user_objs,
  })

def admin_user_list(request):

  admin_user_objs = list(AdminUser.objects.values())
  #for obj in admin_objs:
  #  obj['_dict'] = model_to_dict(obj)

  return TemplateResponse(request, 'admin_user_list.html', {
    'admin_user_objs': admin_user_objs,
  })


def lowerhairs_list(request):

  objs = list(LowerhairInfo.objects.order_by('-id').values())
  #for obj in admin_objs:
  #  obj['_dict'] = model_to_dict(obj)

  return TemplateResponse(request, 'lowerhair_list.html', {
    'objs': objs,
  })


def seq_log_list_view(request):
  seqid = request.GET['q']

def seq_log_view(request):
  seqid = request.GET['q']

  addr = _settings.DIPAY_LOGINDEX_ADDR
  cli = RPCClient(addr)
  rows = cli.call(None, 'GET_REQ_LOGS', reqid)[0]
  print('reqid', reqid, 'rows', len(rows))
  objs = []
  for row in rows:
    op, ts, record = row
    dt = time_utils.ts_to_tz_shanghai(ts)

    #print(op, ts, record)

    reqid = record[0]
    data = record[1]
    msg = data

    if op in [MessageOpts.LOGIC_ERROR]:
      err, err_tb = data
      msg = ",".join([err, err_tb])

    if op in [MessageOpts.DEBUG_DATA]:
      #if isinstance(data, dict):
      #  msg = json.dumps(data)
      msg = mark_safe(obj_to_html(data))

    obj = {
      'op': op,
      'op_desc': MessageOpts.get_desc(op),
      'time': dt.strftime('%Y-%m-%d %H:%M:%S'),
      'msg': msg,
    }
    objs.append(obj)

  return TemplateResponse(request, 'req_log.html', {
    'objs': objs,
  })


def obj_to_html(data):
  if isinstance(data, dict):
    out = []
    out.append('<ul>')
    for k, v in data.items():
      out.append('<li>')
      out.append(u'%s: ' % k)
      a = obj_to_html(v)
      out.append(a)
      out.append('</li>')
      
    out.append('</ul>')

    buf = StringIO()
    for a in out:
      buf.write(a)
      buf.write('\n')

    return buf.getvalue()
  elif isinstance(data, list):
    out = []
    for a in data:
      b = obj_to_html(a)
      out.append(b)

    buf = StringIO()
    for a in out:
      buf.write(a)
      buf.write(', ')
      buf.write('\n')
    return buf.getvalue()

  elif isinstance(data, str):
    return data

  return repr(data)

