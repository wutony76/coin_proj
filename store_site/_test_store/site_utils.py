from __future__ import print_function
import io
import urllib
import math
from datetime import datetime, timedelta
import pytz
from django.utils.safestring import mark_safe

TZ_TW = pytz.timezone("Asia/Taipei")

class _Pagination(object):
  
  def __init__(self, request, total_count, page_number, perpage, link_count=10):
    self.request = request
    self.total_count = total_count
    self.page_number = page_number
    self.perpage = perpage
    self.opt_page_mid = link_count / 2
    self.opt_page_tail = link_count - 1

  def _make_link(self, text, klass, **kwargs):
    qs = {}
    for k in self.request.GET:
      qs[k] = self.request.GET[k]
    qs.update(kwargs)
    url = "%s?%s" % (self.request.path_info, urllib.urlencode(qs))

    return u'<li class="page-item %s"><a class="page-link" href="%s">%s</a></li>' % (" ".join(klass), url, text)

  def _iter_render(self):
    
    page_count = int(math.ceil(self.total_count / float(self.perpage)))

    yield '<div class="">'
    yield '<div class="">'
    yield u"<span>%s筆記錄</span>" % "{:,}".format(self.total_count)
    yield u"<span>共%s頁</span>" % page_count
    yield '</div>'
    yield '</div>'

    #yield '<div class="col-sm-6">'
    #yield '<div class="dataTables_paginate paging_simple_numbers">'
    #yield u'<ul class="pagination">'
    yield u'<ul class="pagination justify-content-center" style="margin-top: 15px;">'
    if self.page_number > 1:
      yield self._make_link(u"第1頁", [], page=1)

    prev_page_number = 1
    klass = []
    #klass.append("paginate_button")
    has_previous = True
    if self.page_number < 2:
      has_previous = False
    if has_previous:
      prev_page_number = self.page_number - 1
    else:
      klass.append("disabled")

    yield self._make_link(u"上一頁", klass, page=prev_page_number)

    #num_range = range(1, page_count+1)

    p_start = self.page_number - self.opt_page_mid
    if p_start < 1:
      p_start = 1

    p_end = p_start + self.opt_page_tail 
    if p_end > page_count:
      p_end = page_count

    for p in range(p_start, p_end+1):
      klass = []
      if p == self.page_number:
        klass.append("active")
      yield self._make_link(p, klass, page=p)

    
    next_page_number = 1
    klass = []
    if self.page_number < page_count:
      next_page_number = self.page_number + 1
    else:
      klass.append("disabled")

    yield self._make_link(u"下一頁", klass, page=next_page_number)

    yield self._make_link(u"最後頁", [], page=page_count)

    yield u"</ul>"
    #yield '</div>'
    #yield '</div>'


  def render(self):
    
    output = []
    for x in self._iter_render():
      output.append(x)

    return mark_safe(u"".join(output))


def make_filter_links(request, q_name, cast_type, options):
  cur_val = None
  try:
    cur_val = cast_type(request.GET[q_name])
  except KeyError:
    pass
  
  base_qs = {}
  for k in request.GET:
    base_qs[k] = request.GET[k]
  out = []
  for val, name in options:

    qs = dict(base_qs)
    try:
      qs.pop(q_name)
    except:
      pass

    if val is not None:
      qs[q_name] = val

    css_class = ""
    if cur_val == val:
      css_class = "selected"
    url = "%s?%s" % (request.path_info, urllib.urlencode(qs))
    out.append({
      "name": name,
      "url": url,
      "css_class": css_class,
    })
  return out

def timestamp_to_datetime(ts):
  dt = datetime.fromtimestamp(ts).replace(tzinfo=pytz.utc)
  dt = dt.astimezone(TZ_TW)
  return dt
