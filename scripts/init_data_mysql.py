from django.db import connection
from fcworks.conf import settings as _settings


def main(*args):
  with connection.cursor() as cursor:
    db_ctx = _settings.COIN_MYSQL_DATABASE
      
    db_name = db_ctx["NAME"]

    sqls = [
      "ALTER DATABASE %s CHARACTER SET utf8;" % db_name,
    ]

    sql = """INSERT INTO system (`id`, `ant_index`, `cash_index`, `pay_index`) VALUES ('0', '0', '0', '0')"""
    sqls.append(sql)


    for sql in sqls:
      try:
        print("execute", sql)
        cursor.execute(sql)
        rs = cursor.fetchall()
        print("rs", rs)
      except Exception as ex:
        print("ex", ex)
