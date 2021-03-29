def on_uart_data_received():
    global 蓝牙命令字符, 命令类型, 舵机号, 舵机角度, 舵机运行时间, 行进命令类型
    if 蓝牙开关:
        蓝牙命令字符 = bluetooth.uart_read_until(serial.delimiters(Delimiters.DOLLAR))
        命令类型 = startbit.startbit_analyzeBluetoothCmd(蓝牙命令字符)
        if 命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.VERSION):
            bluetooth.uart_write_string("CMD|0A|81|$")
        if 命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.ULTRASONIC):
            bluetooth.uart_write_string(startbit.startbit_convertUltrasonic(startbit.startbit_ultrasonic(startbit.startbit_ultrasonicPort.PORT2)))
        if 命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.TEMPERATURE):
            bluetooth.uart_write_string(startbit.startbit_convertTemperature(input.temperature()))
        if 命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.LIGHT):
            bluetooth.uart_write_string(startbit.startbit_convertLight(input.light_level()))
        if 命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.RGB_LIGHT):
            startbit.startbit_setPixelRGBArgs(StartbitLights.LIGHT1, startbit.startbit_getArgs(蓝牙命令字符, 1))
            startbit.startbit_setPixelRGBArgs(StartbitLights.LIGHT2, startbit.startbit_getArgs(蓝牙命令字符, 1))
            startbit.startbit_showLight()
        if 命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.SERVO):
            舵机号 = startbit.startbit_getArgs(蓝牙命令字符, 1)
            舵机角度 = startbit.startbit_getArgs(蓝牙命令字符, 2)
            舵机运行时间 = startbit.startbit_getArgs(蓝牙命令字符, 3)
            if 舵机号 == 1:
                startbit.set_servo(startbit.startbit_servorange.RANGE1, 舵机号, 舵机角度, 舵机运行时间)
            elif 舵机号 == 2:
                if 舵机角度 >= 95:
                    舵机角度 = 95
                if 舵机角度 <= 30:
                    舵机角度 = 30
                startbit.set_servo(startbit.startbit_servorange.RANGE1, 舵机号, 舵机角度, 舵机运行时间)
            elif 舵机号 == 3:
                if 舵机角度 >= 140:
                    舵机角度 = 140
                if 舵机角度 <= 85:
                    舵机角度 = 85
                startbit.set_servo(startbit.startbit_servorange.RANGE1, 舵机号, 舵机角度, 舵机运行时间)
        if 命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.CAR_RUN):
            行进命令类型 = startbit.startbit_getArgs(蓝牙命令字符, 1)
            if 行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.STOP):
                bluetooth.uart_write_string("CMD|01|00|$")
                startbit.startbit_setMotorSpeed(0, 0)
                basic.show_leds("""
                    . . . . .
                    . # . # .
                    . # . # .
                    . # . # .
                    . . . . .
                    """)
            if 行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.GO_AHEAD):
                bluetooth.uart_write_string("CMD|01|01|$")
                startbit.startbit_setMotorSpeed(90, 90)
                basic.show_leds("""
                    . . # . .
                    . . # . .
                    # . # . #
                    . # # # .
                    . . # . .
                    """)
            if 行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.GO_BACK):
                bluetooth.uart_write_string("CMD|01|02|$")
                startbit.startbit_setMotorSpeed(-90, -90)
                basic.show_leds("""
                    . . # . .
                    . # # # .
                    # . # . #
                    . . # . .
                    . . # . .
                    """)
            if 行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.TURN_LEFT):
                bluetooth.uart_write_string("CMD|01|03|$")
                startbit.startbit_setMotorSpeed(90, -90)
                basic.show_leds("""
                    # . . . .
                    # . # . .
                    # . . # .
                    # # # # #
                    . . . # .
                    """)
            if 行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.TURN_RIGHT):
                bluetooth.uart_write_string("CMD|01|04|$")
                startbit.startbit_setMotorSpeed(-90, 90)
                basic.show_leds("""
                    . . . . #
                    . . # . #
                    . # . . #
                    # # # # #
                    . # . . .
                    """)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.DOLLAR), on_uart_data_received)

def on_button_pressed_a():
    global 蓝牙开关
    蓝牙开关 = not (蓝牙开关)
    basic.show_leds("""
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        """)
input.on_button_pressed(Button.A, on_button_pressed_a)

行进命令类型 = 0
舵机运行时间 = 0
舵机角度 = 0
舵机号 = 0
命令类型 = 0
蓝牙命令字符 = ""
蓝牙开关 = False
startbit.startbit_Init()
蓝牙开关 = True
basic.show_leds("""
    . . # . .
    # . # # .
    . # # . .
    # . # # .
    . . # . .
    """)

def on_forever():
    if not (蓝牙开关):
        if startbit.startbit_ultrasonic(startbit.startbit_ultrasonicPort.PORT1) > 10:
            startbit.startbit_setMotorSpeed(90, 90)
        elif startbit.startbit_ultrasonic(startbit.startbit_ultrasonicPort.PORT1) < 5:
            startbit.startbit_setMotorSpeed(-90, -90)
        else:
            startbit.startbit_setMotorSpeed(0, 0)
basic.forever(on_forever)
