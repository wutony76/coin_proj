from __future__ import print_function
from django.template.response import TemplateResponse
from fatcat.conf import settings as _settings
from spider.rpcclient import RPCClient

def new_cli():
  #return  RPCClient(_settings.PAY_VPS_INFO_ADDR)
  return  RPCClient(_settings.TEST_STORE_DB_ADDR)

def table_list_view(request):
  cli = new_cli()
  rtn = cli.call('TABLE_SCHEMA', None)
  print('TABLE_SCHEMA', rtn)
  objs = []
  for info in rtn:
    objs.append(info)

  return TemplateResponse(request, 'store/db/tables.html', {
    'objs': objs,
  })

def table_page_view(request):
  table_name = request.GET['t']

  cli = new_cli()

  rtn = cli.call('TABLE_SCHEMA', None)
  print('TABLE_SCHEMA', rtn)
  table_info_by_name = {}
  for info in rtn:
    table_info_by_name[info['name']] = info

  table_info = table_info_by_name[table_name]
  cols = table_info['cols']

  query = {}
  order_by = ['-create_time', '-id']
  offset = 0
  limit = 100

  q = {
    'name': table_name,
    'query': query,
    'order_by': order_by,
    'limit': limit,
  }

  rtn = cli.call('TABLE_QUERY', None, q)[0]
  print('TABLE_QUERY', rtn)
  ids = rtn['ids']
  total_count = rtn['total_count']


  objs = cli.call('TABLE_GET_ROW', None, table_name, ids)[0]
  print('TABLE_GET_ROW', objs)
  for obj in objs:
    vals = []
    for col in cols:
      col_name = col['name']
      val = obj.get(col_name, None)
      vals.append(val)
    obj['row_vals'] = vals
  

  return TemplateResponse(request, 'store/db/table_query.html', {
    'cols': cols,
    'objs': objs,
  })
