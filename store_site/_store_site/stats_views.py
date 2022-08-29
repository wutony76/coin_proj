from __future__ import print_function
import time
from datetime import datetime, timedelta
from cStringIO import StringIO
from django.template.response import TemplateResponse
from dipay.models import OrderInfo, LowerhairInfo
from fdpays import time_utils

def index_view(request):

  now_ts = time.time()
  now = time_utils.ts_to_tz_shanghai(now_ts)
  today = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=time_utils.TZ_SHANGHAI)
  
  out = []
  i_dates = []

  d = today
  for i in xrange(3):
    i_dates.append(d)
    d = d - timedelta(days=1)

  order_tree, admin_ids1 = query_orders(i_dates)
  lower_tree, admin_ids2 =  query_lowers(i_dates)

  admin_ids = sorted(set(admin_ids1 + admin_ids2))
  status_arr = [0, 1, 2, 3, 4]

  for date in i_dates:

    rows = []

    for admin_id in admin_ids:
      i_k = (admin_id, date.year, date.month, date.day)

      try:
        order = order_tree[i_k]
      except KeyError:
        order = {}

      try:
        lower = lower_tree[i_k]
      except KeyError:
        lower = {}

      obj = {
        'admin_id': admin_id,
        'order': order,
        'lower': lower,
      }
      rows.append(obj)

    total_row = {
      'admin_id': 'total',
    }
    for info_name in ['order', 'lower']:
      
      _obj = {}


      for row in rows:
        info = row[info_name]
        for status in status_arr:
          prefix = 'status_%s' % status
          name_count = '%s_count' % prefix
          name = '%s_total_money' % prefix
          _obj[name] = _obj.get(name, 0) + info.get(name, 0) 
          _obj[name_count] = _obj.get(name_count, 0) + info.get(name_count, 0) 

        #print('row', row)

      for status in status_arr:
        prefix = 'status_%s' % status
        name_count = '%s_count' % prefix
        name_count2 = '%s_desc' % name_count

        name = '%s_total_money' % prefix
        name2 = '%s_desc' % name

        _obj[name2] = '{:,}'.format(_obj.get(name, 0))
        _obj[name_count2] = '{:,}'.format(_obj.get(name_count, 0))
      #print('total', total_row)
      #print('_obj', name, _obj)
      total_row[info_name] = _obj

    rows.append(total_row)


    info = {
      'date': date,
      'rows': rows,
    }
    out.append(info)

  
  return TemplateResponse(request, 'stats/index.html', {
    'groups': out,
    #'orders': orders,
  })

def query_orders(dates):
  tree = {}
  all_admin_ids = set()

  _dates = sorted(dates)
  start_dt = _dates[0]
  start_ts = time_utils.tz_shanghai_to_ts(start_dt)
  print('start_dt', start_dt)

  qs = OrderInfo.objects.filter(create_time__gte=start_ts).all()
  #qs = OrderInfo.objects.all()

  limit = 1024
  offset = 0
  for i in xrange(16):
    objs = list(qs[offset:offset+limit])
    print('offset=%s limit=%s orders=%s' % (offset, limit, len(objs)))

    if len(objs) == 0:
      break
    offset += limit

    for obj in objs:
      create_time_ts = obj.create_time
      admin_id = obj.admin_id
      status = obj.status

      create_time = time_utils.ts_to_tz_shanghai(create_time_ts)
      i_date = (create_time.year, create_time.month, create_time.day)

      if tree.has_key(i_date) == False:
        tree[i_date] = {}

      node1 = tree[i_date]

      k2 = (admin_id, status)
      if node1.has_key(k2) == False:
        node1[k2] = []
      arr = node1[k2]
      arr.append(obj)
  
  out = {}

  status_arr = [0, 1, 2, 3, 4]
  ix_dates = sorted(tree.keys())[::-1]
  for ix_date in ix_dates:
    year, month, day = ix_date

    node1 = tree[ix_date]
    admin_ids = set()
    for x, _ in node1.items():
      admin_id, status = x
      admin_ids.add(admin_id)

    admin_ids = sorted(admin_ids)
    rows = []
    #print('admin_ids', admin_ids)
    for admin_id in admin_ids:
      row = {
        'admin_id': admin_id,
      }

      all_admin_ids.add(admin_id)


      rows.append(row)
      for status in status_arr:
        k2 = (admin_id, status)

        total_money = 0
        total_count = 0

        if node1.has_key(k2):
          objs = node1[k2]

          for obj in objs:
            total_count += 1
            total_money = total_money + round(obj.money)
        total_money = round(total_money, 2)

        prefix = 'status_%s' % status

        name_count = '%s_count' % prefix
        name = '%s_total_money' % prefix
        name2 = '%s_desc' % name

        row[name_count] = total_count
        row[name] = total_money
        row[name2] = '{:,}'.format(total_money)

      i_k = (admin_id, year, month, day)
      out[i_k] = row

    """

    stats = {
      'year': year,
      'month': month,
      'day': day,
      'rows': rows,
    }
    i_k = (year, month, day)

    out[i_k] = rows
    """

  return out, sorted(all_admin_ids)

