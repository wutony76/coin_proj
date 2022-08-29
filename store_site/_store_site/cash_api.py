from __future__ import print_function
import time
import hashlib
from collections import OrderedDict
import requests
import random


def make_sign(token, key_values):
  args = []
  for k, v in key_values:
    args.append('%s=%s' % (k, v))

  a = '&'.join(args)
  print("a=", a)

  b = hashlib.md5(a).hexdigest()
  print("b=", b)
  return b.upper()


def cash_api( api_url, pid, token, money, sn, notify_url ):
  #pay_type_group = 'banktocard'

  bc_type = "bank"
  bc_name = "邮政储蓄银行"
  bc_num = "621*test*4383943"
  bc_user = "TEST测试"

  #  notify_url = "http://52.79.37.229:12009/callback"
  sign = make_sign(token, [
    ("pid", pid),
    ("money", money),
    ("sn", sn),
    ("bc_type", bc_type),
    ("bc_name", bc_name), 
    ("bc_num", bc_num), 
    ("bc_user", bc_user), 
    ("key", token),
  ])

  post_data = {
    "pid": pid,
    "money": money,
    "sn": sn,
    "bc_type":bc_type,
    "bc_name":bc_name,
    "bc_num":bc_num,
    "bc_user":bc_user,
    "notify_url": notify_url,
    "sign": sign,
  }
  
  rep = {
    "code":1,
  }

  try:
    req = requests.post(api_url, data=post_data)
    a = req.content
    print("call", req.status_code)
    print("response", a)

    if req.status_code == 200:
      print("response", a)
      rep["code"] = 0
      rep["data"] = a 

    return rep
  except:
    return rep


def cash_query_api( api_url, pid, token, money, sn ):
  pay_type_group = 'banktocard'
  notify_url = "http://3.35.119.172:12009/callback"

  sign = make_sign(token, [
    ("pid", pid),
    ("sn", sn),
    ("key", token),
  ])

  post_data = {
    "pid": pid,
    "sn": sn,
    'sign': sign,
  }

  rep = {
    "code":1,
  }

  try:
    req = requests.post(api_url, data=post_data)
    a = req.content
    print("call", req.status_code)
    print("response", a)

    if req.status_code == 200:
      print("response", a)
      rep["code"] = 0
      rep["data"] = a 

    return rep
  except:
    return rep



def main():
  pass

  ##api_url = "http://3.35.119.172:9410/pay"
  ##api_url = "http://52.79.37.229:8080/pay"
  #api_url = "http://54.199.80.255:8080/pay"

  #print("api_url", api_url)
  ##pid = 69
  ##token = "ewDimllyUOYMheMrqFCrnXqaTyCVVdN1"
  #pid = 98 
  #token = "NEYnMvtiKWdsiRlNKulPyWGQLOwbpeUd"

  #money = random.randint(200,10000)
  #sn = "sn%s" % int(time.time())
  #pay_type_group = 'banktocard'
  ##notify_url = "http://52.79.37.229:12009/callback"
  ##notify_url = "http://52.79.37.229:8300/ant/test/testcallback"
  #notify_url = "http://52.79.37.229:12009/callback"
  ##notify_url = "http://13.124.29.97:8300/ant/test/testcallback"

  #sign = make_sign(token, [
  #  ("pid", pid),
  #  ("money", money),
  #  ("sn", sn),
  #  ("pay_type_group", pay_type_group),
  #  ("notify_url", notify_url), 
  #  ("key", token),
  #])

  #post_data = {
  #  "pid": pid,
  #  "money": money,
  #  "sn": sn,
  #  "notify_url": notify_url,
  #  "pay_type_group": pay_type_group,
  #  "remark": 'remark',
  #  'sign': sign,
  #}

  #req = requests.post(api_url, data=post_data)
  #a = req.content
  #print("call", req.status_code)
  #print("response", a)

  #if req.status_code == 200:
  #  print("response", a)


if __name__ == "__main__":
  main()

