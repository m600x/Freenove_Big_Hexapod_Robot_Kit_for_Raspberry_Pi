# -*- coding: utf-8 -*-
import threading

from interface.ui_led import Ui_led
from interface.ui_face import Ui_Face
from interface.ui_client import Ui_client
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from app.Client import *
from interface.Calibration import *
from app.Functions import *
import Variables
import math
import Thread
import logging


class MyWindow(QMainWindow, Ui_client):
    def __init__(self):
        logging.basicConfig(format=Variables.Settings.LOG_FORMAT, level=Variables.Settings.LOG_LEVEL)
        print(logging.DEBUG)
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.client = Client()
        self.fct = Functions(self)
        self.Video.setScaledContents(True)

        # Read files containing IP and images with error handling
        if hasattr(Variables.Settings, 'FILEPATH_WINDOW_ICON'):
            logging.debug("Set %s as window icon" % Variables.Settings.FILEPATH_WINDOW_ICON)
            self.setWindowIcon(QIcon(Variables.Settings.FILEPATH_WINDOW_ICON))
        if hasattr(Variables.Settings, 'FILEPATH_WINDOW_CAMERA'):
            logging.debug("Set %s as camera placeholder image" % Variables.Settings.FILEPATH_WINDOW_CAMERA)
            self.Video.setPixmap(QPixmap(Variables.Settings.FILEPATH_WINDOW_CAMERA))
        if hasattr(Variables.Settings, 'FILEPATH_IP'):
            try:
                file = open(Variables.Settings.FILEPATH_IP, 'r')
                self.lineEdit_IP_Adress.setText(str(file.readline()))
                logging.debug("Read IP %s from file" % self.lineEdit_IP_Adress.text())
                file.close()
            except FileNotFoundError:
                logging.error("Cannot read file %s defaulting to blank IP" % Variables.Settings.FILEPATH_IP)

        self.Key_W = False
        self.Key_A = False
        self.Key_S = False
        self.Key_D = False
        self.Key_Space = False

        # Map button click event to function
        self.Button_Connect.clicked.connect(self.connect)
        self.Button_Video.clicked.connect(self.fct.video)
        self.Button_IMU.clicked.connect(self.fct.balance)
        self.Button_Calibration.clicked.connect(self.show_calibration_window)
        self.Button_LED.clicked.connect(self.show_led_window)
        self.Button_Face_ID.clicked.connect(self.show_face_window)
        self.Button_Face_Recognition.clicked.connect(self.face_recognition)
        self.Button_Sonic.clicked.connect(self.fct.ultrasonic)
        self.Button_Relax.clicked.connect(self.fct.motors_status)
        self.Button_Buzzer.pressed.connect(self.fct.buzzer)
        self.Button_Buzzer.released.connect(self.fct.buzzer)

        # Head slider for vertical movement
        self.slider_head.setMinimum(Variables.Settings.HEAD_VERTICAL_MIN)
        self.slider_head.setMaximum(Variables.Settings.HEAD_VERTICAL_MAX)
        self.slider_head.setSingleStep(Variables.Settings.HEAD_VERTICAL_STEP)
        self.slider_head.setValue(Variables.Settings.HEAD_VERTICAL_DEFAULT)
        self.slider_head.valueChanged.connect(self.fct.head_move_vertical)

        # Head slider for horizontal movement
        self.slider_head_1.setMinimum(Variables.Settings.HEAD_HORIZONTAL_MIN)
        self.slider_head_1.setMaximum(Variables.Settings.HEAD_HORIZONTAL_MAX)
        self.slider_head_1.setSingleStep(Variables.Settings.HEAD_HORIZONTAL_STEP)
        self.slider_head_1.setValue(Variables.Settings.HEAD_HORIZONTAL_DEFAULT)
        self.slider_head_1.valueChanged.connect(self.fct.head_move_horizontal)

        # Movement speed slider
        self.slider_speed.setMinimum(Variables.Settings.SPEED_MIN)
        self.slider_speed.setMaximum(Variables.Settings.SPEED_MAX)
        self.slider_speed.setSingleStep(Variables.Settings.SPEED_STEP)
        self.slider_speed.setValue(Variables.Settings.SPEED_DEFAULT)
        self.slider_speed.valueChanged.connect(self.speed)
        self.client.move_speed = str(self.slider_speed.value())

        # Roll slider
        self.slider_roll.setMinimum(Variables.Settings.ROLL_MIN)
        self.slider_roll.setMaximum(Variables.Settings.ROLL_MAX)
        self.slider_roll.setSingleStep(Variables.Settings.ROLL_STEP)
        self.slider_roll.setValue(Variables.Settings.ROLL_DEFAULT)
        self.slider_roll.valueChanged.connect(self.set_roll)
        # Z height slider
        self.slider_Z.setMinimum(Variables.Settings.Z_HEIGHT_MIN)
        self.slider_Z.setMaximum(Variables.Settings.Z_HEIGHT_MAX)
        self.slider_Z.setSingleStep(Variables.Settings.Z_HEIGHT_STEP)
        self.slider_Z.setValue(Variables.Settings.Z_HEIGHT_DEFAULT)
        self.slider_Z.valueChanged.connect(self.set_z_height)
        # Set default checkbox status
        self.ButtonActionMode1.setChecked(True)
        self.ButtonActionMode1.toggled.connect(lambda: self.fct.action_mode(self.ButtonActionMode1))
        self.ButtonActionMode2.setChecked(False)
        self.ButtonActionMode2.toggled.connect(lambda: self.fct.action_mode(self.ButtonActionMode2))
        self.ButtonGaitMode1.setChecked(True)
        self.ButtonGaitMode1.toggled.connect(lambda: self.fct.gait_mode(self.ButtonGaitMode1))
        self.ButtonGaitMode2.setChecked(False)
        self.ButtonGaitMode2.toggled.connect(lambda: self.fct.gait_mode(self.ButtonGaitMode2))
        # Start timers
        self.timer_power = QTimer(self)
        self.timer_power.timeout.connect(self.power)
        # Variables
        self.power_value = [100, 100]
        self.move_point = [325, 635]
        self.move_flag = False
        self.draw_point = [[800, 180], [800, 650]]
        self.action_flag = 1
        self.gait_flag = 1

        self.CalibrationWindow = None
        self.LedWindow = None
        self.FaceWindow = None

    # keyboard
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_C:
            print("C")
            self.connect()
        if event.key() == Qt.Key_V:
            try:
                print("V")
                self.fct.video()
            except Exception as e:
                print(e)
        if event.key() == Qt.Key_R:
            print("R")
            self.relax()
        if event.key() == Qt.Key_L:
            print("L")
            self.show_led_window()
        if event.key() == Qt.Key_B:
            print("B")
            self.fct.balance()
        if event.key() == Qt.Key_F:
            print("F")
            self.face_recognition()
        if event.key() == Qt.Key_U:
            print("U")
            self.fct.ultrasonic()
        if event.key() == Qt.Key_I:
            print("I")
            self.show_face_window()
        if event.key() == Qt.Key_T:
            print("T")
            self.show_calibration_window()
        if event.key() == Qt.Key_Y:
            print("Y")
            self.buzzer()
        if event.isAutoRepeat():
            pass
        else:
            if event.key() == Qt.Key_W:
                self.Key_W = True
                print("W")
                self.move_point = [325, 535]
                self.move()
            elif event.key() == Qt.Key_S:
                self.Key_S = True
                print("S")
                self.move_point = [325, 735]
                self.move()
            elif event.key() == Qt.Key_A:
                self.Key_A = True
                print("A")
                self.move_point = [225, 635]
                self.move()
            elif event.key() == Qt.Key_D:
                self.Key_D = True
                print("D")
                self.move_point = [425, 635]
                self.move()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W:
            if not (event.isAutoRepeat()) and self.Key_W is True:
                print("release W")
                self.Key_W = False
                self.move_point = [325, 635]
                self.move()
        elif event.key() == Qt.Key_A:
            if not (event.isAutoRepeat()) and self.Key_A is True:
                print("release A")
                self.Key_A = False
                self.move_point = [325, 635]
                self.move()
        elif event.key() == Qt.Key_S:
            if not (event.isAutoRepeat()) and self.Key_S is True:
                print("release S")
                self.Key_S = False
                self.move_point = [325, 635]
                self.move()
        elif event.key() == Qt.Key_D:
            if not (event.isAutoRepeat()) and self.Key_D is True:
                print("release D")
                self.Key_D = False
                self.move_point = [325, 635]
                self.move()

    def paintEvent(self, e):
        try:
            qp = QPainter()
            qp.begin(self)
            qp.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            qp.drawRect(700, 80, 200, 200)
            qp.drawRect(700, 550, 200, 200)
            qp.setRenderHint(QPainter.Antialiasing)

            # steering wheel
            qp.setPen(Qt.NoPen)
            qp.setBrush(QBrush(Qt.gray))
            # QColor(0,138,255) Qt.white
            qp.drawEllipse(QPoint(325, 635), 100, 100)
            qp.setBrush(QBrush(QColor(0, 138, 255)))
            qp.drawEllipse(QPoint(self.move_point[0], self.move_point[1]), 15, 15)
            qp.setPen(QPen(QColor(0, 138, 255), 2, Qt.SolidLine))
            x1 = round(math.sqrt(100 ** 2 - (self.move_point[1] - 635) ** 2) + 325)
            y1 = round(math.sqrt(100 ** 2 - (self.move_point[0] - 325) ** 2) + 635)
            qp.drawLine(x1, self.move_point[1], 650 - x1, self.move_point[1])
            qp.drawLine(self.move_point[0], 1270 - y1, self.move_point[0], y1)

            # attitude
            qp.drawLine(self.draw_point[0][0], 80, self.draw_point[0][0], 280)
            qp.drawLine(700, self.draw_point[0][1], 900, self.draw_point[0][1])
            self.label_attitude.move(self.draw_point[0][0] + 10, self.draw_point[0][1] + 10)
            pitch = round((180 - self.draw_point[0][1]) / 100.0 * 15)
            yaw = round((self.draw_point[0][0] - 800) / 100.0 * 15)
            self.label_attitude.setText(str((yaw, pitch)))

            # position
            qp.drawLine(self.draw_point[1][0], 550, self.draw_point[1][0], 750)
            qp.drawLine(700, self.draw_point[1][1], 900, self.draw_point[1][1])
            self.label_position.move(self.draw_point[1][0] + 10, self.draw_point[1][1] + 10)
            y = round((650 - self.draw_point[1][1]) / 100.0 * 40)
            x = round((self.draw_point[1][0] - 800) / 100.0 * 40)
            self.label_position.setText(str((x, y)))
            qp.end()
        except Exception as e:
            print(e)

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if 700 <= x <= 900:
            if 80 <= y <= 280:
                try:
                    self.draw_point = [[800, 180], [800, 650]]
                    if self.move_flag:
                        self.move_point = [325, 635]
                        self.move_flag = False
                        self.move()
                    if self.Button_IMU.text() == Variables.InterfaceText.UI_BALANCE_ON:
                        self.Button_IMU.setText(Variables.InterfaceText.UI_BALANCE_OFF)

                    self.draw_point[0][0] = x
                    self.draw_point[0][1] = y
                    self.update()
                    self.attitude()
                except Exception as e:
                    print(e)
            elif 550 <= y <= 750:
                try:
                    self.draw_point = [[800, 180], [800, 650]]
                    if self.move_flag:
                        self.move_point = [325, 635]
                        self.move_flag = False
                        self.move()
                    if self.Button_IMU.text() == Variables.InterfaceText.UI_BALANCE_ON:
                        self.Button_IMU.setText(Variables.InterfaceText.UI_BALANCE_OFF)
                    self.move_point = [325, 635]
                    self.draw_point[1][0] = x
                    self.draw_point[1][1] = y
                    self.update()
                    self.position()
                except Exception as e:
                    print(e)
        elif 225 <= x <= 425 and 550 <= y <= 750:
            r = (x - 325) ** 2 + (635 - y) ** 2
            self.draw_point = [[800, 180], [800, 650]]
            if self.Button_IMU.text() == Variables.InterfaceText.UI_BALANCE_ON:
                self.Button_IMU.setText(Variables.InterfaceText.UI_BALANCE_OFF)
            if r < 10000:
                self.move_flag = True
                self.move_point[0] = x
                self.move_point[1] = y
                self.move()
                self.update()
            else:
                x = x - 325
                y = 635 - y
                angle = math.atan2(y, x)
                self.move_point[0] = 100 * math.cos(angle) + 325
                self.move_point[1] = 635 - 100 * math.sin(angle)
                self.move()
                self.update()
        elif self.move_flag is True:
            x = x - 325
            y = 635 - y
            angle = math.atan2(y, x)
            self.move_point[0] = 100 * math.cos(angle) + 325
            self.move_point[1] = 635 - 100 * math.sin(angle)
            self.move()
            self.update()

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if 700 <= x <= 900:
            if 80 <= y <= 280:
                try:
                    self.draw_point = [[800, 180], [800, 650]]
                    if self.move_flag:
                        self.move_point = [325, 635]
                        self.move_flag = False
                        self.move()
                    if self.Button_IMU.text() == Variables.InterfaceText.UI_BALANCE_ON:
                        self.Button_IMU.setText(Variables.InterfaceText.UI_BALANCE_OFF)
                    self.draw_point[0][0] = x
                    self.draw_point[0][1] = y
                    self.update()
                    self.attitude()
                except Exception as e:
                    print(e)
            elif 550 <= y <= 750:
                try:
                    self.draw_point = [[800, 180], [800, 650]]
                    if self.move_flag:
                        self.move_point = [325, 635]
                        self.move_flag = False
                        self.move()
                    if self.Button_IMU.text() == Variables.InterfaceText.UI_BALANCE_ON:
                        self.Button_IMU.setText(Variables.InterfaceText.UI_BALANCE_OFF)
                    self.draw_point[1][0] = x
                    self.draw_point[1][1] = y
                    self.update()
                    self.position()
                except Exception as e:
                    print(e)
        elif 225 <= x <= 425 and 550 <= y <= 750:
            r = (x - 325) ** 2 + (635 - y) ** 2
            self.draw_point = [[800, 180], [800, 650]]
            if self.Button_IMU.text() == Variables.InterfaceText.UI_BALANCE_ON:
                self.Button_IMU.setText(Variables.InterfaceText.UI_BALANCE_OFF)
            if r < 10000:
                self.move_flag = True
                self.move_point[0] = x
                self.move_point[1] = y
                self.move()
                self.update()
            else:
                x = x - 325
                y = 635 - y
                angle = math.atan2(y, x)
                self.move_point[0] = 100 * math.cos(angle) + 325
                self.move_point[1] = 635 - 100 * math.sin(angle)
                self.move()
                self.update()
        elif self.move_flag is True:
            x = x - 325
            y = 635 - y
            angle = math.atan2(y, x)
            self.move_point[0] = 100 * math.cos(angle) + 325
            self.move_point[1] = 635 - 100 * math.sin(angle)
            self.move()
            self.update()

    def mouseReleaseEvent(self, event):
        # x = event.pos().x()
        # y = event.pos().y()
        # print(x,y)
        if self.move_flag:
            self.move_point = [325, 635]
            self.move_flag = False
            self.move()
        self.update()

    @staticmethod
    def map(value, from_low, from_high, to_low, to_high):
        return (to_high - to_low) * (value - from_low) / (from_high - from_low) + to_low

    def face_recognition(self):
        try:
            if self.Button_Face_Recognition.text() == "Face Recog":
                self.client.face_recognition_flag = True
                self.Button_Face_Recognition.setText("Close")
            elif self.Button_Face_Recognition.text() == "Close":
                self.client.face_recognition_flag = False
                self.Button_Face_Recognition.setText("Face Recog")
        except Exception as e:
            print(e)

    def move(self):
        try:
            x = self.map((self.move_point[0] - 325), 0, 100, 0, 35)
            y = self.map((635 - self.move_point[1]), 0, 100, 0, 35)
            if self.action_flag == 1:
                angle = 0
            else:
                if x != 0 or y != 0:
                    angle = math.degrees(math.atan2(x, y))

                    if -90 > angle >= -180:
                        angle = angle + 360
                    if -90 <= angle <= 90:
                        angle = self.map(angle, -90, 90, -10, 10)
                    else:
                        angle = self.map(angle, 270, 90, 10, -10)
                else:
                    angle = 0
            speed = self.client.move_speed
            command = Variables.Commands.CMD_MOVE + "#" + str(self.gait_flag) + "#" + str(round(x)) + "#" + str(round(y)) + "#" + str(speed) + "#" + str(round(angle))
            print(command)
            self.client.send_data(command)
        except Exception as e:
            print(e)

    def attitude(self):
        r = self.map((self.draw_point[0][0] - 800), -100, 100, -15, 15)
        p = self.map((180 - self.draw_point[0][1]), -100, 100, -15, 15)
        y = self.slider_roll.value()
        command = Variables.Commands.CMD_ATTITUDE + "#" + str(round(r)) + "#" + str(round(p)) + "#" + str(round(y))
        print(command)
        self.client.send_data(command)

    def position(self):
        x = self.map((self.draw_point[1][0] - 800), -100, 100, -40, 40)
        y = self.map((650 - self.draw_point[1][1]), -100, 100, -40, 40)
        z = self.slider_Z.value()
        command = Variables.Commands.CMD_POSITION + "#" + str(round(x)) + "#" + str(round(y)) + "#" + str(round(z))
        print(command)
        self.client.send_data(command)

    def closeEvent(self, event):
        try:
            self.timer.stop()
            self.timer_power.stop()
        except Exception as e:
            print(e)
        try:
            Thread.stop_thread(self.videoThread)
        except Exception as e:
            print(e)
        try:
            Thread.stop_thread(self.instructionThread)
        except Exception as e:
            print(e)
        self.client.turn_off_client()
        QCoreApplication.instance().quit()
        # os._exit(0)

    @staticmethod
    def restriction(var, v_min, v_max):
        if var < v_min:
            return v_min
        elif var > v_max:
            return v_max
        else:
            return var

    def power(self):
        try:
            command = Variables.Commands.CMD_POWER
            self.client.send_data(command)
            self.progress_Power1.setFormat(str(self.power_value[0]) + "V")
            self.progress_Power2.setFormat(str(self.power_value[1]) + "V")
            self.progress_Power1.setValue(
                self.restriction(round((float(self.power_value[0]) - 5.00) / 3.40 * 100), 0, 100))
            self.progress_Power2.setValue(
                self.restriction(round((float(self.power_value[1]) - 7.00) / 1.40 * 100), 0, 100))
            # print (command)
        except Exception as e:
            print(e)

    def receive_instruction(self, ip):
        try:
            logging.debug("Trying to establish connection with %s" % ip)
            self.client.client_socket1.connect((ip, Variables.Settings.CONN_PORT_COMMANDS))
            self.client.tcp_flag = True
            logging.info("Connection established successfully with %s" % ip)
            self.Button_Video.setText(Variables.InterfaceText.UI_VIDEO_OFF)
        except Exception as e:
            self.client.tcp_flag = False
            logging.error("Failed to establish connection with %s, reason: %s" % (ip, e))
        while True:
            try:
                payload = self.client.receive_data()
            except:
                self.client.tcp_flag = False
                break
            logging.debug("Received %s" % payload.replace('\\n', '\n'))
            if payload == '':
                break
            else:
                cmd_array = payload.split('\n')
                if cmd_array[-1] != "":
                    cmd_array == cmd_array[:-1]
            for oneCmd in cmd_array:
                data = oneCmd.split("#")
                #                print(data)
                if data == "":
                    self.client.tcp_flag = False
                    break
                elif data[0] == Variables.Commands.CMD_ULTRASONIC:
                    self.label_sonic.setText('Obstacle:' + data[1] + 'cm')
                    logging.debug("Ultrasonic sensor value %s" % data[1])
                elif data[0] == Variables.Commands.CMD_POWER:
                    try:
                        if len(data) == 3:
                            self.power_value[0] = data[1]
                            self.power_value[1] = data[2]
                            logging.debug("Power value received %s and %s" % (self.power_value[0], self.power_value[1]))
                    except Exception as e:
                        print(e)

    # CONNECT
    def connect(self):
        try:
            file = open(Variables.Settings.FILEPATH_IP, 'w')
            file.write(self.lineEdit_IP_Adress.text())
            file.close()
            if self.Button_Connect.text() == Variables.InterfaceText.UI_CONNECT:
                self.IP = self.lineEdit_IP_Adress.text()
                # Connecting
                self.client.turn_on_client(self.IP)
                # Enable Video
                self.Button_Video.setText(Variables.InterfaceText.UI_VIDEO_OFF)
                self.fct.video()
                # Start threading
                self.videoThread = threading.Thread(target=self.client.receiving_video, args=(self.IP,))
                self.instructionThread = threading.Thread(target=self.receive_instruction, args=(self.IP,))
                self.videoThread.start()
                self.instructionThread.start()
                # self.face_thread = threading.Thread(target=self.client.face_recognition)
                # self.face_thread.start()
                self.Button_Connect.setText(Variables.InterfaceText.UI_DISCONNECT)
                # self.time_out.start(11000)
                self.timer_power.start(3000)
            else:
                try:
                    Thread.stop_thread(self.videoThread)
                except:
                    pass
                try:
                    Thread.stop_thread(self.instructionThread)
                except:
                    pass
                self.client.tcp_flag = False
                self.client.turn_off_client()
                self.Button_Connect.setText('Connect')
                self.timer_power.stop()
        except Exception as e:
            print(e)

    # Slider
    def speed(self):
        self.client.move_speed = str(self.slider_speed.value())
        self.label_speed.setText(str(self.slider_speed.value()))

    def set_z_height(self):
        self.label_Z.setText(str(self.slider_Z.value()))
        self.position()

    def set_roll(self):
        self.label_roll.setText(str(self.slider_roll.value()))
        self.attitude()

    def show_calibration_window(self):
        command = Variables.Commands.CMD_CALIBRATION
        self.client.send_data(command)
        self.CalibrationWindow = CalibrationWindow(self.client)
        self.CalibrationWindow.setWindowModality(Qt.ApplicationModal)
        self.CalibrationWindow.show()

    def show_led_window(self):
        try:
            self.LedWindow = LedWindow(self.client)
            self.LedWindow.setWindowModality(Qt.ApplicationModal)
            self.LedWindow.show()
        except Exception as e:
            print(e)

    def show_face_window(self):
        try:
            self.FaceWindow = FaceWindow(self.client)
            self.FaceWindow.setWindowModality(Qt.ApplicationModal)
            self.FaceWindow.show()
            self.client.face_id = True
        except Exception as e:
            print(e)


