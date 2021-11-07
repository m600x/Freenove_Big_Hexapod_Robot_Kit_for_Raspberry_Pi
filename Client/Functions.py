# -*- coding: utf-8 -*-

import logging
from PyQt5.QtCore import QTimer
import Command
import Translation
import Variable


class Functions:
    def __init__(self, MyWindow):
        logging.basicConfig(format=Variable.VARIABLE.LOG_FORMAT, level=logging.DEBUG)
        self.win = MyWindow
        self.client = MyWindow.client
        self.timer_sonic = QTimer(MyWindow)
        self.timer_sonic.timeout.connect(self.get_ultrasonic_data)

    def motors_status(self):
        """Control servo motors activation
        Check the button text and toggle the value of it. If the buzzer button is hold on, change the value of the
        button text and send the command
        """
        try:
            if self.win.Button_Relax.text() == Translation.TRANSLATION.UI_MOTORS_ON:
                self.win.Button_Relax.setText(Translation.TRANSLATION.UI_MOTORS_OFF)
                command = Command.COMMAND.CMD_MOTORS_ON
                logging.info("%s: %s" % (Translation.TRANSLATION.LOG_MOTORS_OFF, command))
            else:
                self.win.Button_Relax.setText(Translation.TRANSLATION.UI_MOTORS_ON)
                command = Command.COMMAND.CMD_MOTORS_OFF
                logging.info("%s: %s" % (Translation.TRANSLATION.LOG_MOTORS_ON, command))
            self.client.send_data(command)
        except Exception as e:
            logging.error(e)

    def buzzer(self):
        """Control buzzer activation
        Check the button text and toggle the value of it. If the buzzer button is hold on, change the value of the
        button text and send the command.
        """
        try:
            if self.win.Button_Buzzer.text() == Translation.TRANSLATION.UI_BUZZER_OFF:
                self.win.Button_Buzzer.setText(Translation.TRANSLATION.UI_BUZZER_ON)
                command = Command.COMMAND.CMD_BUZZER_ON
                logging.info("%s: %s" % (Translation.TRANSLATION.LOG_BUZZER_ON, command))
            else:
                self.win.Button_Buzzer.setText(Translation.TRANSLATION.UI_BUZZER_OFF)
                command = Command.COMMAND.CMD_BUZZER_OFF
                logging.info("%s: %s" % (Translation.TRANSLATION.LOG_BUZZER_OFF, command))
            self.client.send_data(command)
        except Exception as e:
            logging.error(e)

    def ultrasonic(self):
        """Control ultrasonic sensor timer activation
        Check the button text and toggle the value of it. If the ultrasonic button is turned on, change the value of the
        button and start the timer_sonic with the set interval to call for get_ultrasonic_data().
        """
        if self.win.Button_Sonic.text() == Translation.TRANSLATION.UI_ULTRASONIC_OFF:
            self.win.Button_Sonic.setText(Translation.TRANSLATION.UI_ULTRASONIC_ON)
            self.timer_sonic.start(Variable.VARIABLE.ULTRASONIC_POLLING_INTERVAL_MS)
            logging.info(Translation.TRANSLATION.LOG_ULTRASONIC_ON)
        else:
            self.win.Button_Sonic.setText(Translation.TRANSLATION.UI_ULTRASONIC_OFF)
            self.timer_sonic.stop()
            logging.info(Translation.TRANSLATION.LOG_ULTRASONIC_OFF)

    def get_ultrasonic_data(self):
        """Getter for ultrasonic data triggered by ultrasonic() timer
        Send the command
        """
        self.client.send_data(Command.COMMAND.CMD_ULTRASONIC)
        logging.debug(">>> %s: %s" % (Translation.TRANSLATION.LOG_ULTRASONIC_POLL, Command.COMMAND.CMD_ULTRASONIC))

    def action_mode(self, mode):
        """Control action mode
        Check the button text and if it's checked then set the proper checked value for both action mode button and
        finally set the variable action_flag to which ever mode is chosen so the move function will move accordingly.
        """
        if mode.text() == Translation.TRANSLATION.UI_ACTION_MODE_1:
            if mode.isChecked() is True:
                self.win.ButtonActionMode1.setChecked(True)
                self.win.ButtonActionMode2.setChecked(False)
                self.win.action_flag = 1
                logging.info(Translation.TRANSLATION.LOG_ACTION_MODE_1)
        elif mode.text() == Translation.TRANSLATION.UI_ACTION_MODE_2:
            if mode.isChecked() is True:
                self.win.ButtonActionMode1.setChecked(False)
                self.win.ButtonActionMode2.setChecked(True)
                self.win.action_flag = 2
                logging.info(Translation.TRANSLATION.LOG_ACTION_MODE_2)

    def gait_mode(self, mode):
        """Control gait mode
        Check the button text and if it's checked then set the proper checked value for both gait mode button and
        finally set the variable gait_mode to which ever mode is chosen so the move function will move accordingly.
        """
        if mode.text() == Translation.TRANSLATION.UI_GAIT_MODE_1:
            if mode.isChecked() is True:
                self.win.ButtonGaitMode1.setChecked(True)
                self.win.ButtonGaitMode2.setChecked(False)
                self.win.gait_flag = 1
                logging.info(Translation.TRANSLATION.LOG_ACTION_MODE_1)
        elif mode.text() == Translation.TRANSLATION.UI_GAIT_MODE_2:
            if mode.isChecked() is True:
                self.win.ButtonGaitMode1.setChecked(False)
                self.win.ButtonGaitMode2.setChecked(True)
                self.win.gait_flag = 2
                logging.info(Translation.TRANSLATION.LOG_GAIT_MODE_2)
