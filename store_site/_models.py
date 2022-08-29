from __future__ import print_function
from decimal import Decimal
from django.db import models
from django_bulk_update.manager import BulkUpdateManager


class ObjType:
  
  ADMIN_USER = 1
  ANT_USER = 2

  ORDER_INFO = 11
  TASK_INFO = 12
  LOWER_INFO = 13

  
  OP_ADMIN_RECH = 201
  OP_ADMIN_KOU = 202
  OP_ANT_RECH = 203
  OP_ANT_KOU = 204


  #配單
  OP_ORDER_ROBTASK = 231
  OP_ORDER_CONFIRM = 232

  #後台確認
  OP_ORDER_SURE = 233
  #後台取消
  OP_ORDER_CANCEL = 234
  #手動補單
  OP_ORDER_CANCEL_SURE = 235
  #排程自動取消任務
  OP_ORDER_CANCEL_AUTO = 231

  OP_LOWER_ADD = 261
  OP_LOWER_CONFIRM = 262
  OP_LOWER_FORCE_CANCEL = 263


class LogEntryType:
  ORDER_COMMISION_CREDIT = 2
  DELETE_ORDER = 11


class AdminUser(models.Model):

  class Meta:
    db_table = 'lq_admin'


  id = models.IntegerField(primary_key=True)
  oid = models.PositiveIntegerField()
  pid = models.IntegerField()
  agent_id = models.IntegerField()
  user_id = models.IntegerField()
  username = models.CharField(max_length=20)
  nickname = models.CharField(max_length=50)
  password = models.CharField(max_length=64)
  salt = models.CharField(max_length=30)
  mobile = models.CharField(max_length=20)
  status = models.IntegerField()
  white_ip = models.CharField(max_length=500)

  email = models.CharField(max_length=50)
  secret = models.CharField(max_length=32)
  token = models.CharField(max_length=20)
  login_time = models.IntegerField()
  login_ip = models.CharField(max_length=16)
  update_time = models.IntegerField()
  create_time = models.IntegerField()
  delete_time = models.IntegerField()

  alipay_rate = models.DecimalField(max_digits=5, decimal_places=2)
  bank_rate = models.DecimalField(max_digits=5, decimal_places=2)
  wechat_rate = models.DecimalField(max_digits=5, decimal_places=2)
  alicode_rate = models.DecimalField(max_digits=5, decimal_places=2)
  wemobile_rate = models.DecimalField(max_digits=5, decimal_places=2)
  lowerhairs_rate = models.DecimalField(max_digits=5, decimal_places=2)
  lowerhairs_fee = models.IntegerField()

  money = models.DecimalField(max_digits=11, decimal_places=2)
  lock_money = models.DecimalField(max_digits=11, decimal_places=2)
  bind_user = models.CharField(max_length=500)
  order_mode = models.IntegerField()
  order_name = models.IntegerField()
  
  def calc_white_ip(self):
    ips = None
    if self.white_ip:
      ips = []
      for a in self.white_ip.split(','):
        a = a.strip() 
        if a:
          ips.append(a)

    return ips


class AntUser(models.Model):

  class Meta:
    db_table = 'lq_users'


  id = models.IntegerField(primary_key=True)
  oid = models.PositiveIntegerField()
  pid = models.IntegerField()
  gid = models.IntegerField()
  mobile = models.CharField(max_length=20)
  user_pass = models.CharField(max_length=64)
  m_salt = models.CharField(max_length=6)
  user_status = models.IntegerField()
  user_type = models.IntegerField()
  m_money = models.DecimalField(max_digits=11, decimal_places=2)
  lock_money = models.DecimalField(max_digits=11, decimal_places=2)
  version = models.IntegerField()
  rate = models.DecimalField(max_digits=5, decimal_places=2)
  daifu_rate = models.DecimalField(max_digits=5, decimal_places=2)
  create_time = models.IntegerField()
  is_bind = models.PositiveSmallIntegerField()
  is_auto = models.PositiveSmallIntegerField()

  signature = models.CharField(max_length=256)
  version = models.IntegerField()

  def make_context(self):
    data = dict(self.__dict__)
    data.pop('_state')
    for k in data.keys():
      v = data[k]
      #print('make_context', k, v, type(v))
      if isinstance(v, Decimal):
        data[k] = float(v)

    return data