class FaceWindow(QMainWindow, Ui_Face):
    def __init__(self, client):
        super(FaceWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(Variables.Settings.FILEPATH_WINDOW_ICON))
        self.Button_Read_Face.clicked.connect(self.read_face)
        self.client = client
        self.face_image = ''
        self.photoCount = 0
        self.timeout = 0
        self.name = ''
        self.readFaceFlag = False
        # Timer
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.face_detection)
        self.timer1.start(10)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.face_photo)

    def closeEvent(self, event):
        self.timer1.stop()
        self.client.face_id = False

    def read_face(self):
        try:
            if self.Button_Read_Face.text() == "Read Face":
                self.Button_Read_Face.setText("Reading")
                self.timer2.start(10)
                self.timeout = time.time()
            else:
                self.timer2.stop()
                if self.photoCount != 0:
                    self.Button_Read_Face.setText("Waiting ")
                    self.client.face.trainImage()
                    QMessageBox.information(self, "Message", "success", QMessageBox.Yes)
                self.Button_Read_Face.setText("Read Face")
                self.name = self.lineEdit.setText("")
                # wtf self.photoCount == 0
        except Exception as e:
            print(e)

    def face_photo(self):
        try:
            if self.photoCount == 30:
                # wtf self.photoCount == 0
                self.timer2.stop()
                self.Button_Read_Face.setText("Waiting ")
                self.client.face.trainImage()
                QMessageBox.information(self, "Message", "success", QMessageBox.Yes)
                self.Button_Read_Face.setText("Read Face")
                self.name = self.lineEdit.setText("")
            if len(self.face_image) > 0:
                self.name = self.lineEdit.text()
                if len(self.name) > 0:
                    height, width = self.face_image.shape[:2]
                    QImg = QImage(self.face_image.data.tobytes(), width, height, 3 * width, QImage.Format_RGB888)
                    self.label_photo.setPixmap(QPixmap.fromImage(QImg))
                    second = int(time.time() - self.timeout)
                    if second > 1:
                        self.save_face_photo()
                        self.timeout = time.time()
                    else:
                        self.Button_Read_Face.setText(
                            "Reading " + str(1 - second) + "S   " + str(self.photoCount) + "/30")
                    self.face_image = ''
                else:
                    QMessageBox.information(self, "Message", "Please enter your name", QMessageBox.Yes)
                    self.timer2.stop()
                    self.Button_Read_Face.setText("Read Face")
        except Exception as e:
            print(e)

    def save_face_photo(self):
        cv2.cvtColor(self.face_image, cv2.COLOR_BGR2RGB, self.face_image)
        cv2.imwrite('Face/' + str(len(self.client.face.name)) + '.jpg', self.face_image)
        self.client.face.name.append([str(len(self.client.face.name)), str(self.name)])
        self.client.face.Save_to_txt(self.client.face.name, 'Face/name')
        self.client.face.name = self.client.face.Read_from_txt('Face/name')
        self.photoCount += 1
        self.Button_Read_Face.setText("Reading " + str(0) + " S " + str(self.photoCount) + "/30")

    def face_detection(self):
        try:
            if len(self.client.image) > 0:
                gray = cv2.cvtColor(self.client.image, cv2.COLOR_BGR2GRAY)
                faces = self.client.face.detector.detectMultiScale(gray, 1.2, 5)
                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        self.face_image = self.client.image[y - 5:y + h + 5, x - 5:x + w + 5]
                        cv2.rectangle(self.client.image, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 2)
                if self.client.video_flag is False:
                    height, width, bytes_per_component = self.client.image.shape
                    cv2.cvtColor(self.client.image, cv2.COLOR_BGR2RGB, self.client.image)
                    QImg = QImage(self.client.image.data.tobytes(), width, height, 3 * width, QImage.Format_RGB888)
                    self.label_video.setPixmap(QPixmap.fromImage(QImg))
                    self.client.video_flag = True
        except Exception as e:
            print(e)


