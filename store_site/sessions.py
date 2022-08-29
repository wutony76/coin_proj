import time
import random
import uuid
from zodbpickle import fastpickle as pickle
from django.conf import settings
from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.exceptions import SessionInterrupted
from django.contrib.sessions.backends.base import SessionBase
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import http_date

from fcworks.conf import settings as _settings
from ashera.threads.client import base_http_rpc_call

def rpc_call(cmd, *cmd_args):
  
  url = "%s/call" % _settings.TRXW_SESSION_HTTP.strip('/')

  rtn = base_http_rpc_call(url, cmd, *cmd_args)
  return rtn


def random_session_key():
  ts = int(time.time())
  node_id = uuid.getnode()
  #print("node_id", node_id)
  a = "%010x%014x%08x" % (ts, node_id, random.randint(0x10000000, 0xffffffff))
  #print("a", a)
  return a

class SessionStore(SessionBase):

  def __init__(self, session_key=None):
    #self._session_cache = None
    super().__init__(session_key)

  def _get_new_session_key(self):
    session_key = random_session_key()
    return session_key

  @property
  def cache_key(self):
    session_key = self._get_or_create_session_key()
    return "%s-%s" % (settings.SESSION_PREFIX, session_key)

  def load(self):
    print("=" * 100)
    print(self, "load", self.cache_key)
    session_data = rpc_call("SESSION_GET", self.cache_key)[0]
    if session_data is not None:
      session_data = pickle.loads(session_data)
      #print("get_session_data", self.cache_key, session_data)
      return session_data

    self._session_key = None
    return {}

  def save(self, must_create=False):
    data = self._get_session(no_load=must_create)

    expiry_age = 60 * 60 * 6
    if hasattr(self, "expiry_age"):
      expiry_age = self.expiry_age
    data_encoded = pickle.dumps(data)
    rtn = rpc_call("SESSION_SET", self.cache_key, data_encoded, expiry_age + 60 * 60)[0]
    print("SESSION_SET cache_key", self.cache_key)


