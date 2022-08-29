#!/usr/bin/python
# -*- coding: UTF-8 -*-


from __future__ import print_function
import pytz
import time
from datetime import datetime, timedelta 
#from datetime.datetime import astimezone
from cStringIO import StringIO
from django.http import HttpResponse
from django.template.response import TemplateResponse
#from dipay.models import OrderInfo, LowerhairInfo
#from fdpays import time_utils

from fatcat.conf import settings as _settings
from spider.rpcclient import RPCClient

from django.views.decorators.csrf import csrf_exempt
from site_utils import timestamp_to_datetime as ts_to_dt

ts_to_dt

VPS_INFO_HK = {}
VPS_INFO_TOKYO = {}
VPS_INFO_SEL = {}
VPS_INFO =  {
  #---HK---
  'ip-10-0-0-230':'HK-CALLBACK',
  'ip-10-0-0-156':'HK-API',
  'ip-10-0-0-110':'HK-WEB2',
  'ip-10-0-0-228':'HK-ANT-BACKUP(backup.)',
  'ip-10-0-0-75':'HK-ANT1',
  'ip-10-0-0-151':'HK-STATIC',
  'ip-10-0-0-213':'HK-ENTER',

  'ip-10-0-1-101':'HK-DB',
  'ip-10-0-1-103':'HK-LOGIC(no use.)',
  'ip-10-0-1-209':'HK-LOG',
  'ip-10-0-1-176':'HK-BROKER1',
  'ip-10-0-1-236':'HK-BROKER2',
  'ip-10-0-1-248':'HK-LOGIC3',

  'http://18.162.118.7:8081':'HK-e.web',
  'http://18.162.37.130:8300':'HK-e.ant',
  'http://18.163.176.106:8080':'HK-e.api',
  'http://16.162.159.131:8085':'HK-e.log',


  #---SEL---
  'ip-13-0-0-44':'SEL-WEB',
  'ip-13-0-0-51':'SEL-API',
  'ip-13-0-0-104':'SEL-ENTER',

  'ip-13-0-1-190':'SEL-DB',
  'ip-13-0-1-177':'SEL-LOGIC',
  'ip-13-0-1-202':'SEL-BROKER1',
  'ip-13-0-1-64':'SEL-BROKER2',

  'http://13.124.70.143:8081':'SEL-e.web',
  'http://13.124.70.143:8300':'SEL-e.ant',
  'http://3.37.170.246:8080':'SEL-e.api',
  'http://3.37.205.113:8085':'SEL-e.log',


  #---TOKYO---
  'ip-10-0-0-17':'TOKYO-WEB',
  'ip-10-0-0-234':'TOKYO-API',
  'ip-10-0-0-247':'TOKYO-ENTER',

  'ip-10-0-1-100':'TOKYO-DB',
  'ip-10-0-1-9':'TOKYO-LOGIC',

  'http://54.95.200.135:8081':'TOKYO-e.web',
  'http://54.95.200.135:8300':'TOKYO-e.ant',
  'http://54.199.80.255:8080':'TOKYO-e.api',
  'http://3.115.201.240:8085':'TOKYO-e.log',
} 





def new_cli():
  return  RPCClient(_settings.PAY_VPS_INFO_ADDR)


