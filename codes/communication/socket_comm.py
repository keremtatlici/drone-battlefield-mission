import codes.database as db
import socket
import cv2
import numpy as np
import time
import imutils
import base64
import sys
import pickle
import struct
import json


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
            

def liveframe_socket():
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = 9998
    socket_address = (db.ip,port)
    server.bind(socket_address)
    server.listen(5)
    client, address = server.accept()

    while True:
        if db.liveframe is not None:
            time.sleep(0.100) 
            frame = db.liveframe.frame
            width= db.liveframe.width
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            print("liveframe göndermeye çalışıyor ..")
            client.sendall(message)            
            print(frame.shape)

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
    print(db.telemetri_obj)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((db.ip, 9994))
    server.listen()
    client, client_adress = server.accept()   
    print(db.telemetri_obj)
    print(type(db.telemetri_obj.pitch))
    print(type(db.telemetri_obj.roll))
    while True:
        if db.telemetri_obj is not None:
            db.telemetri_obj.update()
            time.sleep(0.100)
            message = {'pitch': db.telemetri_obj.pitch, 'roll': db.telemetri_obj.roll}
            print(message)
            client.send(json.dumps(message).encode())
            
