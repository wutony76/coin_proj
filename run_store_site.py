from __future__ import print_function
import os
import io
import imp
#import StringIO
import sys
import random
import threading
import time
from optparse import OptionParser


def setup():
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  ROOT_DIR = BASE_DIR

  #sys.path.insert(0, os.path.join(ROOT_DIR, "store_site"))
  #sys.path.insert(0, os.path.join(ROOT_DIR, "store_site"))
  sys.path.insert(0, os.path.join(ROOT_DIR, "packages"))
  sys.path.insert(0, ROOT_DIR)

  os.environ.setdefault("FC_ROOT", ROOT_DIR)
  os.environ.setdefault("FC_CONF", "local")

  #os.environ["DJANGO_SETTINGS_MODULE"] = "store_site.settings"
  os.environ["DJANGO_SETTINGS_MODULE"] = "store_site.settings"

  import django
  django.setup()


def heartbeat_loop():
  print("heartbeat", time.time())

def main(port):
  from django.core.handlers.wsgi import WSGIHandler
  from twisted.web import server
  from twisted.web.wsgi import WSGIResource
  from twisted.python.threadpool import ThreadPool
  from twisted.application import service, strports
  from twisted.internet import reactor, ssl
  from twisted.internet.task import LoopingCall
  from twisted.python.modules import getModule
  from fcworks.conf import settings as _settings
  #from fatcat.conf import settings as _settings

  opt_parser = OptionParser()
  opt_parser.add_option("-p", "--port", dest="port")

  opts, args = opt_parser.parse_args()

  if opts.port is not None:
    port = int(opts.port)

  reactor.suggestThreadPoolSize(4096)

  application = WSGIHandler()

  wsgi_resource = WSGIResource(reactor, reactor.getThreadPool(), application)

  site = server.Site(wsgi_resource)
  reactor.listenTCP(port, site)
  #reactor.listenTCP(80, site)

  print("start coin site at :%s" % port)
  loop = LoopingCall(heartbeat_loop)
  loop.start(10)

  try:
    reactor.run()

  except KeyboardInterrupt:
    reactor.stop()
  
if __name__ == '__main__':
  imp.reload(sys)
  #sys.setdefaultencoding("utf-8")

  setup()
  #main(8085)
  main(9321)
