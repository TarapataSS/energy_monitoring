from pyModbusTCP.client import ModbusClient
from to_db import DBConnection
import string


db = DBConnection()
# TCP auto connect on modbus request, close after it
c = ModbusClient(host="localhost", auto_open=True, debug=True)

regs = c.read_holding_registers(0,3)

db.add_reg(c.host, regs[2])