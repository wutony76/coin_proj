from __future__ import print_function
from cStringIO import StringIO
import msgpack
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from fatcat.conf import settings as _settings
from spider.rpcclient import RPCClient
from spider.consts import LogMsgOpts
from fdpays import time_utils
from fdpays.consts import LogMsgDataOpts
from store_site.site_utils import _Pagination
#from debug_site.site_utils import _Pagination

def new_log_index_cli():
  return  RPCClient(_settings.PAY_LOG_INDEX_ADDR)

def new_log_data_cli():
  return  RPCClient(_settings.PAY_LOG_DATA_ADDR)

def index_view(request):

  cli = new_log_index_cli()

  rtn = cli.call('GET_HOUR_INDEX', None)
  print('GET_HOUR_INDEX', rtn)

  rtn = rtn[::-1]
  objs = []

  for ix_time, meta in rtn:
    _ix_time = str(ix_time)
    year = _ix_time[:4]
    month = _ix_time[4:6]
    day = _ix_time[6:8]
    hour = _ix_time[8:10]

    time_desc = '%s-%s-%s %s:00:00' % (year, month, day, hour)
    start_time = _ix_time
    meta.update({
      'time_desc': time_desc,
      'start_time': start_time,
      #'end_time': end_time,
    })

    objs.append(meta)
    

  return TemplateResponse(request, 'log/index.html', {
    'objs': objs,
  })

