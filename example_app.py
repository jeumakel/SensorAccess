#!/usr/bin/env python
from SensorAccess import SensorAccess

sensor_access = SensorAccess()
print "Temperature: ", sensor_access.get_cpu_temperature(), "'C"
print "Network total received:", sensor_access.get_bytes_received(), "bytes"
print "Network total sent:", sensor_access.get_bytes_sent(), "bytes"
print "CPU usage percentage:", sensor_access.get_cpu_usage(), "%"