class OrderInfo(models.Model):
  class Meta:
    db_table = 'lq_orders'


  id = models.AutoField(primary_key=True)
  oid = models.PositiveIntegerField()
  agent_admin_id = models.IntegerField()
  admin_id = models.IntegerField()
  users_id = models.IntegerField()
  sn = models.CharField(max_length=128)
  out_sn = models.CharField(max_length=256)
  money = models.DecimalField(max_digits=10, decimal_places=2)
  pay_name = models.DecimalField(max_digits=10, decimal_places=2)
  rate = models.DecimalField(max_digits=5, decimal_places=2)
  brokerage = models.DecimalField(max_digits=10, decimal_places=2)
  agent_brokerage = models.DecimalField(max_digits=10, decimal_places=2)
  real_money = models.DecimalField(max_digits=10, decimal_places=2)
  ip = models.CharField(max_length=255)
  user_ip = models.CharField(max_length=20)
  notify_url = models.CharField(max_length=512)
  pay_type = models.CharField(max_length=64)
  url_key = models.CharField(max_length=128)
  status = models.SmallIntegerField()
  is_callback = models.SmallIntegerField()
  p_remark = models.CharField(max_length=256)
  sign = models.CharField(max_length=256)
  operator = models.PositiveIntegerField(default=0)
  pay_time = models.PositiveIntegerField(default=0)
  rob_time = models.PositiveIntegerField(default=0)
  create_time = models.PositiveIntegerField()
  update_time = models.PositiveIntegerField()
  tdgroup_biaoshi = models.CharField(max_length=50)
  remark = models.CharField(max_length=100)

  def make_context(self):
    data = dict(self.__dict__)
    data.pop('_state')
    for k in data.keys():
      v = data[k]
      #print('make_context', k, v, type(v))
      if isinstance(v, Decimal):
        data[k] = float(v)

    return data

class TaskInfo(models.Model):
  class Meta:
    db_table = 'lq_task'


  id = models.AutoField(primary_key=True)
  oid = models.PositiveIntegerField()
  admin_id = models.PositiveIntegerField()
  bc_id = models.PositiveIntegerField()
  pid = models.PositiveIntegerField()
  users_id = models.PositiveIntegerField()
  orders_id = models.PositiveIntegerField()
  gold = models.DecimalField(max_digits=10, decimal_places=2)
  fudong_gold = models.DecimalField(max_digits=10, decimal_places=2)
  real_money = models.DecimalField(max_digits=10, decimal_places=2)
  bond = models.DecimalField(max_digits=10, decimal_places=2)
  pay_type = models.CharField(max_length=16)
  status = models.PositiveSmallIntegerField()
  bc_name = models.CharField(max_length=128)
  bc_num = models.CharField(max_length=128)
  bc_branch = models.CharField(max_length=500)
  bc_user = models.CharField(max_length=128)
  short_num = models.CharField(max_length=8)
  pay_name = models.CharField(max_length=128)

  confirm_user = models.PositiveIntegerField()
  confirm_time = models.PositiveIntegerField()

  rob_time = models.PositiveIntegerField()
  create_time = models.PositiveIntegerField()
  update_time = models.PositiveIntegerField()
  is_auto = models.PositiveSmallIntegerField()
  is_lock = models.PositiveSmallIntegerField()
  payurl = models.CharField(max_length=500)

  def make_context(self):
    data = dict(self.__dict__)
    data.pop('_state')
    for k in data.keys():
      v = data[k]
      #print('make_context', k, v, type(v))
      if isinstance(v, Decimal):
        data[k] = float(v)

    return data


 
