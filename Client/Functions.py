#encoding : UTF-8

import logging

from Command import COMMAND as cmd
from Translation import TRANSLATION as txt
from Variable import VARIABLE as var

class Functions:
    def __init__(self, MyWindow):
        logging.basicConfig(format=var.LOG_FORMAT,
                            level=logging.DEBUG)
        self.win = MyWindow
        self.client = MyWindow.client
        pass

    """
    Control servo motors activation
    """
    def motors_status(self):
        try:
            if self.win.Button_Relax.text() == txt.UI_MOTORS_ON:
                self.win.Button_Relax.setText(txt.UI_MOTORS_OFF)
                command = cmd.CMD_MOTORS_ON
                logging.info(">>> %s: %s" % (txt.LOG_TXT_MOTORS_OFF , command))
            else:
                self.win.Button_Relax.setText(txt.UI_MOTORS_ON)
                command = cmd.CMD_MOTORS_OFF
                logging.info(">>> %s: %s" % (txt.LOG_TXT_MOTORS_ON , command))
            self.client.send_data(command)
        except Exception as e:
            logging.error(e)

    """
    Control buzzer activation
    """
    def buzzer(self):
        try:
            if self.win.Button_Buzzer.text() == txt.UI_BUZZER_OFF:
                self.win.Button_Buzzer.setText(txt.UI_BUZZER_ON)
                command = cmd.CMD_BUZZER_ON
                logging.info(">>> %s: %s" % (txt.LOG_BUZZER_ON , command))
            else:
                self.win.Button_Buzzer.setText(txt.UI_BUZZER_OFF)
                command = cmd.CMD_BUZZER_OFF
                logging.info(">>> %s: %s" % (txt.LOG_BUZZER_OFF , command))
            self.client.send_data(command)
        except Exception as e:
            logging.error(e)