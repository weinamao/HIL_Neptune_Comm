from niveristand.legacy import NIVeriStand
from niveristand import nivs_rt_sequence
from niveristand.clientapi import DoubleValue, BooleanValue
from address import *
from niveristand.library import wait
from niveristand.library import multitask, nivs_yield, stop_task, task
import time
from comtypes.client import CreateObject


def launch_veristand():
    NIVeriStand.LaunchNIVeriStand()
    print('wait for Veristand Launching')
    time.sleep(10)
    print('Wait end')
    workspace = NIVeriStand.Workspace2('localhost')
    return workspace


def deploy_veristand(workspace, system_definition_file_path):
    """Customize each system definition file for B, C, D, E Truck"""
    path = system_definition_file_path
    workspace.ConnectToSystem(path, True, 60000)


def disconnect_veristand(workspace):
    workspace.DisconnectFromSystem('', True)


def set_power_supply_voltage(voltage=12.6, current=5):
    ps = CreateObject("LambdaGenPS.LambdaGenPS")
    ps.Initialize("COM3", True, True,'DriverSetup=SerialAddress=6, BaudRate=9600')
    ps.Output.VoltageLimit = voltage
    ps.Output.CurrentLimit = current
    ps.Output.Enabled = True
    time.sleep(2)
    mes_vol = ps.Output.MeasureVoltage()
    ps.Close()
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
            set_power_supply_voltage(13, 8)
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
    print(set_power_supply_voltage(5, 5))
    # # step 1: launch Veristand
    # result_workspace = launch_veristand()
    # # step 2: deploy Veristand system definition file
    # deploy_veristand(result_workspace,"C:\\Users\\Public\\"
    #                                   "Documents\\National Instruments\\NI VeriStand 2018"
    #                                   "\\Examples\\Stimulus Profile\\Engine Demo\\Engine Demo.nivssdf")
    # print("deploy Success")
    # # step 3: write test steps
    # set_val(ReAX_GearA_Disable_chan, 0)
    # set_val(ReAX_GearB_Disable_chan, 0)
    # set_power_supply_voltage(13, 8)
    # check_val(SystemStatus_chan, 25)
    # power_on_button()
    # autonomous_on_button()
    # check_val(SystemStatus_chan, 30)
    # set_val(MODE_TRANS_chan, 18)
    # # step 4: undeploy Veristand
    # disconnect_veristand(result_workspace)