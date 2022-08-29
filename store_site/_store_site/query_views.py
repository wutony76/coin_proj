from __future__ import print_function
import json
from django.http import HttpResponse
from django.template.response import TemplateResponse
from fatcat.conf import settings as _settings
from dipay.rpcclient import HTTPRPCClient

def query_ix_view(request):

  query = {
    'limit': 1024,
  }
  if 'user_id' in request.GET:
    user_id = int(request.GET['user_id'])
    query['user_id'] = user_id

  cli = HTTPRPCClient(_settings.DIPAYIX_HTTP)

  rtn = cli.call('QUERY_ORDER', query)[0]

  pks = rtn['pks']
  orders = []
  if pks:
    orders = cli.call('LIST_ORDER', *pks)

  objs = []

  for pk, order in zip(pks, orders):
    print('pk', pk, order)

    objs.append(order)

  return TemplateResponse(request, 'query/ix.html', {
    'objs': objs,
  })
