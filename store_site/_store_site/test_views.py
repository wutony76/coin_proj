from __future__ import print_function
import json
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from fatcat.conf import settings as _settings
from dipay.models import AdminUser, AntUser, OrderInfo, TaskInfo
from dipay.rpcclient import RPCClient

def calc_task_confirm(request):
  task_id = int(request.GET['task_id'])

  rpc_cli = RPCClient()
  rpc_cli.connect(_settings.DIPAY_LOGIC_ADDR)
  rtn = rpc_cli.call('CALC_TASK_CONFIRM', task_id)


  return JsonResponse({
    'rtn': rtn,
  })
