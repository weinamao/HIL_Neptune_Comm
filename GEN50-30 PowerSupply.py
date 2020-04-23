from comtypes.client import CreateObject


def power_supply(input_voltage=6):
    PS2 = CreateObject("LambdaGenPS.LambdaGenPS")
    PS2.Initialize("COM3", True, True, "DriverSetup=SerialAddress=6,BaudRate=9600")
    PS2.Output.VoltageLimit = input_voltage
    PS2.Output.CurrentLimit = 1
    PS2.Output.Enabled = True
    PS2.Close()
    return PS2.Output.MeasureVoltage()


if __name__ == "__main__":
    power_supply(3)