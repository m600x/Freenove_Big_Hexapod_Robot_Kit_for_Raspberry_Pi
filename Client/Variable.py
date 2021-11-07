class VARIABLE:
    FILEPATH_IP = "IP.txt"
    FILEPATH_WINDOW_ICON = "Picture/logo_Mini.png"
    FILEPATH_WINDOW_CAMERA = "Picture/Spider_client.png"

    LOG_FORMAT = "[%(asctime)s][ %(levelname)-8s ][ %(module)s:%(funcName)s:%(lineno)s ] %(message)s"

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
    SPEED_DEFAULT = 8

    ROLL_MIN = -15
    ROLL_MAX = 15
    ROLL_STEP = 1
    ROLL_DEFAULT = 0

    Z_HEIGHT_MIN = -20
    Z_HEIGHT_MAX = 20
    Z_HEIGHT_STEP = 1
    Z_HEIGHT_DEFAULT = 0

#    _MIN = 
#    _MAX = 
#    _STEP = 
#    _DEFAULT = 
    def __init__(self):
        pass