def hour_seq_index_view(request):

  cli = new_log_index_cli()

  _ix_time = request.GET['q']
  year = int(_ix_time[:4])
  month = int(_ix_time[4:6])
  day = int(_ix_time[6:8])
  hour = int(_ix_time[8:10])
  #end = int(request.GET['3'])
  start_time = '%04d%02d%02d%02d%02d%02d' % (year, month, day, hour, 0, 0)
  end_time = '%04d%02d%02d%02d%02d%02d' % (year, month, day, hour, 59, 59)

  rtn = cli.call('ITEMS_HOUR_SEQ', None, start_time, end_time)
  print('ITEMS_HOUR_SEQ', rtn)

  objs = []

  rtn = sorted(rtn, key=lambda x: x['ts'])

  for obj in rtn:
    ts = obj['ts']
    tag = obj['tag']
    dt = time_utils.ts_to_tz_shanghai(ts)
    opts = tag['opts']
    data_codes = tag['data_codes']
    admin_ids = tag['admin_ids']
    ant_ids = tag['ant_ids']
    out_sns = tag['out_sns']
    path_infos = tag['path_infos']

    opts_desc = []
    for op in opts:
      opts_desc.append(LogMsgOpts.get_desc2(op))


    data_desc = []

    for data_code in data_codes:
      data_desc.append(LogMsgDataOpts.get_desc2(data_code))

    obj['time_desc'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    obj['admin_id'] = ', '.join([str(a) for a in admin_ids])
    obj['ant_id'] = ', '.join([str(a) for a in ant_ids])
    obj['out_sn'] = ', '.join(out_sns)
    obj['opts_desc'] = u', '.join(opts_desc)
    obj['path_info'] = u', '.join(path_infos)
    obj['data_desc'] = u', '.join(data_desc)

    objs.append(obj)


  start_time = '%04d-%02d-%02d %02d:%02d:%02d' % (year, month, day, hour, 0, 0)

  return TemplateResponse(request, 'log/hour_seqid.html', {
    'start_time': start_time,
    'objs': objs,
  })

LOGMSG_DATA_OPTS = [
  LogMsgOpts.DATA,
  LogMsgOpts.SYS_DATA,
  LogMsgOpts.APP_DATA,
  LogMsgOpts.DEBUG_DATA,
]

def _make_data_desc(ctx):
  data_html = obj_to_html(data)
  data_html = mark_safe(data_html)

class DataRow(object):

  def __init__(self, ctx):
    self.ctx = ctx
  
  def make_row(self):
    print('make_row')
    data = self.ctx['data']
    ctx = dict(self.ctx)

    rep = None

    data_html = obj_to_html(data)
    data_html = mark_safe(data_html)
    ctx['data'] = data_html

    rep = render_to_string('log/seq_logs_row.html', {
      'obj': ctx,
    })

    if rep is None:
      rep = render_to_string('log/seq_logs_row.html', {
        'obj': ctx,
      })
    return rep

def seq_items_view(request):

  q_seqid = request.GET['q']

  cli = new_log_index_cli()
  data_cli = new_log_data_cli()

  logids = cli.call('GET_SEQ_LOGIDS', None, q_seqid)[0]
  logdatas = []
  if logids:
    logdatas = data_cli.call('GET', None, *logids)

  objs = []
  for logid, logdata in zip(logids, logdatas):
    op, ts, seqid, data = logdata

    #print('logmsg', logmsg)
    dt = time_utils.ts_to_tz_shanghai(ts)
    time_desc = dt.strftime('%Y-%m-%d %H:%M:%S')

    desc = ''

    if op in LOGMSG_DATA_OPTS:
      if data.has_key('code'):
        desc = LogMsgDataOpts.get_desc2(data['code'])

    #data_html = obj_to_html(data)
    #data_html = mark_safe(data_html)
    #a = str(data_html)
    #print('seq_logs', op)
    ctx = {
      'op': op,
      'ts': ts,
      'seqid': seqid,
      'data': data,
      'desc': desc,
      'time_desc': time_desc,
      #'data_html': data_html,
    }
    obj = DataRow(ctx)
    print('obj', obj)
    objs.append(obj)



  return TemplateResponse(request, 'log/seq_logs.html', {
    'seqid': q_seqid,
    'objs': objs,
  })


def find_view(request):
  q_text = request.GET['q'].strip()

  cli = new_log_index_cli()
  data_cli = new_log_data_cli()
  logids = cli.call('FIND_TEXT', None, q_text)[0]
  #print('FIND_TEXT=%s' % q_text, logids)
  print('FIND_TEXT=%s' % q_text, 'rtn', len(logids))
  logdatas = []
  if logids:
    _logids = list(logids)
    limit = 256
    while len(_logids) > 0:
      pks, _logids = _logids[:limit], _logids[limit:]
      rtn = data_cli.call('GET', None, *pks)
      logdatas.extend(rtn)

  objs = []

  for logid, logdata in zip(logids, logdatas):
    op, ts, seqid, data = logdata

    dt = time_utils.ts_to_tz_shanghai(ts)
    time_desc = dt.strftime('%Y-%m-%d %H:%M:%S')
    op2_desc = None

    data_html = obj_to_html(data)
    data_html = mark_safe(data_html)

    if isinstance(data, dict):
      if data.has_key('code'):
        op2 = data['code']
        op2_desc = LogMsgDataOpts.get_desc2(op2)

    obj = {
      'op': LogMsgOpts.get_desc2(op),
      'op2': op2_desc,
      'ts': ts,
      'seqid': seqid,
      'data_html': data_html,
      'time_desc': time_desc,
    }
    objs.append(obj)

  return TemplateResponse(request, 'log/find.html', {
    'objs': objs,
    'q_text': q_text,
  })

def scan_view(request):

  query = {}

  page_number = 1
  perpage = 1000
  try:
    page_number = int(request.GET['page'])
  except:
    pass

  if page_number < 1:
    page_number = 1

  offset = (page_number-1)*perpage
  limit = perpage




  if 'data_code' in request.GET:
    data_code = int(request.GET['data_code'])
    query['data_code'] = data_code

  if 'command' in request.GET:
    command = request.GET['command']
    query['command'] = command

  if 'admin_id' in request.GET:
    admin_id = int(request.GET['admin_id'])
    query['admin_id'] = admin_id

  cli = new_log_index_cli()
  data_cli = new_log_data_cli()


  rtn = cli.call('SCAN', None, query)
  #print('SCAN rtn', rtn)
  all_logids = rtn[0]
  total_count = len(all_logids)
  print('SCAN', 'all_logids count', total_count)
  logids = all_logids[offset:offset+limit]

  logdatas = []
  if logids:
    logdatas = data_cli.call('GET', None, *logids)
    #print('logdatas', logdatas)

  objs = []

  seqids = set()

  for logid, logdata in zip(logids, logdatas):
    op, ts, seqid, data = logdata
    seqids.add(seqid)
  seqids = sorted(seqids)
  #print('seqids', seqids)
  tagdata_by_seqid = {}
  if seqids:
    tagdatas = cli.call('GET_TAG_DATA', None, *seqids)
    for seqid, tagdata in zip(seqids, tagdatas):
      tagdata_by_seqid[seqid] = tagdata

  for logid, logdata in zip(logids, logdatas):
    op, ts, seqid, data = logdata

    tagdata = tagdata_by_seqid[seqid]
    print('logid', logid, 'seqid', seqid, 'tagdata', tagdata)

    dt = time_utils.ts_to_tz_shanghai(ts)
    time_desc = dt.strftime('%Y-%m-%d %H:%M:%S')

    data_html = obj_to_html(data)
    data_html = mark_safe(data_html)

    obj = {
      'op': op,
      'data_code': data.get('code', None),
      'seqid': seqid,
      'data': data,
      'data_html': data_html,
      'time_desc': time_desc,
      'tag': tagdata,
    }
    objs.append(obj)

  pagination = _Pagination(request, total_count, page_number, perpage)

  return TemplateResponse(request, 'log/scan.html', {
    #'seqid': q_seqid,
    'objs': objs,
    'pagination': pagination,
  })
    
    

def find_out_sn_view(request):
  q_out_sn = request.GET['q'].strip()

  cli = new_log_index_cli()
  seqids = cli.call('FIND_OUT_SN', None, q_out_sn)[0]
  #print('FIND_OUT_SN=%s' % q_out_sn, seqids)
  min_tss = []
  if seqids:
    min_tss = cli.call('GET_SEQID_MIN_TIME', None, *seqids)

  objs = []
  for seqid, ts in zip(seqids, min_tss):
    dt = time_utils.ts_to_tz_shanghai(ts)
    time_desc = dt.strftime('%Y-%m-%d %H:%M:%S')
    obj = {
      'seqid': seqid,
      'time_desc': time_desc,
    }
    objs.append(obj)

  return TemplateResponse(request, 'log/find_result.html', {
    'objs': objs,
    'q_out_sn': q_out_sn,
  })

def obj_to_html(data):
  if isinstance(data, dict):
    out = []
    out.append(u'<ul>')
    for k, v in data.items():
      out.append(u'<li>')
      out.append(u'%s: ' % k)
      a = obj_to_html(v)
      out.append(a)
      out.append(u'</li>')
      
    out.append(u'</ul>')

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
    buf = StringIO()
    buf.write(data)
    return buf.getvalue()

  buf = StringIO()
  buf.write(repr(data))
  return buf.getvalue()

