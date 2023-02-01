import firstmission
import codes.database as db
import codes.communication.socket_comm as socket_comm
from threading import Thread
import codes.communication.pixhawk_comm as pixhawk_comm
import codes.communication.arduino_comm as arduino_comm
import time

mission_socket_process = Thread(target=socket_comm.mission_socket)
liveframe_socket_process = Thread(target= socket_comm.liveframe_socket)
get_telemetri_process = Thread(target= pixhawk_comm.get_telemetri)
telemetri_socket_process = Thread(target=socket_comm.telemetri_socket)

pixhawk_comm.vehicle_conn()
mission_socket_process.start()
liveframe_socket_process.start()
#get_telemetri_process.start()
#telemetri_socket_process.start()
db.arduino = arduino_comm.connect_to_arduino()

#db.first_mission=True

while True:
    firstmission.main()
