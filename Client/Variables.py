import logging


class Settings:
    FILEPATH_IP = "assets/IP.txt"
    FILEPATH_POINT = "assets/point.txt"
    FILEPATH_WINDOW_ICON = "assets/Picture/logo_Mini.png"
    FILEPATH_WINDOW_CAMERA = "assets/Picture/Spider_client.png"
    FILEPATH_WINDOW_CALIBRATION = "assets/Picture/Spider_calibration.png"
    LOG_FORMAT = "[%(asctime)s][ %(levelname)-8s ][ %(module)s:%(funcName)s:%(lineno)s ] %(message)s"
    LOG_LEVEL = logging.INFO
    CONN_PORT_COMMANDS = 5002
    CONN_PORT_VIDEO = 8002
    HEAD_VERTICAL_MIN = 50
    HEAD_VERTICAL_MAX = 180
    HEAD_VERTICAL_STEP = 1
    HEAD_VERTICAL_DEFAULT = 90
    HEAD_HORIZONTAL_MIN = 0
    HEAD_HORIZONTAL_MAX = 180
    HEAD_HORIZONTAL_STEP = 1
    HEAD_HORIZONTAL_DEFAULT = 90
    SPEED_MIN = 2
    SPEED_MAX = 10
    SPEED_STEP = 1
    SPEED_DEFAULT = 10
    ROLL_MIN = -15
    ROLL_MAX = 15
    ROLL_STEP = 1
    ROLL_DEFAULT = 0
    Z_HEIGHT_MIN = -20
    Z_HEIGHT_MAX = 50
    Z_HEIGHT_STEP = 1
    Z_HEIGHT_DEFAULT = 0
    ULTRASONIC_POLLING_INTERVAL_MS = 1000
    VIDEO_POLLING_INTERVAL_MS = 10
#    _MIN =
#    _MAX =
#    _STEP =
#    _DEFAULT =


class Commands:
    CMD_MOTORS_ON = "CMD_SERVOPOWER#1"
    CMD_MOTORS_OFF = "CMD_SERVOPOWER#0"
    CMD_BUZZER_ON = "CMD_BUZZER#1"
    CMD_BUZZER_OFF = "CMD_BUZZER#0"
    CMD_ULTRASONIC = "CMD_SONIC"
    CMD_HEAD_VERT = "CMD_HEAD#0#"
    CMD_HEAD_HORI = "CMD_HEAD#1#"
    CMD_BALANCE_ON = "CMD_BALANCE#1"
    CMD_BALANCE_OFF = "CMD_BALANCE#0"

    CMD_MOVE = "CMD_MOVE"
    CMD_LED_MOD = "CMD_LED_MOD"
    CMD_LED = "CMD_LED"
    CMD_HEAD = "CMD_HEAD"
    CMD_BALANCE = "CMD_BALANCE"
    CMD_ATTITUDE = "CMD_ATTITUDE"
    CMD_POSITION = "CMD_POSITION"
    CMD_RELAX = "CMD_RELAX"
    CMD_POWER = "CMD_POWER"
    CMD_CALIBRATION = "CMD_CALIBRATION"
    CMD_CAMERA = "CMD_CAMERA"


class InterfaceText:
    UI_CONNECT = "Connect"
    UI_DISCONNECT = "Disconnect"
    UI_BUZZER_ON = "Buzzing"
    UI_BUZZER_OFF = "Buzzer"
    UI_MOTORS_ON = "Motors ON"
    UI_MOTORS_OFF = "Motors OFF"
    UI_ULTRASONIC_ON = "Ultrasonic ON"
    UI_ULTRASONIC_OFF = "Ultrasonic OFF"
    UI_ACTION_MODE_1 = "Action Mode 1"
    UI_ACTION_MODE_2 = "Action Mode 2"
    UI_GAIT_MODE_1 = "Gait Mode 1"
    UI_GAIT_MODE_2 = "Gait Mode 2"
    UI_VIDEO_ON = "Close video"
    UI_VIDEO_OFF = "Open video"
    UI_BALANCE_ON = "Close"
    UI_BALANCE_OFF = "Balance"


class InterfaceLog:
    LOG_BUZZER_ON = "Activating buzzer"
    LOG_BUZZER_OFF = "Deactivating buzzer"
    LOG_MOTORS_ON = "Powering motors on"
    LOG_MOTORS_OFF = "Powering motors off"
    LOG_ULTRASONIC_ON = "Activating ultrasonic sensor"
    LOG_ULTRASONIC_OFF = "Deactivating ultrasonic sensor"
    LOG_ULTRASONIC_POLL = "Polling ultrasonic data"
    LOG_ACTION_MODE_1 = "Change action mode to 1 (movement)"
    LOG_ACTION_MODE_2 = "Change action mode to 2 (turn)"
    LOG_GAIT_MODE_1 = "Change gait mode to 1 (3x3)"
    LOG_GAIT_MODE_2 = "Change gait mode to 2 (1b1)"
    LOG_VIDEO_ON = "Start video streaming"
    LOG_VIDEO_OFF = "Stop video streaming"
    LOG_HEAD_VERT = "Head - Move vertically to "
    LOG_HEAD_HORI = "Head - Move horizontally to "
    LOG_BALANCE_ON = "Balance mode turned on"
    LOG_BALANCE_OFF = "Balance mode turned off"
