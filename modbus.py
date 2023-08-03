from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
from to_db import DBConnection
import string
import random
import calendar
import time
from datetime import datetime 
import time
import struct
from threading import Timer

def convert_value(regs2):
    b1, b2 = bin(regs2[1]), bin(regs2[0]) # возвращаем в двоичное представление числа
    reg1, reg2 = b1[2:], b2[2:] # убираем '0b'
    reg1, reg2 = reg1.rjust(16, '0'), reg2.rjust(16, '0') # если длина не 16 добавить нули в начало
    b = reg1 + reg2 
    b_to_int = int(b, 2)
    return struct.unpack('f', struct.pack('I', b_to_int))[0]
addresses = {"voltage_a": (5240,2), 
             "current_a": (5252, 2),
             "active_power_a": (5264, 2),
             "reactive_power_a": (5276, 2),
             "full_power_a": (5288, 2),
             "power_factor_a": (5300, 2),
             "voltage_b": (5242,2), 
             "current_b": (5254, 2),
             "active_power_b": (5266, 2),
             "reactive_power_b": (5278, 2),
             "full_power_b": (5290, 2),
             "power_factor_b": (5302, 2),
             "voltage_c": (5244,2), 
             "current_c": (5256, 2),
             "active_power_c": (5268, 2),
             "reactive_power_c": (5280, 2),
             "full_power_c": (5292, 2),
             "power_factor_c": (5304, 2),
             "interfacial_angle_a_b": (5312, 2),
             "interfacial_angle_b_c": (5314, 2),
             "interfacial_angle_c_a": (5316, 2),
             "interfacial_voltage_a_b": (5324, 2),
             "interfacial_voltage_b_c": (5326, 2),
             "interfacial_voltage_c_a": (5328, 2),
             }
  

db = DBConnection()
c = ModbusClient(host="192.168.1.100", port=502, auto_open=True, debug=True)
while(True):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    values_from_device=[current_time]
    addresses_names=["reading_time"]  
    for address_name, address_key in addresses.items():
        reg_addr, reg_nb=address_key
        regs2 = c.read_input_registers(reg_addr, reg_nb)
        value = convert_value(regs2)
        addresses_names.append(address_name)
        values_from_device.append(value)
    db.add_reg(addresses_names,*values_from_device)
    time.sleep(0.875)
"""
for i in range(24):
    current_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ').replace(hour=i).strftime('%Y-%m-%dT%H:%M:%SZ')
    work_status=random.randint(0,2)
    for j in range(60):
        current_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ').replace(minute=j).strftime('%Y-%m-%dT%H:%M:%SZ')
        db.add_reg("192.168.3.4", random.randint(10,29), current_time, work_status)

"""