def index_view(request):
  cli = new_cli()
  #print( "cli=", cli)
  rtn = cli.call("LIST_MACHINE_INFO", None)
  #print( "rtn=", rtn)

  #print( "rtn=")
  for k, v in rtn.items():
    var_mem = v["mem"]
    try:
      v["int_mem"] = float(var_mem)
    except:
      v["int_mem"] = 0 


    var_disk = v["disk"]
    try:
      v["int_disk"] = float(var_disk)
    except:
      v["int_disk"] = 0 


    var_cpu = v["cpu"]
    try:
      v["int_cpu"] = float(var_cpu)
    except:
      v["int_cpu"] = 0 


  default_data = {
    "name":"-",
    "disk":"-",
    "cpu":"-",
    "mem":"-",
    #"timer": tw_dt.strftime("%Y/%m/%d %H:%M:%S"),
    "conn":"-",
    "serv":"-",
  }

  # HK #
  hk_desc_ip=[
    'ip-10-0-0-230',
    'ip-10-0-0-156',
    'ip-10-0-0-110',
    'ip-10-0-0-228',
    'ip-10-0-0-75',
    'ip-10-0-0-151',
    'ip-10-0-0-213',

    'ip-10-0-1-101',
    'ip-10-0-1-103',
    'ip-10-0-1-209',
    'ip-10-0-1-176',
    'ip-10-0-1-236',
    'ip-10-0-1-248',

    'http://18.162.118.7:8081',
    'http://18.162.37.130:8300',
    'http://18.163.176.106:8080',
    'http://16.162.159.131:8085',
  ]
  hk = {} 
  for host in hk_desc_ip:
    hk[host] = rtn.get(host, default_data)

  # SEL #
  sel_desc_ip=[
    'ip-13-0-0-44',
    'ip-13-0-0-51',
    'ip-13-0-0-104',
    'ip-13-0-1-64',
    'ip-13-0-1-202',
    'ip-13-0-1-177',
    'ip-13-0-1-190',

    'http://13.124.70.143:8081',
    'http://13.124.70.143:8300',
    'http://3.37.170.246:8080',
    'http://3.37.205.113:8085',
  ]
  sel = {} 
  for host in sel_desc_ip:
    sel[host] = rtn.get(host, default_data)

  # TOKYO  #
  tokyo_desc_ip=[
    'ip-10-0-0-247',
    'ip-10-0-0-17',
    'ip-10-0-0-234',
    'ip-10-0-1-100',
    'ip-10-0-1-9',

    'http://54.95.200.135:8081',
    'http://54.95.200.135:8300',
    'http://54.199.80.255:8080',
    'http://3.115.201.240:8085',
  ]
  tokyo = {} 
  for host in tokyo_desc_ip:
    tokyo[host] = rtn.get(host, default_data)
    #print("item =", item)

  return TemplateResponse(request, 'infos/index.html', {
    'hk': hk,
    'sel': sel,
    'tokyo': tokyo,
    'all': rtn,
  })


def add_data( cont_dict, key ):
  #tw = pytz.timezone('Asia/Taipei')
  #ts = time.time()
  #time = datetime.fromtimestamp(ts).replace(tzinfo=tw)
  #print ("time = ", time)
  
#  ts.astimezone
  cont_dict[key] = {
    "name":"-",
    "disk":"-",
    "cpu":"-",
    "mem":"-",
    #"timer": tw_dt.strftime("%Y/%m/%d %H:%M:%S"),
    "conn":"-",
    "serv":"-",
  }
  



def save_info(info_data):
  #tw = pytz.timezone('Asia/Taipei')
  #ts = time.time()
  #dt = datetime.fromtimestamp(ts).replace(tzinfo=pytz.utc)
  #tw_time = dt.astimezone(tw)
  #print ("tw_time = ", tw_time)


  ts = time.time()
  twdt = ts_to_dt(ts)
  print ("twdt = ", twdt)


  cli = new_cli()
  host = info_data['host']
  #info_data['timer'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
  info_data['timer'] = twdt.strftime("%Y/%m/%d %H:%M:%S"),

  rtn = cli.call("UPDATE_MACHINE_INFO", host, info_data)
  print ( 'test_info = ',rtn )
  return rtn


def add_test_data(request):
  cli = new_cli()
  test_data = {
    "host":("test %s" % int(time.time())),
    "name":"test",
    "disk":int(10.0),
    "cpu":float(10.2),
    "mem":float(55.2),
    #"timer": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    "conn":"-",
    "serv":"-",
    #"create_uts":get_now_uts(),
    #"time":uts_to_tztw(get_now_uts()).strftime('%Y-%m-%d %H:%M:%S'),
  }

  rtn = save_info(test_data)
  print ( 'test_info = ',rtn )

  return HttpResponse("success")


@csrf_exempt
def post_vps_info(request):
  print("post_vps_info")

  if request.method == "POST":

    #print ( "request.POST =", request.POST)
    post_host = str( request.POST['host'] ),
    str_host = "".join(post_host)
    post_host = str_host
    #print ( "post_host =", post_host, type(post_host))
    #print( str_host, type(str_host), len(str_host) )
    try:
      vps_name = VPS_INFO[post_host]
    except:
      vps_name = 'NONE'

    save_data = {
      "host": post_host,
      "name": vps_name,
      "disk": request.POST['disk'],
      "cpu": request.POST['cpu'],
      "mem": request.POST['mem'],
      #"timer": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
      "conn": request.POST['conn'],
      "serv": request.POST['serv'],
      #"create_uts":get_now_uts(),
      #"time":uts_to_tztw(get_now_uts()).strftime('%Y-%m-%d %H:%M:%S'),
    }
    print ( 'save_data = ',save_data )

    rtn = save_info(save_data)
    print ( 'test_info = ',rtn )
  return HttpResponse("success")



