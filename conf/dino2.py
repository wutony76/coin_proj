from __future__ import print_function
import os 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.dirname(BASE_DIR))
DATA_DIR = os.path.join(ROOT_DIR, "data")

PAYS_ZODB_DATA_DIR = os.path.join(DATA_DIR, "zodb")
DIPAYIX_IX_ADDR = ('0.0.0.0', 9416)
DIPAYIX_IX_SYNC_ADDR = ('0.0.0.0', 9418)

####
#DIPAYIX_HTTP = 'http://127.0.0.1:9416'
#DIPAY_API_DOMAIN = 'http://52.79.37.229:8080'
#DIPAY_LOGIC_ADDR = ('127.0.0.1', 9421)
#DIPAY_BROKER_ADDR = ('127.0.0.1', 9427)
#DIPAY_LOGSTORAGE_ADDR = ('127.0.0.1', 9431)

DIPAY_SERVICE_ADDR = '/var/pays/service_v2.sock'
DIPAY_LOGIC_ADDR_OLD = ('127.0.0.1', 9421)
DIPAY_LOGSTORAGE2_ADDR = ('127.0.0.1', 9442)
DIPAY_LOGSTORAGE3_ADDR = ('127.0.0.1', 9443)

DIPAYIX_MYSQL_DATABASE = {
  'HOST': "17.0.0.153",
  'NAME': "DB2",
  'USER': "root",
  'PASSWORD': "",
}

##############################

#DIPAY_PAY_APP_DOMAIN = 'http://52.79.37.229:8080'


PAYS_SERVICE_ADDR = '/var/pays/service_v2.sock'
DIPAY_API_DOMAIN = 'http://52.79.37.229:8080'
DIPAYIX_HTTP = 'http://127.0.0.1:9416'
DIPAYIX_SESSION_URL = 'http://127.0.0.1:9417'
DIPAY_LOGIC_ADDR = ('127.0.0.1', 9422)
DIPAY_BROKER1_ADDR = ('127.0.0.1', 9431)
DIPAY_BROKER2_ADDR = ('127.0.0.1', 9432)
DIPAY_LOGSTORAGE1_ADDR = ('127.0.0.1', 9441)
DIPAY_LOGINDEX_ADDR = ('127.0.0.1', 9451)
PHP_FCGI_ADDR = '/var/run/php-fpm/php-fpm.sock'
PHP_DIPAY_API_PROJ_ROOT = os.path.abspath('/mixcat/yainpay2/api')
PHP_DIPAY_ANT_PROJ_ROOT = os.path.abspath('/mixcat/yainpay2/ant')
PHP_DIPAY_ADMIN_PROJ_ROOT = os.path.abspath('/mixcat/yainpay2/admin')



#######################################################################

PAY_DB_DATA_DIR = '/var/pays'

SWORD_MYSQL_DATABASE = {
  'HOST': "127.0.0.1",
  'NAME': "coin_dev2",
  'USER': "root",
  'PASSWORD': "",
  'PORT': 3306,
}
PAY_MYSQL_DATABASE = SWORD_MYSQL_DATABASE
COIN_MYSQL_DATABASE = SWORD_MYSQL_DATABASE


SMS_VERIFY_DB_ADDR = ('127.0.0.1', 40002)
G_OTP_DB_DIR = '/var/opt_db'
G_OTP_DB_ADDR = SMS_VERIFY_DB_ADDR
G_OTP_BIND_PREFIX = 'http://3.35.172.98:8092/bind'
G_OTP_EMAIL_PREFIX = '3.35.172.98:8092/verify_email'

FIRECAT_SESSION_HTTP = "http://21.0.1.18:8361"



