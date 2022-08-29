from django.db import models


class System(models.Model):
  class Meta:
    db_table = 'system'
  id = models.AutoField( primary_key = True )
  ant_index = models.IntegerField()     #ant_index
  cash_index = models.IntegerField()     #cash_index
  pay_index = models.IntegerField()     #pay_index

class AntUser(models.Model):
  class Meta:
    db_table = 'ant_users'
  id = models.AutoField( primary_key = True )
  ant_id = models.CharField( max_length = 64 )
  mobile = models.CharField( max_length = 20 )      #and_account
  password = models.CharField( max_length = 64 )    #and_password
  remark = models.CharField( max_length = 40 )    
  key = models.CharField( max_length = 64 )
  create_time = models.IntegerField()



class CashOrder(models.Model):
  class Meta:
    db_table = 'cash'
  id = models.AutoField( primary_key = True )
  ant_id = models.CharField( max_length = 64 )
  whose_id = models.CharField( max_length = 64 )
  out_sn = models.CharField(max_length=128)
  sn = models.CharField(max_length=128)
  money = models.DecimalField(max_digits=10, decimal_places=2)
  bank_code = models.CharField(max_length = 4)
  bank_number = models.CharField(max_length = 15)
  bank_name = models.CharField(max_length = 5)

  status = models.SmallIntegerField()
  create_time = models.IntegerField()
  pay_time = models.IntegerField()
  pair_time = models.IntegerField()
  cancel_time = models.IntegerField()
  remark = models.CharField( max_length = 40 )    



class PayOrder(models.Model):
  class Meta:
    db_table = 'pay'
  id = models.AutoField( primary_key = True )
  ant_id = models.CharField( max_length = 64 )
  whose_id = models.CharField( max_length = 64 )

  out_sn = models.CharField(max_length=128)
  sn = models.CharField(max_length=128)
  order_key = models.CharField(max_length=64)

  money = models.DecimalField(max_digits=10, decimal_places=2)
  bank_code = models.CharField(max_length = 4)
  bank_number = models.CharField(max_length = 15)
  bank_name = models.CharField(max_length = 5)

  status = models.SmallIntegerField()

  create_time = models.IntegerField()
  pay_time = models.IntegerField()
  pair_time = models.IntegerField()
  cancel_time = models.IntegerField()

  remark = models.CharField( max_length = 40 )    




