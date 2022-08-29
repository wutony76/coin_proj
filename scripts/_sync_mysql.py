from django.db import connection
from fcworks.conf import settings as _settings


def main(*args):
  with connection.cursor() as cursor:
    db_ctx = _settings.ACRM_MYSQL_DATABASE
      
    db_name = db_ctx["NAME"]

    sqls = [
      "ALTER DATABASE %s CHARACTER SET utf8;" % db_name,
    ]

    sql = """CREATE TABLE IF NOT EXISTS acrm_post_mail(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      partner_id INT NOT NULL,
      user_id BIGINT NOT NULL,
      mail_to VARCHAR(128) NOT NULL,
      subject VARCHAR(128) NOT NULL,
      body LONGTEXT NOT NULL,
      reason VARCHAR(256) NOT NULL
    )"""

    sqls.append(sql)




    sql = """CREATE TABLE IF NOT EXISTS acrm_finlog(
      id BIGINT NOT NULL PRIMARY KEY,
      type_id INT NOT NULL,
      pn INT NOT NULL,
      time BIGINT NOT NULL,
      partner_id INT NOT NULL,
      agent_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      item_id BIGINT NOT NULL,
      t_type_id INT NOT NULL,
      t_obj_id BIGINT NOT NULL,
      amount DECIMAL(20, 6) NOT NULL,
      balance DECIMAL(20, 6) NOT NULL,
      remark VARCHAR(64)
    )"""

    sqls.append(sql)

    ####

    sql = """CREATE TABLE IF NOT EXISTS acrm_user(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      partner_id INT NOT NULL,
      parent_id BIGINT NOT NULL,
      agent_id BIGINT NOT NULL,
      create_time BIGINT NOT NULL,
      last_login BIGINT NOT NULL,
      username VARCHAR(64) NOT NULL,
      email VARCHAR(64) NOT NULL,
      password VARCHAR(128) NOT NULL,
      security_password VARCHAR(128) NOT NULL,
      secret_key VARCHAR(32) NOT NULL,
      UNIQUE(partner_id, username)
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_user_profile(
      user_id BIGINT NOT NULL PRIMARY KEY,
      is_truename TINYINT NOT NULL,
      invit_code VARCHAR(32) NOT NULL,
      first_name VARCHAR(32) NOT NULL,
      last_name VARCHAR(32) NOT NULL,
      country_region VARCHAR(64) NOT NULL,
      street_address_1 VARCHAR(128) NOT NULL,
      street_address_2 VARCHAR(128) NOT NULL,
      town_city VARCHAR(32) NOT NULL,
      state_county VARCHAR(32) NOT NULL,
      postcode_zip VARCHAR(32) NOT NULL,
      phone VARCHAR(32) NOT NULL,
      data LONGTEXT NOT NULL,
      UNIQUE(invit_code)
    )"""


    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_user_index(
      user_id BIGINT NOT NULL PRIMARY KEY,
      state INT,
      partner_id INT,
      parent_id BIGINT,
      agent_id BIGINT,
      create_time BIGINT NOT NULL,
      is_truename TINYINT NOT NULL,
      is_trader TINYINT NOT NULL,

      trader_level INT NOT NULL,
      intern_state INT NOT NULL,
      intern_login_id BIGINT NOT NULL,
      intern_start_time BIGINT NOT NULL,
      intern_end_time BIGINT NOT NULL,

      credit_31 DECIMAL(20, 6) NOT NULL DEFAULT 0, 

      email VARCHAR(64) NOT NULL,
      invit_code VARCHAR(32) NOT NULL
    )"""

    sqls.append(sql)

    #####
    sql = """CREATE TABLE IF NOT EXISTS acrm_agent_user(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      state2 INT NOT NULL,
      partner_id INT NOT NULL,
      create_time BIGINT NOT NULL,
      action_time BIGINT NOT NULL,
      invit_code VARCHAR(32) NOT NULL,
      username VARCHAR(64) NOT NULL,
      nickname VARCHAR(32) NOT NULL,
      secret_key VARCHAR(32) NOT NULL,
      password VARCHAR(128) NOT NULL,
      security_password VARCHAR(128) NOT NULL,
      email VARCHAR(64) NOT NULL,
      token VARCHAR(32) NULL,
      UNIQUE(username),
      UNIQUE(invit_code)
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_admin_user(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      username VARCHAR(64) NOT NULL,
      password VARCHAR(128) NOT NULL,
      secret_key VARCHAR(128) NOT NULL
    )"""

    sqls.append(sql)


    ####

    sql = """CREATE TABLE IF NOT EXISTS acrm_user_logs(
      id BIGINT NOT NULL PRIMARY KEY,
      type_id INT NOT NULL,
      partner_id INT NOT NULL,
      user_id BIGINT NOT NULL,
      time BIGINT NOT NULL,
      t_type_id INT NOT NULL,
      t_obj_id BIGINT NOT NULL,
      message VARCHAR(256) NOT NULL
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_email_register(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      partner_id INT NOT NULL,
      email VARCHAR(64) NOT NULL,
      secret_key VARCHAR(32) NOT NULL,
      password VARCHAR(128) NOT NULL,
      token VARCHAR(128) NOT NULL,
      UNIQUE(token)
    )"""

    sqls.append(sql)

    ###################

    sql = """CREATE TABLE IF NOT EXISTS acrm_trc20_txlog(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT,
      time BIGINT NOT NULL,
      txid VARCHAR(96) NOT NULL,
      symbol VARCHAR(16),
      amount DECIMAL(20, 6) NOT NULL DEFAULT 0, 
      address_from VARCHAR(96) NOT NULL,
      address_to VARCHAR(96) NOT NULL,
      remark VARCHAR(128) NOT NULL,
      UNIQUE(txid)
    )"""

    sqls.append(sql)


    sql = """CREATE TABLE IF NOT EXISTS acrm_recharge_trxaddr(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      active_time BIGINT NOT NULL,
      address VARCHAR(96) NOT NULL,
      bind_id BIGINT,
      bind_key VARCHAR(64),
      priv_key VARCHAR(128) NOT NULL,
      pub_key VARCHAR(128) NOT NULL,
      UNIQUE(address),
      UNIQUE(bind_key)
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_recharge_trxaddr_bind(
      id BIGINT NOT NULL PRIMARY KEY,
      time BIGINT NOT NULL,
      addr_id BIGINT NOT NULL,
      bind_key VARCHAR(64) NOT NULL
    )"""
    #data LONGTEXT NOT NULL

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_recharge_trxaddr_log(
      id BIGINT NOT NULL PRIMARY KEY,
      time BIGINT NOT NULL,
      address VARCHAR(96) NOT NULL,
      bind_key VARCHAR(64)
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_recharge_trc20(
      id BIGINT NOT NULL PRIMARY KEY,
      time BIGINT NOT NULL,
      item_id INT NOT NULL,
      partner_id BIGINT NOT NULL,
      agent_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      amount DECIMAL(20, 6) NOT NULL DEFAULT 0, 
      address_from VARCHAR(64) NOT NULL,
      address_to VARCHAR(64) NOT NULL,
      txid VARCHAR(96) NOT NULL,
      UNIQUE(txid)
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_recharge_trc20_bind_set(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      time BIGINT NOT NULL,
      f_log_id BIGINT NOT NULL,
      buyreq_id BIGINT NOT NULL,
      bind_key VARCHAR(64),
      amount DECIMAL(20, 6) NOT NULL DEFAULT 0, 
      txid VARCHAR(96) NOT NULL,
      reason VARCHAR(128) NOT NULL,
      UNIQUE(txid)
    )"""

    sqls.append(sql)


    ###

    sql = """CREATE TABLE IF NOT EXISTS acrm_buy_req(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      item_id INT NOT NULL,
      agent_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      time BIGINT NOT NULL,
      trader_id BIGINT NOT NULL,
      t_type_id INT NOT NULL,
      t_obj_id BIGINT NOT NULL,
      f_log_id BIGINT NOT NULL,
      price DECIMAL(20, 6) NOT NULL DEFAULT 0, 
      type_name VARCHAR(32) NOT NULL,
      reason VARCHAR(128) NOT NULL
    )"""

    sqls.append(sql)

    ###



    sql = """CREATE TABLE IF NOT EXISTS acrm_token_set(
      id BIGINT NOT NULL PRIMARY KEY,
      type_id INT NOT NULL,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      token VARCHAR(128) NOT NULL,
      data LONGTEXT NOT NULL,
      UNIQUE(token)
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_order(
      id BIGINT NOT NULL PRIMARY KEY,
      partner_id INT NOT NULL,
      user_id BIGINT NOT NULL,
      login_id BIGINT NOT NULL,
      type_id INT NOT NULL,
      state INT NOT NULL,
      symbol_id INT NOT NULL,
      open_time BIGINT NOT NULL,
      open_price DECIMAL(20, 6) NOT NULL DEFAULT 0, 
      volume BIGINT NOT NULL,
      digits INT NOT NULL,
      sl DECIMAL(20, 6) NOT NULL DEFAULT 0,
      tp DECIMAL(20, 6) NOT NULL DEFAULT 0,
      timestamp BIGINT NOT NULL
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_hisorder(
      id BIGINT NOT NULL PRIMARY KEY,
      user_id BIGINT NOT NULL,
      partner_id INT NOT NULL,
      login_id BIGINT NOT NULL,
      order_id BIGINT NOT NULL,
      type_id INT NOT NULL,
      symbol_id INT NOT NULL,
      open_time BIGINT NOT NULL,
      open_price DECIMAL(20, 6) NOT NULL DEFAULT 0, 
      close_time BIGINT NOT NULL,
      close_price DECIMAL(20, 6) NOT NULL DEFAULT 0,
      volume BIGINT NOT NULL,
      digits INT NOT NULL,
      sl DECIMAL(20, 6) NOT NULL DEFAULT 0,
      tp DECIMAL(20, 6) NOT NULL DEFAULT 0,
      timestamp BIGINT NOT NULL,
      profit DECIMAL(20, 6) NOT NULL DEFAULT 0,
      rkey VARCHAR(64) NOT NULL,
      UNIQUE(rkey)
    )"""

    sqls.append(sql)

    ###

    sql = """CREATE TABLE IF NOT EXISTS acrm_mt_account(
      id BIGINT NOT NULL PRIMARY KEY,
      user_id BIGINT NOT NULL,
      agent_id BIGINT NOT NULL,
      partner_id INT NOT NULL,
      trader_id BIGINT NOT NULL,
      type_id INT NOT NULL,
      create_time BIGINT NOT NULL,
      version BIGINT NOT NULL,
      login_id BIGINT NOT NULL,
      state INT NOT NULL,
      state2 INT NOT NULL,
      level INT NOT NULL,
      step INT NOT NULL,
      start_time BIGINT NOT NULL,
      end_time BIGINT NOT NULL,
      leverage INT NOT NULL,
      balance DECIMAL(20, 6) NOT NULL DEFAULT 0,
      groupname VARCHAR(32) NOT NULL,
      username VARCHAR(64) NOT NULL,
      password VARCHAR(32) NOT NULL,
      investor VARCHAR(32) NOT NULL,
      phonepwd VARCHAR(32) NOT NULL, 
      UNIQUE(login_id)
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_trader(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      agent_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      create_time BIGINT NOT NULL,
      level INT NOT NULL,

      intern_login_id BIGINT NOT NULL,
      formal_login_id BIGINT NOT NULL,
      upreq_id BIGINT NOT NULL
    )"""

    if False:
      """
      level INT NOT NULL,
      formal_state INT NOT NULL,
      formal_start_time BIGINT NOT NULL,

      intern_state INT NOT NULL,
      intern_step INT NOT NULL,
      intern_start_time BIGINT NOT NULL,
      intern_end_time BIGINT NOT NULL,

      """

    sqls.append(sql)


    sql = """CREATE TABLE IF NOT EXISTS acrm_mt_account_mail_notify(
      login_id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      user_id BIGINT NOT NULL
    )"""

    sqls.append(sql)

    ####

    sql = """CREATE TABLE IF NOT EXISTS acrm_order_checkout(
      id BIGINT NOT NULL PRIMARY KEY,
      time BIGINT NOT NULL,
      login_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      agent_id BIGINT NOT NULL,
      order_id BIGINT NOT NULL,
      symbol_id INT NOT NULL,
      digits INT NOT NULL,
      volume DECIMAL(20, 6) NOT NULL DEFAULT 0,
      open_time BIGINT NOT NULL,
      open_price DECIMAL(20, 6) NOT NULL DEFAULT 0,
      close_price DECIMAL(20, 6) NOT NULL DEFAULT 0,
      sl DECIMAL(20, 6) NOT NULL DEFAULT 0,
      tp DECIMAL(20, 6) NOT NULL DEFAULT 0,
      remark VARCHAR(32) NOT NULL
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_intern_apply(
      id BIGINT NOT NULL PRIMARY KEY,
      agent_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      state INT NOT NULL,
      login_id BIGINT NOT NULL,
      result_id BIGINT NOT NULL,
      level INT NOT NULL,
      step INT NOT NULL,
      create_time BIGINT NOT NULL,
      close_time BIGINT NOT NULL,
      reason VARCHAR(256) NOT NULL
    )"""

    sqls.append(sql)


    sql = """CREATE TABLE IF NOT EXISTS acrm_intern_result(
      id BIGINT NOT NULL PRIMARY KEY,
      agent_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      state INT NOT NULL,
      login_id BIGINT NOT NULL,
      create_time BIGINT NOT NULL,
      level INT NOT NULL,
      step INT NOT NULL,
      data LONGTEXT NOT NULL
    )"""

    sqls.append(sql)


    ####

    sql = """CREATE TABLE IF NOT EXISTS acrm_rech_wiretrans(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      item_id INT NOT NULL,
      create_time BIGINT NOT NULL,
      agent_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      f_log_id BIGINT NOT NULL,
      pay_time BIGINT NOT NULL,
      amount DECIMAL(20, 6) NOT NULL DEFAULT 0,
      remitter VARCHAR(32) NOT NULL,
      email VARCHAR(64) NOT NULL,
      reason VARCHAR(256) NOT NULL
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_trader_apply(
      id BIGINT NOT NULL PRIMARY KEY,
      trader_id BIGINT NOT NULL,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      name VARCHAR(64) NOT NULL,
    )"""

    sqls.append(sql)


    sql = """CREATE TABLE IF NOT EXISTS acrm_recharge_register(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      email VARCHAR(64) NOT NULL,
      t_type_id INT NOT NULL,
      t_obj_id BIGINT NOT NULL,
      amount DECIMAL(20, 6) NOT NULL,
      create_time BIGINT NOT NULL
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_keydata(
      id VARCHAR(64) NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      data LONGTEXT NOT NULL
    )"""

    sqls.append(sql)

    #
    sql = """CREATE TABLE IF NOT EXISTS acrm_reg_apply(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      agent_id BIGINT NOT NULL,
      email VARCHAR(64) NOT NULL,
      reason VARCHAR(128) NOT NULL,
      data LONGTEXT NOT NULL
    )"""

    sqls.append(sql)

    ##
    sql = """CREATE TABLE IF NOT EXISTS acrm_stripe_set(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      email VARCHAR(64) NOT NULL,
      cus_id VARCHAR(64) NOT NULL,
      card_id VARCHAR(64) NOT NULL,
      reason VARCHAR(256) NOT NULL,
      data LONGTEXT NOT NULL
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_stripe_subjob(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      set_id BIGINT NOT NULL,
      price_id VARCHAR(64) NOT NULL,
      sub_id VARCHAR(64) NOT NULL,
      job_id VARCHAR(64) NOT NULL,
      reason VARCHAR(128) NOT NULL,
      response_data LONGTEXT NOT NULL
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_stripe_invquery(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      create_time BIGINT NOT NULL,
      hash_key VARCHAR(96) NOT NULL,
      reason VARCHAR(128) NOT NULL,
      data LONGTEXT NOT NULL,
      UNIQUE(hash_key)
    )"""

    sqls.append(sql)

    sql = """CREATE TABLE IF NOT EXISTS acrm_stripe_invlog(
      id BIGINT NOT NULL PRIMARY KEY,
      state INT NOT NULL,
      time BIGINT NOT NULL,
      paid TINYINT NOT NULL,
      amount DECIMAL(20, 6) NOT NULL,
      status VARCHAR(32) NOT NULL,
      number VARCHAR(32) NOT NULL,
      inv_id VARCHAR(64) NOT NULL,
      cus_id VARCHAR(64) NOT NULL,
      sub_id VARCHAR(64) NOT NULL,
      job_id VARCHAR(64) NOT NULL,
      email VARCHAR(64) NOT NULL,
      agent_id BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      f_log_id BIGINT NOT NULL,
      reason VARCHAR(128) NOT NULL,
      UNIQUE(inv_id)
    )"""

    sqls.append(sql)



      

    for sql in sqls:
      try:
        print("execute", sql)
        cursor.execute(sql)
        rs = cursor.fetchall()
        print("rs", rs)
      except Exception as ex:
        print("ex", ex)
