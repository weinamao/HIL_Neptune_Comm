from comtypes.client import CreateObject
import time


def power_supply(input_voltage=6):
    ps2 = CreateObject("LambdaGenPS.LambdaGenPS")
    ps2.Initialize("COM3", True, True, "DriverSetup=SerialAddress=6,BaudRate=9600")
    ps2.Output.VoltageLimit = input_voltage
    ps2.Output.CurrentLimit = 1
    ps2.Output.Enabled = True
    time.sleep(2)
    mes_vol = ps2.Output.MeasureVoltage()
    ps2.Close()
    return mes_vol


if __name__ == '__main__':
    print(power_supply(10))