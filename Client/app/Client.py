# -*- coding: utf-8 -*-

import logging
import io
import socket
import struct
from app.PID import *
from app.Face import *
import numpy as np
from PIL import Image
import Variables


class Client:
    def __init__(self):
        logging.basicConfig(format=Variables.Settings.LOG_FORMAT, level=Variables.Settings.LOG_LEVEL)
        self.face = Face()
        self.pid = Incremental_PID(1, 0, 0.0025)
        self.tcp_flag = False
        self.video_flag = True
        self.face_id = False
        self.face_recognition_flag = False
        self.image = ''
        self.client_socket1 = None
        self.client_socket = None
  #      self.connection = None
        self.ip = "127.0.0.1"

    def turn_on_client(self, ip):
        logging.info("Set client connection setting with: %s" % ip)
        self.ip = ip
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def turn_off_client(self):
        logging.info("Closing connection with server at IP: %s" % self.ip)
        try:
            self.client_socket.shutdown(2)
            self.client_socket1.shutdown(2)
            self.client_socket.close()
            self.client_socket1.close()
        except Exception as e:
            logging.error("Exception while closing connection with server %s reason: %s" % (self.ip, e))

    def is_valid_image_4_bytes(self, buf):
#        print('v')
        is_valid = True
        if buf[6:10] in (b'JFIF', b'Exif'):
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                is_valid = False
        else:
            try:
                Image.open(io.BytesIO(buf)).verify()
            except:
                is_valid = False
        return is_valid

    def receiving_video(self, ip):
        try:
            self.client_socket.connect((ip, Variables.Settings.CONN_PORT_VIDEO))
            self.connection = self.client_socket.makefile('rb')
        except:
            #print ("command port connect failed")
            pass
        while True:
            try:
                stream_bytes = self.connection.read(4)

                leng = struct.unpack('<L', stream_bytes[:4])
#                print('unpack %s leng %s' % (stream_bytes, leng))
                jpg = self.connection.read(leng[0])
                if self.is_valid_image_4_bytes(jpg):
                    if self.video_flag:
                        self.image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        if self.face_id is False and self.face_recognition_flag:
                            self.face.face_detect(self.image)
                        self.video_flag = False
            except BaseException as e:
                print(e)
                break

    def send_data(self, data):
        payload = data + '\n'
        if self.tcp_flag:
            try:
                self.client_socket1.send(payload.encode('utf-8'))
            except Exception as e:
                print(e)

    def receive_data(self):
        data = ""
        data = self.client_socket1.recv(1024).decode('utf-8')
        return data


if __name__ == '__main__':
    c = Client()
    c.face_recognition()