class CalibrationWindow(QMainWindow, Ui_calibration):
    def __init__(self, client):
        super(CalibrationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(Variables.Settings.FILEPATH_WINDOW_ICON))
        self.label_picture.setScaledContents(True)
        self.label_picture.setPixmap(QPixmap(Variables.Settings.FILEPATH_WINDOW_CALIBRATION))
        self.point = self.Read_from_txt(Variables.Settings.FILEPATH_POINT)
        self.set_point(self.point)
        self.client = client
        self.leg = 'one'
        self.x = 0
        self.y = 0
        self.z = 0
        self.radioButton_one.setChecked(True)
        self.radioButton_one.toggled.connect(lambda: self.leg_point(self.radioButton_one))
        self.radioButton_two.setChecked(False)
        self.radioButton_two.toggled.connect(lambda: self.leg_point(self.radioButton_two))
        self.radioButton_three.setChecked(False)
        self.radioButton_three.toggled.connect(lambda: self.leg_point(self.radioButton_three))
        self.radioButton_four.setChecked(False)
        self.radioButton_four.toggled.connect(lambda: self.leg_point(self.radioButton_four))
        self.radioButton_five.setChecked(False)
        self.radioButton_five.toggled.connect(lambda: self.leg_point(self.radioButton_five))
        self.radioButton_six.setChecked(False)
        self.radioButton_six.toggled.connect(lambda: self.leg_point(self.radioButton_six))
        self.Button_Save.clicked.connect(self.save)
        self.Button_X1.clicked.connect(self.move_x_plus)
        self.Button_X2.clicked.connect(self.move_x_minus)
        self.Button_Y1.clicked.connect(self.move_y_plus)
        self.Button_Y2.clicked.connect(self.move_y_minus)
        self.Button_Z1.clicked.connect(self.move_z_plus)
        self.Button_Z2.clicked.connect(self.move_z_minus)

    def move_x_plus(self):
        self.get_point()
        self.x += 1
        command = Variables.Commands.CMD_CALIBRATION + '#' + self.leg + '#' + str(self.x) + '#' + str(self.y) + '#' + str(self.z)
        self.client.send_data(command)
        self.set_point()

    def move_x_minus(self):
        self.get_point()
        self.x -= 1
        command = Variables.Commands.CMD_CALIBRATION + '#' + self.leg + '#' + str(self.x) + '#' + str(self.y) + '#' + str(self.z)
        self.client.send_data(command)
        self.set_point()

    def move_y_plus(self):
        self.get_point()
        self.y += 1
        command = Variables.Commands.CMD_CALIBRATION + '#' + self.leg + '#' + str(self.x) + '#' + str(self.y) + '#' + str(self.z)
        self.client.send_data(command)
        self.set_point()

    def move_y_minus(self):
        self.get_point()
        self.y -= 1
        command = Variables.Commands.CMD_CALIBRATION + '#' + self.leg + '#' + str(self.x) + '#' + str(self.y) + '#' + str(self.z)
        self.client.send_data(command)
        self.set_point()

    def move_z_plus(self):
        self.get_point()
        self.z += 1
        command = Variables.Commands.CMD_CALIBRATION + '#' + self.leg + '#' + str(self.x) + '#' + str(self.y) + '#' + str(self.z)
        self.client.send_data(command)
        self.set_point()

    def move_z_minus(self):
        self.get_point()
        self.z -= 1
        command = Variables.Commands.CMD_CALIBRATION + '#' + self.leg + '#' + str(self.x) + '#' + str(self.y) + '#' + str(self.z)
        self.client.send_data(command)
        self.set_point()

    def set_point(self, data=None):
        if data == None:
            if self.leg == "one":
                self.one_x.setText(str(self.x))
                self.one_y.setText(str(self.y))
                self.one_z.setText(str(self.z))
                self.point[0][0] = self.x
                self.point[0][1] = self.y
                self.point[0][2] = self.z
            elif self.leg == "two":
                self.two_x.setText(str(self.x))
                self.two_y.setText(str(self.y))
                self.two_z.setText(str(self.z))
                self.point[1][0] = self.x
                self.point[1][1] = self.y
                self.point[1][2] = self.z
            elif self.leg == "three":
                self.three_x.setText(str(self.x))
                self.three_y.setText(str(self.y))
                self.three_z.setText(str(self.z))
                self.point[2][0] = self.x
                self.point[2][1] = self.y
                self.point[2][2] = self.z
            elif self.leg == "four":
                self.four_x.setText(str(self.x))
                self.four_y.setText(str(self.y))
                self.four_z.setText(str(self.z))
                self.point[3][0] = self.x
                self.point[3][1] = self.y
                self.point[3][2] = self.z
            elif self.leg == "five":
                self.five_x.setText(str(self.x))
                self.five_y.setText(str(self.y))
                self.five_z.setText(str(self.z))
                self.point[4][0] = self.x
                self.point[4][1] = self.y
                self.point[4][2] = self.z
            elif self.leg == "six":
                self.six_x.setText(str(self.x))
                self.six_y.setText(str(self.y))
                self.six_z.setText(str(self.z))
                self.point[5][0] = self.x
                self.point[5][1] = self.y
                self.point[5][2] = self.z
        else:
            self.one_x.setText(str(data[0][0]))
            self.one_y.setText(str(data[0][1]))
            self.one_z.setText(str(data[0][2]))
            self.two_x.setText(str(data[1][0]))
            self.two_y.setText(str(data[1][1]))
            self.two_z.setText(str(data[1][2]))
            self.three_x.setText(str(data[2][0]))
            self.three_y.setText(str(data[2][1]))
            self.three_z.setText(str(data[2][2]))
            self.four_x.setText(str(data[3][0]))
            self.four_y.setText(str(data[3][1]))
            self.four_z.setText(str(data[3][2]))
            self.five_x.setText(str(data[4][0]))
            self.five_y.setText(str(data[4][1]))
            self.five_z.setText(str(data[4][2]))
            self.six_x.setText(str(data[5][0]))
            self.six_y.setText(str(data[5][1]))
            self.six_z.setText(str(data[5][2]))

    def get_point(self):
        if self.leg == "one":
            self.x = int(self.one_x.text())
            self.y = int(self.one_y.text())
            self.z = int(self.one_z.text())
        elif self.leg == "two":
            self.x = int(self.two_x.text())
            self.y = int(self.two_y.text())
            self.z = int(self.two_z.text())
        elif self.leg == "three":
            self.x = int(self.three_x.text())
            self.y = int(self.three_y.text())
            self.z = int(self.three_z.text())
        elif self.leg == "four":
            self.x = int(self.four_x.text())
            self.y = int(self.four_y.text())
            self.z = int(self.four_z.text())
        elif self.leg == "five":
            self.x = int(self.five_x.text())
            self.y = int(self.five_y.text())
            self.z = int(self.five_z.text())
        elif self.leg == "six":
            self.x = int(self.six_x.text())
            self.y = int(self.six_y.text())
            self.z = int(self.six_z.text())

    def save(self):
        command = Variables.Commands.CMD_CALIBRATION + '#' + 'save'
        self.client.send_data(command)

        self.point[0][0] = self.one_x.text()
        self.point[0][1] = self.one_y.text()
        self.point[0][2] = self.one_z.text()

        self.point[1][0] = self.two_x.text()
        self.point[1][1] = self.two_y.text()
        self.point[1][2] = self.two_z.text()

        self.point[2][0] = self.three_x.text()
        self.point[2][1] = self.three_y.text()
        self.point[2][2] = self.three_z.text()

        self.point[3][0] = self.four_x.text()
        self.point[3][1] = self.four_y.text()
        self.point[3][2] = self.four_z.text()

        self.Save_to_txt(self.point, 'point')
        reply = QMessageBox.information(self,
                                        "Message",
                                        "Saved successfully",
                                        QMessageBox.Yes)
        # print(command)

    def Read_from_txt(self, filename):
        file1 = open(filename, "r")
        list_row = file1.readlines()
        list_source = []
        print(type(list_source))
        for i in range(len(list_row)):
            column_list = list_row[i].strip().split("\t")
            list_source.append(column_list)
        print(type(list_source))
        for i in range(len(list_source)):
            for j in range(len(list_source[i])):
                list_source[i][j] = int(list_source[i][j])
        print(type(list_source))
        print(list_source)
        file1.close()
        return list_source

    def Save_to_txt(self, list, filename):
        file2 = open(filename + '.txt', 'w')
        for i in range(len(list)):
            for j in range(len(list[i])):
                file2.write(str(list[i][j]))
                file2.write('\t')
            file2.write('\n')
        file2.close()

    def leg_point(self, leg):
        if leg.text() == "One":
            if leg.isChecked() == True:
                self.leg = "one"
        elif leg.text() == "Two":
            if leg.isChecked() == True:
                self.leg = "two"
        elif leg.text() == "Three":
            if leg.isChecked() == True:
                self.leg = "three"
        elif leg.text() == "Four":
            if leg.isChecked() == True:
                self.leg = "four"
        elif leg.text() == "Five":
            if leg.isChecked() == True:
                self.leg = "five"
        elif leg.text() == "Six":
            if leg.isChecked() == True:
                self.leg = "six"


