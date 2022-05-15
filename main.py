import firstmission
import codes.database as db
import codes.communication.socket_comm as socket_comm
from threading import Thread
import codes.communication.pixhawk_comm as pixhawk_comm

mission_socket_process = Thread(target=socket_comm.mission_socket)
liveframe_socket_process = Thread(target= socket_comm.liveframe_socket)
get_telemetri_process = Thread(target= pixhawk_comm.get_telemetri)


#pixhawk_comm.vehicle_conn()
#mission_socket_process.start()
liveframe_socket_process.start()
#get_telemetri_process.start()


while True:
    firstmission.main()

