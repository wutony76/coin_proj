
import hashlib 
import uuid

from store_site.models import System
from datetime import datetime
from datetime import timedelta

from store_site.models import AntUser



data_cache = { "ant":[] }


def hashlib_password( _key, _password ):
  #_data = AntUser.objects.get( id = _id ) 
  #_key = _data.key
  s_key = "%s%s" % (_password, _key)

  sha = hashlib.sha256()
  sha.update(s_key.encode("utf-8"))
  return sha.hexdigest()


def get_order_key():
  return str(uuid.uuid4().hex)
  
  





# pay_index
def get_pay_index():
  _sys = System.objects.get( id = 0 )
  _n = _sys.pay_index + 1
  return _n
  
def save_pay_index( _n ):
  system = System.objects.get( id = 0 )
  system.pay_index = _n
  system.save()



# cash_index
def get_cash_index():
  _sys = System.objects.get( id = 0 )
  _n = _sys.cash_index + 1
  return _n
  
def save_cash_index( _n ):
  system = System.objects.get( id = 0 )
  system.cash_index = _n
  system.save()


# ant_index 
def get_ant_index():
  _sys = System.objects.get( id = 0 )
  _n = _sys.ant_index + 1
  return _n
  
def save_ant_index( _n ):
  system = System.objects.get( id = 0 )
  system.ant_index = _n
  system.save()





def uts_to_date(ts):
  #print("uts_to_datets ---------")
  utc_time = datetime.utcfromtimestamp(ts)
  time2 = utc_time + timedelta(hours=8)
  return time2.strftime("%Y-%m-%d %H:%M:%S")



### start cache
def cache_ant_list():
  _lsit = list( AntUser.objects.values() )
  n_list = []

  for obj in _lsit:
    n_list.append( obj.get("ant_id") )
  
  data_cache ["ant"] = n_list
  return n_list
  
  
  
