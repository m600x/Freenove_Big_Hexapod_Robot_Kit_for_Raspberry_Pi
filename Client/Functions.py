#encoding : UTF-8

class Functions(Client):

    def relax(self):
        try:
            if self.Button_Relax.text() == "Motors ON":
                self.Button_Relax.setText("Motors OFF")
                command = cmd.CMD_SERVOPOWER + "#" + "0" + '\n'
                logging.info(">>> %s: %s" % (txt.TXT_MOTORS_OFF , command))
            else:
                self.Button_Relax.setText("Motors ON")
                command = cmd.CMD_SERVOPOWER + "#" + "1" + '\n'
                print(">>> Powering on motors: %s" % command)
            self.client.send_data(command)
        except Exception as e:
            print(e)