def query_lowers(dates):
  tree = {}
  all_admin_ids = set()

  _dates = sorted(dates)
  start_dt = _dates[0]
  start_ts = time_utils.tz_shanghai_to_ts(start_dt)
  print('start_dt', start_dt)

  qs = LowerhairInfo.objects.filter(create_time__gte=start_ts).all()

  limit = 1024
  offset = 0
  for i in xrange(16):
    objs = list(qs[offset:offset+limit])
    print('offset=%s limit=%s orders=%s' % (offset, limit, len(objs)))

    if len(objs) == 0:
      break
    offset += limit

    for obj in objs:
      create_time_ts = obj.create_time
      admin_id = obj.admin_id
      status = obj.status

      create_time = time_utils.ts_to_tz_shanghai(create_time_ts)
      i_date = (create_time.year, create_time.month, create_time.day)

      if tree.has_key(i_date) == False:
        tree[i_date] = {}

      node1 = tree[i_date]

      k2 = (admin_id, status)
      if node1.has_key(k2) == False:
        node1[k2] = []
      arr = node1[k2]
      arr.append(obj)
  
  out = {}

  status_arr = [0, 1, 2, 3, 4]
  ix_dates = sorted(tree.keys())[::-1]
  for ix_date in ix_dates:
    year, month, day = ix_date

    node1 = tree[ix_date]
    admin_ids = set()
    for x, _ in node1.items():
      admin_id, status = x
      admin_ids.add(admin_id)

    admin_ids = sorted(admin_ids)
    rows = []
    #print('admin_ids', admin_ids)
    for admin_id in admin_ids:
      row = {
        'admin_id': admin_id,
      }

      all_admin_ids.add(admin_id)


      rows.append(row)
      for status in status_arr:
        k2 = (admin_id, status)

        total_money = 0
        total_count = 0

        if node1.has_key(k2):
          objs = node1[k2]

          for obj in objs:
            total_count += 1
            total_money = total_money + round(obj.money)
        total_money = round(total_money, 2)

        prefix = 'status_%s' % status

        name_count = '%s_count' % prefix
        name = '%s_total_money' % prefix
        name2 = '%s_desc' % name

        row[name_count] = total_count
        row[name] = total_money
        row[name2] = '{:,}'.format(total_money)

      i_k = (admin_id, year, month, day)
      out[i_k] = row

    """
    total_row = {
      'admin_id': 'total',
    }
    for row in rows:
      for status in status_arr:
        prefix = 'status_%s' % status
        name_count = '%s_count' % prefix
        name = '%s_total_money' % prefix
        total_row[name] = total_row.get(name, 0) + row.get(name, 0) 
        total_row[name_count] = total_row.get(name_count, 0) + row.get(name_count, 0) 

      #print('row', row)

    for status in status_arr:
      prefix = 'status_%s' % status
      name_count = '%s_count' % prefix
      name_count2 = '%s_desc' % name_count

      name = '%s_total_money' % prefix
      name2 = '%s_desc' % name

      total_row[name2] = '{:,}'.format(total_row.get(name, 0))
      total_row[name_count2] = '{:,}'.format(total_row.get(name_count, 0))

    #print('total', total_row)

    roows.append(total_row)

    stats = {
      'year': year,
      'month': month,
      'day': day,
      'rows': rows,
    }
    i_k = (year, month, day)

    out[i_k] = rows
    """

  return out, sorted(all_admin_ids)
