from __future__ import print_function
import json
import time
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from dipay.models import Aisle, AdminUser, AntUser, OrderInfo, AdminChannel, LogEntry, TaskInfo, TdGroup, SysConfig, BankCard
from fdpays import time_utils
#import ts_to_tz_shanghai, TZ_SHANGHAI, tz_shanghai_to_ts


def calc_robtask_view(request):
  task_gold = round(float(request.GET['task_gold']), 2)
  pay_type = int(request.GET['pay_type'])
  admin_id = int(request.GET['admin_id'])


  admin_user = AdminUser.objects.get(id=admin_id)

  sysconfig = SysConfig.objects.get(varname='site_config')
  site_config = json.loads(sysconfig.value)

  data_src = RobModelDataSource()
  
  server = None
  robtask = RobTask(server)
  t0 = time.time()
  calc_result = robtask.calc(data_src, site_config,  pay_type, task_gold, admin_user)
  dt = time.time() - t0
  print('dt', dt)


  return JsonResponse({
    'calc_result': calc_result.make_context(),
  })




class RobModelDataSource(object):

  def __init__(self):
    self.ant_user_by_id = {}

    self._day_bank_card_total_money_tree = None

  def __repr__(self):
    return '<RobModelDataSource>'

  def get_ant_user(self, ant_user_id):
    if self.ant_user_by_id.has_key(ant_user_id) == False:
      try:
        ant_user = AntUser.objects.get(id=ant_user_id)
        #print(self, 'get_ant_user=%s' % ant_user_id, ant_user)
      except AntUser.DoesNotExist:
        ant_user = None
      self.ant_user_by_id[ant_user_id] = ant_user
    ant_user = self.ant_user_by_id[ant_user_id]
    return ant_user

  def get_day_bank_card_total_money_tree(self, year, month, day):
    if self._day_bank_card_total_money_tree is None:
      tree = {}

      start_dt = datetime(year, month, day, 0, 0, 0, tzinfo=TZ_SHANGHAI)
      print('start_dt', start_dt)
      start_ts = tz_shanghai_to_ts(start_dt)
      start_ts2 = start_ts - (60*60*24)

      qs = TaskInfo.objects.filter(rob_time__gte=start_ts2)
      limit = 1024
      offset = 0
      for i in xrange(128):
        objs = list(qs[offset:(offset+limit)])
        print('offset=%s limit=%s count=%s' % (offset, limit, len(objs)))
        for o in objs:
          assert o.rob_time >= start_ts2
          if o.rob_time >= start_ts:
            if o.status in [2]:
              tree[o.bc_id] = tree.get(o.bc_id, 0) + round(o.gold, 2)
          

        if len(objs) < limit:
          break

        offset += limit

      print('tree', tree)
      self._day_bank_card_total_money_tree = tree

    return self._day_bank_card_total_money_tree

  def get_day_bank_card_total_money(self, bc_id, year, month, day):
    tree = self.get_day_bank_card_total_money_tree(year, month, day)
    return tree.get(bc_id, 0)

class RobTask(object):
  def __init__(self, server):
    self.server = server
  

  def __repr__(self):
    return '<RobTask>'


  def calc(self, data_src, site_config,  pay_type, task_gold, admin_user):

    ts = time.time()
    now = ts_to_tz_shanghai(ts)


    bind_user_ids = None
    if admin_user.bind_user:
      bind_user_ids = []
      _arr = admin_user.bind_user.split(',')
      print('bind_user', _arr)
      for a in _arr:
        try:
          b = int(a)
          bind_user_ids.append(b)
        except:
          pass

    #print('%s bind_user_ids %s' % (self, bind_user_ids))

    auto_rob_money = round(float(site_config['auto_rob_money']), 2)
    task_pay_type = pay_type

    bank_cards = list(BankCard.objects.all())
    result = CalcResult({
      'admin': {
        'id': admin_user.id,
        'status': admin_user.status,
        'money': round(admin_user.money, 2),
        'lock_money': round(admin_user.lock_money, 2),
      },
      'task_gold': task_gold,
      'pay_type': pay_type,
      'auto_rob_money': auto_rob_money,
    })
    result.bind_user_ids = bind_user_ids


    for bank_card in bank_cards:
      
      errors = []
      if bank_card.bc_status != 1:
        errors.append(u'禁用')

      if bank_card.aisle_id != task_pay_type:
        errors.append(u'支付方式不一致')
        #print('aisle_id=%s task_pay_type=%s' % (repr([bank_card.aisle_id]), repr([task_pay_type])))

      if bind_user_ids is not None:
        if bank_card.m_id not in bind_user_ids:
          errors.append(u'非白名單')


      day_money_limit = round(float(bank_card.day_money_limit), 2)

      if day_money_limit > 0:
        today_bank_card_total_money = data_src.get_day_bank_card_total_money(bank_card.bc_id, now.year, now.month, now.day)
        #print("bank_card=%s today_bank_card_total_money=%s" % (bank_card.bc_id, today_bank_card_total_money))
        total_money2 = today_bank_card_total_money + task_gold
        if total_money2 > day_money_limit:
          err = '日限额%s 不足, 已接单金额%s, 该单金额%s' % (day_money_limit, total_money2, task_gold)
          errors.append(err)

      if task_pay_type == 8:
        if bank_card.online != 0:
          pass

      ant_user = data_src.get_ant_user(bank_card.m_id)
      parent_ant_user = None
      if ant_user is None:
        errors.append(u'碼商不存在')
      else:
        ant_user_money = round(ant_user.m_money, 2)
        if ant_user.user_status != 1:
          errors.append(u'碼商禁用')

        if ant_user.is_auto != 1:
          errors.append(u'碼商停用自動搶單')

        if ant_user_money < auto_rob_money:
          errors.append(u'碼商餘額<最低自動搶單金額')
            

        if ant_user.pid and ant_user.is_bind:
          _parent_user = data_src.get_ant_user(ant_user.pid)
          if _parent_user is None:
            err = u'关联用户%s不存在' % ant_user.pid
            errors.append(err)
          else:
            parent_ant_user = _parent_user
            if _parent_user.m_money < task_gold:
              err = u'关联扣款，抢单用户%s, 上级%s余额(%s)不足' % (ant_user.id,  _parent_user.id, _parent_user.m_money)
              errors.append(err)

      if ant_user is not None:
        if parent_ant_user is None:
          if ant_user.m_money < task_gold:
            err = u'%s余额(%s)不足' % (ant_user.id, ant_user.m_money)
            errors.append(err)
          

      result.error_tree[bank_card.bc_id] = {
        'errors': errors,
        'm_id': bank_card.m_id,
        #'day_money_limit': day_money_limit,
      }

      if not errors:
        result.active_bc_ids.append(bank_card.bc_id)
        result.answers.append((bank_card, ant_user, parent_ant_user))

    return result



class CalcResult(object):

  def __init__(self, params):
    self.params = params
    self.active_bc_ids = []
    self.error_tree = {}
    self.answers = []
    self.bind_user_ids = None


  def make_context(self):
    return {
      'params': self.params,
      'active_bc_ids': self.active_bc_ids,
      'errors': self.error_tree,
      'bind_user_ids': self.bind_user_ids,

    }
