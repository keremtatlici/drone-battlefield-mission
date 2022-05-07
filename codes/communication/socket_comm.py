import codes.database as db
import socket
import cv2
import numpy as np
import time



def mission_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((db.ip, 9999))
    server.listen()
    client, client_adress = server.accept()

    while True:
        message =client.recv(1024)
        print(message)
        time.sleep(0.050)
        message = message.decode("ascii")
        if message == "firstmissionstart":
            db.first_mission=True
            db.second_mission=False
        elif message == "firstmissionend":
            db.first_mission=False
        elif message == "secondmissionstart":
            db.first_mission=False
            db.second_mission=True
        elif message == "secondmissionend":
            db.second_mission=False
        else:
            print("HATA")
            pass
        print(message)
        client.send(message.encode("ascii"))

def liveframe_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((db.ip, 9998))
    server.listen()
    client, client_adress = server.accept()

    while True:
        if db.liveframe is not None:
            pass

def normalframe_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((db.ip, 9997))
    server.listen()
    client, client_adress = server.accept()

    while True:
        if db.normalframe is not None:
            pass

def coordinate_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((db.ip, 9996))
    server.listen()
    client, client_adress = server.accept()

    while True:
        if db.normalframe is not None:
            pass

def label_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((db.ip, 9995))
    server.listen()
    client, client_adress = server.accept()

    while True:
        if db.normalframe is not None:
            pass

def telemetri_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((db.ip, 9994))
    server.listen()
    client, client_adress = server.accept()   

    while True:
        if db.telemetri is not None:
            pass 
