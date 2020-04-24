# Created by Weina Mao on 04/04/2020
from comtypes.client import CreateObject
import time
from niveristand.legacy import NIVeriStand
from niveristand.clientapi import DoubleValue, BooleanValue
from niveristand.library import wait, multitask, nivs_yield, stop_task, task
from niveristand import nivs_rt_sequence
from address import *


def launch_veristand():
    NIVeriStand.LaunchNIVeriStand()
    print('wait for Veristand Launching')
    time.sleep(15)
    print('Wait end')
    workspace = NIVeriStand.Workspace2('localhost')
    return workspace


def deploy_veristand(workspace, system_definition_file_path):
    """Customize each system definition file for B, C, D, E Truck"""
    path = system_definition_file_path
    workspace.ConnectToSystem(path, True, 60000)


def disconnect_veristand(workspace):
    workspace.DisconnectFromSystem('', True)


def power_supply(input_voltage=6):
    ps2 = CreateObject("LambdaGenPS.LambdaGenPS")
    ps2.Initialize("COM3", True, True, "DriverSetup=SerialAddress=6,BaudRate=9600")
    ps2.Output.VoltageLimit = input_voltage
    ps2.Output.CurrentLimit = 5
    ps2.Output.Enabled = True
    time.sleep(2)
    mes_vol = ps2.Output.MeasureVoltage()
    ps2.Close()
    return mes_vol


@nivs_rt_sequence
def enter_autonomous():
    error_status = BooleanValue(False)
    enter_autonomous_complete = BooleanValue(False)
    enter_autonomous_succeeded = BooleanValue(False)

    with multitask() as mt:
        @task(mt)
        def enter_30():
            ReAX_GearA_Disable_chan.value = 0
            ReAX_GearB_Disable_chan.value = 0
            # Set power supply
            power_supply(13)
            # Power on button
            Power_On_chan.value = 1
            # Check System Status
            if SystemStatus_chan.value != 25:
                error_status.value = True
            # Push autonomous driving button
            Autonomous_Drive_chan.value = 1
            wait(DoubleValue(1))
            Autonomous_Drive_chan.value = 0
            # Check System Status
            if SystemStatus_chan.value != 30:
                error_status.value = True
            MODE_TRANS_chan.value = 18
            enter_autonomous_succeeded.value = True

        @task(mt)
        def monitor_error_status():
            while enter_autonomous_complete.value is False:
                if error_status.value:
                    stop_task(enter_30)
                    enter_autonomous_complete.value = True
                    enter_autonomous_succeeded.value = False
                nivs_yield()
    return enter_autonomous_succeeded.value


if __name__ == '__main__':
    print(power_supply(10))
    result_workspace = launch_veristand()
    deploy_veristand(result_workspace, "C:\\Users\\Public\\"
                                      "Documents\\National Instruments\\NI VeriStand 2018"
                                      "\\Examples\\Stimulus Profile\\Engine Demo\\Engine Demo.nivssdf")
    print("deploy Success")
    disconnect_veristand(result_workspace)