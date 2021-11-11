# -*- coding: utf-8 -*-

import logging
import cv2.cv2 as cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import Variables


class Functions:
    def __init__(self, window):
        logging.basicConfig(format=Variables.Settings.LOG_FORMAT, level=Variables.Settings.LOG_LEVEL)
        self.win = window
        self.client = window.client
        self.timer_sonic = QTimer(window)
        self.timer_sonic.timeout.connect(self.get_ultrasonic_data)
        self.timer_video = QTimer(window)
        self.timer_video.timeout.connect(self.refresh_image)

    def motors_status(self):
        """Control servo motors activation
        Check the button text and toggle the value of it. If the buzzer button is hold on, change the value of the
        button text and send the command
        """
        try:
            if self.win.Button_Relax.text() == Variables.InterfaceText.UI_MOTORS_ON:
                self.win.Button_Relax.setText(Variables.InterfaceText.UI_MOTORS_OFF)
                command = Variables.Commands.CMD_MOTORS_ON
                logging.info("%s: %s" % (Variables.InterfaceLog.LOG_MOTORS_OFF, command))
            else:
                self.win.Button_Relax.setText(Variables.InterfaceText.UI_MOTORS_ON)
                command = Variables.Commands.CMD_MOTORS_OFF
                logging.info("%s: %s" % (Variables.InterfaceLog.LOG_MOTORS_ON, command))
            self.client.send_data(command)
        except Exception as e:
            logging.error(e)

    def buzzer(self):
        """Control buzzer activation
        Check the button text and toggle the value of it. If the buzzer button is hold on, change the value of the
        button text and send the command.
        """
        try:
            if self.win.Button_Buzzer.text() == Variables.InterfaceText.UI_BUZZER_OFF:
                self.win.Button_Buzzer.setText(Variables.InterfaceText.UI_BUZZER_ON)
                command = Variables.Commands.CMD_BUZZER_ON
                logging.info("%s: %s" % (Variables.InterfaceLog.LOG_BUZZER_ON, command))
            else:
                self.win.Button_Buzzer.setText(Variables.InterfaceText.UI_BUZZER_OFF)
                command = Variables.Commands.CMD_BUZZER_OFF
                logging.info("%s: %s" % (Variables.InterfaceLog.LOG_BUZZER_OFF, command))
            self.client.send_data(command)
        except Exception as e:
            logging.error(e)

    def ultrasonic(self):
        """Control ultrasonic sensor timer activation
        Check the button text and toggle the value of it. If the ultrasonic button is turned on, change the value of the
        button and start the timer_sonic with the set interval to call for get_ultrasonic_data().
        """
        if self.win.Button_Sonic.text() == Variables.InterfaceText.UI_ULTRASONIC_OFF:
            self.win.Button_Sonic.setText(Variables.InterfaceText.UI_ULTRASONIC_ON)
            self.timer_sonic.start(Variables.Settings.ULTRASONIC_POLLING_INTERVAL_MS)
            logging.info(Variables.InterfaceLog.LOG_ULTRASONIC_ON)
        else:
            self.win.Button_Sonic.setText(Variables.InterfaceText.UI_ULTRASONIC_OFF)
            self.timer_sonic.stop()
            logging.info(Variables.InterfaceLog.LOG_ULTRASONIC_OFF)

    def get_ultrasonic_data(self):
        """Getter for ultrasonic data triggered by ultrasonic() timer
        Send the command
        """
        self.client.send_data(Variables.Commands.CMD_ULTRASONIC)
        logging.debug("%s: %s" % (Variables.InterfaceLog.LOG_ULTRASONIC_POLL, Variables.Commands.CMD_ULTRASONIC))

    def action_mode(self, mode):
        """Control action mode
        Check the button text and if it's checked then set the proper checked value for both action mode button and
        finally set the variable action_flag to which ever mode is chosen so the move function will move accordingly.
        """
        if mode.text() == Variables.InterfaceText.UI_ACTION_MODE_1:
            if mode.isChecked() is True:
                self.win.ButtonActionMode1.setChecked(True)
                self.win.ButtonActionMode2.setChecked(False)
                self.win.action_flag = 1
                logging.info(Variables.InterfaceLog.LOG_ACTION_MODE_1)
        elif mode.text() == Variables.InterfaceText.UI_ACTION_MODE_2:
            if mode.isChecked() is True:
                self.win.ButtonActionMode1.setChecked(False)
                self.win.ButtonActionMode2.setChecked(True)
                self.win.action_flag = 2
                logging.info(Variables.InterfaceLog.LOG_ACTION_MODE_2)

    def gait_mode(self, mode):
        """Control gait mode
        Check the button text and if it's checked then set the proper checked value for both gait mode button and
        finally set the variable gait_mode to which ever mode is chosen so the move function will move accordingly.
        Gait mode 1 is tripod (L1-L3-R2 then L2-R1-R3)
        Gait mode 2 is ripple
        """
        if mode.text() == Variables.InterfaceText.UI_GAIT_MODE_1:
            if mode.isChecked() is True:
                self.win.ButtonGaitMode1.setChecked(True)
                self.win.ButtonGaitMode2.setChecked(False)
                self.win.gait_flag = 1
                logging.info(Variables.InterfaceLog.LOG_ACTION_MODE_1)
        elif mode.text() == Variables.InterfaceText.UI_GAIT_MODE_2:
            if mode.isChecked() is True:
                self.win.ButtonGaitMode1.setChecked(False)
                self.win.ButtonGaitMode2.setChecked(True)
                self.win.gait_flag = 2
                logging.info(Variables.InterfaceLog.LOG_GAIT_MODE_2)

    def video(self):
        """Control video streaming activation
        Check the button text and toggle the value of it. If the video button is turned on, change the value of the
        button and start the timer_sonic with the set interval to call for refresh_image().
        """
        if self.win.Button_Video.text() == Variables.InterfaceText.UI_VIDEO_OFF:
            self.timer_video.start(Variables.Settings.VIDEO_POLLING_INTERVAL_MS)
            self.win.Button_Video.setText(Variables.InterfaceText.UI_VIDEO_ON)
            logging.info(Variables.InterfaceLog.LOG_VIDEO_ON)
        else:
            self.timer_video.stop()
            self.win.Button_Video.setText(Variables.InterfaceText.UI_VIDEO_OFF)
            logging.info(Variables.InterfaceLog.LOG_VIDEO_OFF)

    def refresh_image(self):
        """Trigger an image refresh of the camera
        Convert the image received in self.image by Client.receiving_video() method to an image in the UI.
        """
        if self.client.video_flag is False:
            height, width, bytes_per_component = self.client.image.shape
            cv2.cvtColor(self.client.image, cv2.COLOR_BGR2RGB, self.client.image)
            new_image = QImage(self.client.image.data.tobytes(), width, height, 3 * width, QImage.Format_RGB888)
            self.win.Video.setPixmap(QPixmap.fromImage(new_image))
            self.client.video_flag = True

    def head_move_vertical(self):
        """Control head movement vertically
        Read the slider value, set the associated text and send the command with the angle
        """
        try:
            angle = str(self.win.slider_head.value())
            self.win.label_head.setText(angle)
            command = Variables.Commands.CMD_HEAD_VERT + angle
            self.client.send_data(command)
            logging.info("%s %s" % (Variables.InterfaceLog.LOG_HEAD_VERT, angle))
        except Exception as e:
            logging.error(e)

    def head_move_horizontal(self):
        """Control head movement horizontally
        Read the slider value, set the associated text and send the command with the angle
        """
        try:
            angle = str(180 - self.win.slider_head_1.value())
            self.win.label_head_1.setText(angle)
            command = Variables.Commands.CMD_HEAD_HORI + angle
            self.client.send_data(command)
            logging.info("%s %s" % (Variables.InterfaceLog.LOG_HEAD_HORI, angle))
        except Exception as e:
            logging.error(e)

    def balance(self):
        """Control the balance function activation
        Check the button text and toggle the value of it then send the command.
        """
        if self.win.Button_IMU.text() == Variables.InterfaceText.UI_BALANCE_OFF:
            command = Variables.Commands.CMD_BALANCE_ON
            self.win.Button_IMU.setText(Variables.InterfaceText.UI_BALANCE_ON)
            logging.info(Variables.InterfaceLog.LOG_BALANCE_ON)
        else:
            command = Variables.Commands.CMD_BALANCE_OFF
            self.win.Button_IMU.setText(Variables.InterfaceText.UI_BALANCE_OFF)
            logging.info(Variables.InterfaceLog.LOG_BALANCE_OFF)
        self.client.send_data(command)
