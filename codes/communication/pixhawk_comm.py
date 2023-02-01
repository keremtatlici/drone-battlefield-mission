from dronekit import connect,Vehicle, LocationGlobalRelative
import codes.database as db
import time

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

class telemetriClass():
    def __init__(self,vehicle):
        self.vehicle = vehicle
        self.update()
        time.sleep(2)
        self.takeoff_coordinate = [self.lat, self.lon, self.alt]

    def update(self):
        self.pitch = self.vehicle.attitude.pitch
        self.yaw = self.vehicle.attitude.yaw
        self.roll = self.vehicle.attitude.roll
        self.mode = self.vehicle.mode.name
        self.battery = self.vehicle.battery
        self.groundspeed = self.vehicle.groundspeed
        self.airspeed = self.vehicle.airspeed
        self.lat = self.vehicle.location.global_relative_frame.lat
        self.lon = self.vehicle.location.global_relative_frame.lon
        self.alt = self.vehicle.location.global_relative_frame.alt
        #self.channels = self.vehicle.channels
        

    def printAll(self):
        self.update()
        print(" TAKE OFF COORDINATE : ", self.takeoff_coordinate)
        print(f'pitch: {self.pitch}, yaw: {self.yaw}, roll: {self.roll}')
        print(f'groundspeed: {self.groundspeed}, airspeed: {self.airspeed}')
        print(f'mode: {self.mode}')
        print(f'battery: {self.battery}')
        print(f'GPS: lat: {self.lat}, lon: {self.lon}, alt: {self.alt}')
        #print(f'channels: {self.channels}')
        time.sleep(1)


def vehicle_conn():
    db.vehicle = connect('/dev/serial/by-id/usb-ArduPilot_Pixhawk4_1F0024000F50563758363720-if00',wait_ready = False , baud = 57600,vehicle_class = MyVehicle)
    time.sleep(2)
    db.telemetri_obj = telemetriClass(db.vehicle)

def get_telemetri():
    while True:
        db.telemetri_obj.printAll()

def go2coordinate(x,y):
    if db.vehicle.channel['7'] == 2004:
        coordinate = LocationGlobalRelative(x, y, db.vehicle.location.global_relative_frame.alt)
        db.vehicle.simple_goto(coordinate)

"""
    print('#####')
    print('vehicle mode : ', vehicle.mode.name)
    print('#####')
    print('vehicle bataryası: ',vehicle.battery)
    print('#####')
    print('gps: ',vehicle.location.global_relative_frame)
    print('#####')
    print('gps2: ',vehicle.location.global_frame)
    print('#####')
    print('groundspeed: ',vehicle.groundspeed)
    print('#####')
    print('airspeed: ',vehicle.airspeed)
    print('#####')
    print('channel', vehicle.channels)
"""

