from pyModbusTCP.client import ModbusClient
from to_db import DBConnection
import time
from datetime import datetime 
import time
import struct
from threading import Thread

def convert_value(regs2):
    b1, b2 = bin(regs2[1]), bin(regs2[0]) # возвращаем в двоичное представление числа
    reg1, reg2 = b1[2:], b2[2:] # убираем '0b'
    reg1, reg2 = reg1.rjust(16, '0'), reg2.rjust(16, '0') # если длина не 16 добавить нули в начало
    b = reg1 + reg2 
    b_to_int = int(b, 2)
    return struct.unpack('f', struct.pack('I', b_to_int))[0]

class Stand:
 
    def __init__(self, ip, sensor_data, table_name):
        self.c = ModbusClient(host=ip, port=502, auto_open=True, debug=True)
        self.sensor_data = sensor_data        
        self.table_name= table_name

    def forward(self):
        while(True):
            addresses = self.sensor_data
            current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            values_from_device=[current_time]
            addresses_names=["reading_time"]
            for address_name, address_key in addresses.items():
                reg_addr, reg_nb=address_key
                regs = self.c.read_input_registers(reg_addr, reg_nb)
                value = convert_value(regs)
                addresses_names.append(address_name)
                if self.table_name=="sensor_data1" or self.table_name=="sensor_data2":
                    value = -0.013*(value**2)+1.502*value-1.525
                values_from_device.append(round(value,3))
            db.add_reg(self.table_name, addresses_names,*values_from_device)
            time.sleep(1)

if __name__ == "__main__":
    sensor_data1 = {"voltage": (4000,2)}
    sensor_data2 = {"voltage_a": (4000,2),"voltage_b": (4003,2),"voltage_c": (4006,2)}
    sensor_data3 = {"voltage_a": (5240,2), 
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
    
    
    stand1=Stand("192.168.1.101", sensor_data1,  "sensor_data1")
    stand2=Stand("192.168.1.99", sensor_data2, "sensor_data2")
    stand3=Stand("192.168.1.98", sensor_data3, "sensor_data3")
    th1 = Thread(target=stand1.forward)
    th1.start()
    th2 = Thread(target=stand2.forward)
    th2.start()
    th3 = Thread(target=stand3.forward)
    th3.start()
    th1.join()
    th2.join()
    th3.join()
