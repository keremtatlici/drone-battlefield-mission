from dronekit import connect,Vehicle

class MyVehicle(Vehicle):
    def __init__(self, connection_string):
        super(MyVehicle, self).__init__(connection_string)
        self._system_time = SystemTIME()
        @self.on_message('SYSTEM_TIME')
        def listener(self, name, message):
            self._system_time.time_boot_unix=int (message.time_unix_usec)
            self._system_time.time_boot_ms = int (message.time_boot_ms )


    @property
    def system_time(self):
        return self._system_time

class SystemTIME(object):
    def __init__(self, time_boot_unix=None , time_boot_ms=None):
        self.time_boot_unix = time_boot_unix
        self.time_boot_ms = time_boot_ms
    def __str__(self):
        return "{}".format(self.time_boot_unix,self.time_boot_ms)

def vehicle_conn():
    db.vehicle = connect('/dev/serial/by-id/usb-ArduPilot_Pixhawk4_1F0024000F50563758363720-if00',wait_ready = False , baud = 57600,vehicle_class = MyVehicle)

def get_telemetri():
    while True:
        db.pitch= db.vehicle.attitude
        db.yaw= db.vehicle.attitude
        db.roll= db.vehicle.attitude