class ColorDialog(QtWidgets.QColorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOptions(self.options() | QtWidgets.QColorDialog.DontUseNativeDialog)
        for children in self.findChildren(QtWidgets.QWidget):
            classname = children.metaObject().className()
            if classname not in ("QColorPicker", "QColorLuminancePicker"):
                children.hide()


class LedWindow(QMainWindow, Ui_led):
    def __init__(self, client):
        super(LedWindow, self).__init__()
        self.setupUi(self)
        self.client = client
        self.setWindowIcon(QIcon(Variables.Settings.FILEPATH_WINDOW_ICON))
        self.hsl = [0, 0, 1]
        self.rgb = [0, 0, 0]
        self.dial_color.setRange(0, 360)
        self.dial_color.setNotchesVisible(True)
        self.dial_color.setWrapping(True)
        self.dial_color.setPageStep(10)
        self.dial_color.setNotchTarget(10)
        self.dial_color.valueChanged.connect(self.dialValueChanged)
        composite_2f = lambda f, g: lambda t: g(f(t))
        self.hsl_to_rgb255 = composite_2f(self.hsl_to_rgb01, self.rgb01_to_rgb255)
        self.hsl_to_rgbhex = composite_2f(self.hsl_to_rgb255, self.rgb255_to_rgbhex)
        self.rgb255_to_hsl = composite_2f(self.rgb255_to_rgb01, self.rgb01_to_hsl)
        self.rgbhex_to_hsl = composite_2f(self.rgbhex_to_rgb255, self.rgb255_to_hsl)
        self.colordialog = ColorDialog()
        self.colordialog.currentColorChanged.connect(self.onCurrentColorChanged)
        lay = QtWidgets.QVBoxLayout(self.widget)
        lay.addWidget(self.colordialog, alignment=QtCore.Qt.AlignCenter)

        self.pushButtonLightsOut.clicked.connect(self.lights_out)
        self.radioButtonOne.setChecked(True)
        self.radioButtonOne.toggled.connect(lambda: self.led_mode(self.radioButtonOne))
        self.radioButtonTwo.setChecked(False)
        self.radioButtonTwo.toggled.connect(lambda: self.led_mode(self.radioButtonTwo))
        self.radioButtonThree.setChecked(False)
        self.radioButtonThree.toggled.connect(lambda: self.led_mode(self.radioButtonThree))
        self.radioButtonFour.setChecked(False)
        self.radioButtonFour.toggled.connect(lambda: self.led_mode(self.radioButtonFour))
        self.radioButtonFive.setChecked(False)
        self.radioButtonFive.toggled.connect(lambda: self.led_mode(self.radioButtonFive))

    def lights_out(self):
        command = Variables.Commands.CMD_LED_MOD + '#' + '0'
        self.client.send_data(command)

    def led_mode(self, index):
        if index.text() == "Mode 1":
            if index.isChecked():
                command = Variables.Commands.CMD_LED_MOD + '#' + '1'
                self.client.send_data(command)
        elif index.text() == "Mode 2":
            if index.isChecked():
                command = Variables.Commands.CMD_LED_MOD + '#' + '2'
                self.client.send_data(command)
        elif index.text() == "Mode 3":
            if index.isChecked():
                command = Variables.Commands.CMD_LED_MOD + '#' + '3'
                self.client.send_data(command)
        elif index.text() == "Mode 4":
            if index.isChecked():
                command = Variables.Commands.CMD_LED_MOD + '#' + '4'
                self.client.send_data(command)
        elif index.text() == "Mode 5":
            if index.isChecked():
                command = Variables.Commands.CMD_LED_MOD + '#' + '5'
                self.client.send_data(command)

    def mode1Color(self):
        if (self.radioButtonOne.isChecked() == True) or (self.radioButtonThree.isChecked() == True):
            command = Variables.Commands.CMD_LED + '#' + str(self.rgb[0]) + '#' + str(self.rgb[1]) + '#' + str(self.rgb[2])
            self.client.send_data(command)

    def onCurrentColorChanged(self, color):
        try:
            self.rgb = self.rgbhex_to_rgb255(color.name())
            self.hsl = self.rgb255_to_hsl(self.rgb)
            self.changeHSLText()
            self.changeRGBText()
            self.mode1Color()
            self.update()
        except Exception as e:
            print(e)

    def paintEvent(self, e):
        try:
            qp = QPainter()
            qp.begin(self)
            brush = QBrush(QColor(self.rgb[0], self.rgb[1], self.rgb[2]))
            qp.setBrush(brush)
            qp.drawRect(20, 10, 80, 30)
            qp.end()
        except Exception as e:
            print(e)

    def dialValueChanged(self):
        try:
            self.lineEdit_H.setText(str(self.dial_color.value()))
            self.changeHSL()
            self.hex = self.hsl_to_rgbhex((self.hsl[0], self.hsl[1], self.hsl[2]))
            self.rgb = self.rgbhex_to_rgb255(self.hex)
            self.changeRGBText()
            self.mode1Color()
            self.update()
        except Exception as e:
            print(e)

    def changeHSL(self):
        self.hsl[0] = float(self.lineEdit_H.text())
        self.hsl[1] = float(self.lineEdit_S.text())
        self.hsl[2] = float(self.lineEdit_L.text())

    def changeHSLText(self):
        self.lineEdit_H.setText(str(int(self.hsl[0])))
        self.lineEdit_S.setText(str(round(self.hsl[1], 1)))
        self.lineEdit_L.setText(str(round(self.hsl[2], 1)))

    def changeRGBText(self):
        self.lineEdit_R.setText(str(self.rgb[0]))
        self.lineEdit_G.setText(str(self.rgb[1]))
        self.lineEdit_B.setText(str(self.rgb[2]))

    @staticmethod
    def rgb255_to_rgbhex(rgb: np.array) -> str:
        f = lambda n: 0 if n < 0 else 255 if n > 255 else int(n)
        return '#%02x%02x%02x' % (f(rgb[0]), f(rgb[1]), f(rgb[2]))

    @staticmethod
    def rgbhex_to_rgb255(rgb_hex: str) -> np.array:
        if rgb_hex[0] == '#':
            rgb_hex = rgb_hex[1:]
        r = int(rgb_hex[0:2], 16)
        g = int(rgb_hex[2:4], 16)
        b = int(rgb_hex[4:6], 16)
        return np.array((r, g, b))

    @staticmethod
    def rgb01_to_rgb255(rgb: np.array) -> np.array:
        return rgb * 255

    @staticmethod
    def rgb255_to_rgb01(rgb: np.array) -> np.array:
        return rgb / 255

    @staticmethod
    def rgb01_to_hsl(rgb: np.array) -> np.array:
        r, g, b = rgb
        lmin = min(r, g, b)
        lmax = max(r, g, b)
        if lmax == lmin:
            h = 0
        elif lmin == b:
            h = 60 + 60 * (g - r) / (lmax - lmin)
        elif lmin == r:
            h = 180 + 60 * (b - g) / (lmax - lmin)
        elif lmin == g:
            h = 300 + 60 * (r - b) / (lmax - lmin)
        else:
            h = 0
        s = lmax - lmin
        l = (lmax + lmin) / 2
        hsl = np.array((h, s, l))
        return hsl

    @staticmethod
    def hsl_to_rgb01(hsl: np.array) -> np.array:
        h, s, l = hsl
        lmin = l - s / 2
        lmax = l + s / 2
        ldif = lmax - lmin
        if h < 60:
            r, g, b = lmax, lmin + ldif * (0 + h) / 60, lmin
        elif h < 120:
            r, g, b = lmin + ldif * (120 - h) / 60, lmax, lmin
        elif h < 180:
            r, g, b = lmin, lmax, lmin + ldif * (h - 120) / 60
        elif h < 240:
            r, g, b = lmin, lmin + ldif * (240 - h) / 60, lmax
        elif h < 300:
            r, g, b = lmin + ldif * (h - 240) / 60, lmin, lmax
        else:
            r, g, b = lmax, lmin, lmin + ldif * (360 - h) / 60
        rgb = np.array((r, g, b))
        return rgb


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
