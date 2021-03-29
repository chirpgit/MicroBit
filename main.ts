bluetooth.onUartDataReceived(serial.delimiters(Delimiters.Dollar), function () {
    if (蓝牙开关) {
        蓝牙命令字符 = bluetooth.uartReadUntil(serial.delimiters(Delimiters.Dollar))
        命令类型 = startbit.startbit_analyzeBluetoothCmd(蓝牙命令字符)
        if (命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.VERSION)) {
            bluetooth.uartWriteString("CMD|0A|81|$")
        }
        if (命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.ULTRASONIC)) {
            bluetooth.uartWriteString(startbit.startbit_convertUltrasonic(startbit.startbit_ultrasonic(startbit.startbit_ultrasonicPort.port2)))
        }
        if (命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.TEMPERATURE)) {
            bluetooth.uartWriteString(startbit.startbit_convertTemperature(input.temperature()))
        }
        if (命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.LIGHT)) {
            bluetooth.uartWriteString(startbit.startbit_convertLight(input.lightLevel()))
        }
        if (命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.RGB_LIGHT)) {
            startbit.startbit_setPixelRGBArgs(StartbitLights.Light1, startbit.startbit_getArgs(蓝牙命令字符, 1))
            startbit.startbit_setPixelRGBArgs(StartbitLights.Light2, startbit.startbit_getArgs(蓝牙命令字符, 1))
            startbit.startbit_showLight()
        }
        if (命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.SERVO)) {
            舵机号 = startbit.startbit_getArgs(蓝牙命令字符, 1)
            舵机角度 = startbit.startbit_getArgs(蓝牙命令字符, 2)
            舵机运行时间 = startbit.startbit_getArgs(蓝牙命令字符, 3)
            if (舵机号 == 1) {
                startbit.setServo(startbit.startbit_servorange.range1, 舵机号, 舵机角度, 舵机运行时间)
            } else if (舵机号 == 2) {
                if (舵机角度 >= 95) {
                    舵机角度 = 95
                }
                if (舵机角度 <= 30) {
                    舵机角度 = 30
                }
                startbit.setServo(startbit.startbit_servorange.range1, 舵机号, 舵机角度, 舵机运行时间)
            } else if (舵机号 == 3) {
                if (舵机角度 >= 140) {
                    舵机角度 = 140
                }
                if (舵机角度 <= 85) {
                    舵机角度 = 85
                }
                startbit.setServo(startbit.startbit_servorange.range1, 舵机号, 舵机角度, 舵机运行时间)
            }
        }
        if (命令类型 == startbit.startbit_getBluetoothCmdtype(startbit.startbit_CmdType.CAR_RUN)) {
            行进命令类型 = startbit.startbit_getArgs(蓝牙命令字符, 1)
            if (行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.STOP)) {
                bluetooth.uartWriteString("CMD|01|00|$")
                startbit.startbit_setMotorSpeed(0, 0)
                basic.showLeds(`
                    . . . . .
                    . # . # .
                    . # . # .
                    . # . # .
                    . . . . .
                    `)
            }
            if (行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.GO_AHEAD)) {
                bluetooth.uartWriteString("CMD|01|01|$")
                startbit.startbit_setMotorSpeed(90, 90)
                basic.showLeds(`
                    . . # . .
                    . . # . .
                    # . # . #
                    . # # # .
                    . . # . .
                    `)
            }
            if (行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.GO_BACK)) {
                bluetooth.uartWriteString("CMD|01|02|$")
                startbit.startbit_setMotorSpeed(-90, -90)
                basic.showLeds(`
                    . . # . .
                    . # # # .
                    # . # . #
                    . . # . .
                    . . # . .
                    `)
            }
            if (行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.TURN_LEFT)) {
                bluetooth.uartWriteString("CMD|01|03|$")
                startbit.startbit_setMotorSpeed(90, -90)
                basic.showLeds(`
                    # . . . .
                    # . # . .
                    # . . # .
                    # # # # #
                    . . . # .
                    `)
            }
            if (行进命令类型 == startbit.startbit_getRunCarType(startbit.startbit_CarRunCmdType.TURN_RIGHT)) {
                bluetooth.uartWriteString("CMD|01|04|$")
                startbit.startbit_setMotorSpeed(-90, 90)
                basic.showLeds(`
                    . . . . #
                    . . # . #
                    . # . . #
                    # # # # #
                    . # . . .
                    `)
            }
        }
    }
})
input.onButtonPressed(Button.A, function () {
    蓝牙开关 = !(蓝牙开关)
    basic.showLeds(`
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        `)
})
let 行进命令类型 = 0
let 舵机运行时间 = 0
let 舵机角度 = 0
let 舵机号 = 0
let 命令类型 = 0
let 蓝牙命令字符 = ""
let 蓝牙开关 = false
startbit.startbit_Init()
蓝牙开关 = true
basic.showLeds(`
    . . # . .
    # . # # .
    . # # . .
    # . # # .
    . . # . .
    `)
basic.forever(function () {
    if (!(蓝牙开关)) {
        if (startbit.startbit_ultrasonic(startbit.startbit_ultrasonicPort.port1) > 10) {
            startbit.startbit_setMotorSpeed(90, 90)
        } else if (startbit.startbit_ultrasonic(startbit.startbit_ultrasonicPort.port1) < 5) {
            startbit.startbit_setMotorSpeed(-90, -90)
        } else {
            startbit.startbit_setMotorSpeed(0, 0)
        }
    }
})