class Account(models.Model):
  class Meta:
    db_table = 'lq_account'

  ac_id = models.AutoField(primary_key=True)
  ac_code = models.CharField(max_length=30)
  agent_admin_id = models.PositiveIntegerField(default=0)
  m_id = models.IntegerField()
  ac_money = models.DecimalField(max_digits=12, decimal_places=2)
  ac_user_money = models.DecimalField(max_digits=12, decimal_places=2)
  ac_flow = models.SmallIntegerField()
  ac_type = models.SmallIntegerField()
  children_level = models.PositiveSmallIntegerField()
  children_id = models.PositiveIntegerField()
  children_nickname = models.CharField(max_length=255)
  isdel = models.SmallIntegerField()
  p_id = models.IntegerField()
  t_id = models.IntegerField()
  t_type = models.PositiveSmallIntegerField()
  ip = models.CharField(max_length=16)
  site_id = models.IntegerField(default=1)
  remark = models.CharField(max_length=255)
  add_time = models.IntegerField()

  def make_context(self):
    data = dict(self.__dict__)
    data.pop('_state')
    for k in data.keys():
      v = data[k]
      #print('make_context', k, v, type(v))
      if isinstance(v, Decimal):
        data[k] = float(v)

    return data

#變帳明細v2
class AccountSet(models.Model):
  class Meta:
    db_table = 'lq_account_set'

  oid = models.PositiveIntegerField(primary_key=True)
  target_oid = models.PositiveIntegerField()
  target_type = models.IntegerField()
  target_op = models.IntegerField()
  state = models.IntegerField()
  data = models.CharField(max_length=4096)
  note = models.CharField(max_length=128)
  time = models.PositiveIntegerField()

class AccountItem(models.Model):

  class Meta:
    db_table = 'lq_account_item'

  oid = models.PositiveIntegerField(primary_key=True)
  p_oid = models.PositiveIntegerField()
  ac_id = models.PositiveIntegerField()
  ac_flow = models.SmallIntegerField()
  ac_type = models.SmallIntegerField()
  ac_code = models.CharField(max_length=32)
  t_oid = models.IntegerField()
  t_id = models.IntegerField()
  t_type = models.IntegerField()
  m_id = models.IntegerField()
  m_type = models.IntegerField()
  incr_credit = models.DecimalField(max_digits=11, decimal_places=2)
  remaining_credit = models.DecimalField(max_digits=11, decimal_places=2)
  q_admin_id = models.IntegerField()
  q_ant_id = models.IntegerField()
  remark = models.CharField(max_length=256)
  ip = models.CharField(max_length=24)
  time = models.PositiveIntegerField()

  def make_context(self):
    data = dict(self.__dict__)
    data.pop('_state')
    for k in data.keys():
      v = data[k]
      #print('make_context', k, v, type(v))
      if isinstance(v, Decimal):
        data[k] = float(v)

    return data



class TdGroup(models.Model):
  class Meta:
    db_table = 'lq_tdgroup'

  id = models.PositiveIntegerField(primary_key=True)
  name = models.CharField(max_length=50)
  biaoshi = models.CharField(max_length=20)
  tdids = models.CharField(max_length=200)
  fudong_type = models.PositiveSmallIntegerField()
  fudong_money = models.DecimalField(max_digits=10, decimal_places=2)
  teli_money = models.CharField(max_length=200)


class Aisle(models.Model):
  class Meta:
    db_table = 'lq_aisle'

  id = models.PositiveIntegerField(primary_key=True)
  name = models.CharField(max_length=18)
  min_money = models.DecimalField(max_digits=10, decimal_places=2)
  max_money = models.DecimalField(max_digits=10, decimal_places=2)
  status = models.PositiveSmallIntegerField()
  is_image = models.PositiveSmallIntegerField()
  remark = models.TextField()


