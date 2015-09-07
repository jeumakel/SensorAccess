#!/usr/bin/env python
from __future__ import division
from subprocess import PIPE, Popen
import psutil
import json
import config

class SensorAccess(object):
    def __init__(self):
        #Initializing
        pass

    def get_cpu_temperature(self, is_json = False):
        process = Popen([config.exec_path + 'vcgencmd', 'measure_temp'], stdout=PIPE)
        output, _error = process.communicate()
        value = float(output[output.index('=') + 1:output.rindex("'")])
        if is_json:
            return json.dumps({"cpu_temp": value})
        return value

    def _get_nic(self, nic_list):
        wifi_name = False
        #print nic_list
        if not nic_list:
            return False
        for nic_name in list(nic_list.keys()):
            if nic_name != 'lo' and nic_name != 'eth0':
                wifi_name = nic_name
                break
        #print nic_list['eth0']
        if wifi_name:
            return nic_list[wifi_name]
        elif nic_list['eth0']:
            return nic_list['eth0']
        else:
            return nic_list['lo']

    def get_bytes_received(self, is_json = False):
        #net_stats = psutil.net_io_counters() #original
        net_stats = psutil.network_io_counters(pernic=True)
        nic = self._get_nic(net_stats)
        if nic:
            if is_json:
                return json.dumps({"bytes_recv": nic.bytes_recv})
            return nic.bytes_recv
        else:
            if is_json:
                return {"bytes_recv": 0}
            return 0 

    def get_bytes_sent(self, is_json = False):
        #net_stats = psutil.net_io_counters() #original
        net_stats = psutil.network_io_counters(pernic=True)
        nic = self._get_nic(net_stats)
        if nic:
            if is_json:
                return json.dumps({"bytes_sent": nic.bytes_sent})
            return nic.bytes_sent
        else:
            if is_json:
                return json.dumps({"bytes_sent": 0})
            return 0 

    def get_cpu_usage(self, is_json = False):
        value = psutil.cpu_percent()
        if is_json:
            return json.dumps({"cpu_usage": value})
        return value

    def get_all_json(self):
        return json.dumps({"cpu_temp": self.get_cpu_temperature(False), "cpu_usage": self.get_cpu_usage(False), "net_sent": self.get_bytes_sent(False), "net_recv": self.get_bytes_received(False)})


