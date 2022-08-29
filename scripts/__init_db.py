import os
import time
from acrm.models import AgentUserEntry
from acrm.networking import NetManager

net_mgr = NetManager.get_inst()

def main(args):
  
  schema_data = net_mgr.sys_call("SCHEMA")
  print("SCHEMA", schema_data)

  
  schema_data = {'_last_sync_finlog_id': 1125899906842951, 'last_obj_id1': 1099511627785, 'last_obj_id2': 17592186044426, 'last_obj_id3': 140737488355416, 'last_obj_id4': 1125899906842951, 'last_user_id': 12884901934}
  

  net_mgr.sys_call("SCHEMA_SET_MIN", schema_data)
  
  agent_id = 12884901888

  try:
    agent_user = AgentUserEntry.objects.get(id=agent_id)
  except AgentUserEntry.DoesNotExist:
    agent_user = AgentUserEntry(
      id=agent_id,
      state=1,
      state2=0,
      create_time = time.time(),
      action_time = time.time(),
      partner_id=201,
      invit_code="FCW888",
      username="admin",
      secret_key=os.urandom(8).hex(),
      password="",
      security_password="",
      email="admin@gmail.com"
    )

    agent_user.save()
  print("root agent", agent_user)