class AdminChannel(models.Model):
  class Meta:
    db_table = 'lq_admin_channel'

  id = models.PositiveIntegerField(primary_key=True)
  admin_id = models.PositiveIntegerField()
  aisle_id = models.PositiveIntegerField()
  rate = models.DecimalField(max_digits=10, decimal_places=2)
  status = models.PositiveSmallIntegerField()
  create_time = models.PositiveIntegerField()
  update_time = models.PositiveIntegerField()


class LogEntry(models.Model):
  class Meta:
    db_table = 'lq_logentry'

  id = models.AutoField(primary_key=True)
  data = models.TextField()
  time = models.PositiveIntegerField()


class SysConfig(models.Model):
  class Meta:
    db_table = 'lq_sysconfig'

  id = models.AutoField(primary_key=True)
  varname = models.CharField(max_length=20)
  info = models.CharField(max_length=100)
  value = models.TextField()
  o_type_id = models.IntegerField()
  site_id = models.IntegerField()

class BankCard(models.Model):
  class Meta:
    db_table = 'lq_bank_card'

  bc_id = models.AutoField(primary_key=True)
  pid = models.PositiveIntegerField()
  m_id = models.IntegerField()
  aisle_id = models.PositiveIntegerField()
  channel_name = models.CharField(max_length=30)
  bc_type = models.PositiveSmallIntegerField()
  bc_name = models.CharField(max_length=50)
  bc_num = models.CharField(max_length=128)
  bc_branch = models.CharField(max_length=500)
  short_num = models.CharField(max_length=8)
  bc_user = models.CharField(max_length=20)
  bc_status = models.PositiveSmallIntegerField()
  image = models.CharField(max_length=256)
  add_time = models.IntegerField()
  delete_time = models.IntegerField()
  site_id = models.PositiveIntegerField()
  fail_num = models.PositiveSmallIntegerField()
  platform_account = models.CharField(max_length=50)
  platform_cookie = models.CharField(max_length=5000)
  online = models.PositiveSmallIntegerField()
  money = models.DecimalField(max_digits=15, decimal_places=2)
  expire_time = models.PositiveIntegerField()
  day_money_limit = models.DecimalField(max_digits=10, decimal_places=2)
  remark = models.CharField(max_length=100)


class LowerhairInfo(models.Model):
  class Meta:
    db_table = 'lq_lowerhairs'

  id = models.AutoField(primary_key=True)
  oid = models.PositiveIntegerField()
  agent_admin_id = models.PositiveIntegerField()
  admin_id = models.PositiveIntegerField()
  type = models.CharField(max_length=128)
  users_id = models.PositiveIntegerField()
  money = models.DecimalField(max_digits=10, decimal_places=2)
  rate = models.DecimalField(max_digits=6, decimal_places=2)
  brokerage = models.DecimalField(max_digits=10, decimal_places=2)
  user_brokerage = models.DecimalField(max_digits=10, decimal_places=2)
  real_money = models.DecimalField(max_digits=10, decimal_places=2)
  gold = models.DecimalField(max_digits=10, decimal_places=2)
  bank_name = models.CharField(max_length=32)
  bank_num = models.CharField(max_length=32)
  bank_user = models.CharField(max_length=32)
  status = models.PositiveSmallIntegerField()
  image = models.CharField(max_length=512)
  p_remark = models.CharField(max_length=256)
  create_time = models.PositiveIntegerField()
  update_time = models.PositiveIntegerField()
  notify_url = models.CharField(max_length=512)
  pay_time = models.PositiveIntegerField()
  sn = models.CharField(max_length=256)
  is_callback = models.PositiveSmallIntegerField()
  agent_money = models.DecimalField(max_digits=15, decimal_places=2)
  is_lock = models.PositiveSmallIntegerField(default=0)


############################
class DataPage(models.Model):
  class Meta:
    db_table = 'lq_datapage' 

  objects = BulkUpdateManager()

  page_key = models.CharField(max_length=64, primary_key=True)
  page_data = models.BinaryField()
