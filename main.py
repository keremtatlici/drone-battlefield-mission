import firstmission
import codes.database as db
import codes.communication.socket_comm as socket_comm
from threading import Thread

mission_socket_process = Thread(target=socket_comm.mission_socket)

mission_socket_process.start()


while True:
    firstmission.main()

