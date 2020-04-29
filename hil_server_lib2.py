# Created by Weina Mao on 04/04/2020
from comtypes.client import CreateObject
import time
from niveristand.legacy import NIVeriStand
from niveristand.clientapi import DoubleValue, BooleanValue, ChannelReference
from niveristand.library import wait, multitask, nivs_yield, stop_task, task
from niveristand import nivs_rt_sequence
from address import *


def launch_veristand():
    NIVeriStand.LaunchNIVeriStand()
    print('wait for Veristand Launching')
    time.sleep(15)
    print('Wait end')
    # workspace = NIVeriStand.Workspace2('localhost')
    # return workspace


def deploy_veristand(system_definition_file_path):
    """Customize each system definition file for B, C, D, E Truck"""
    workspace = NIVeriStand.Workspace2('localhost')
    path = system_definition_file_path
    workspace.ConnectToSystem(path, True, 60000)
    return workspace


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
    ReAX_GearA_Disable_chan = ChannelReference(
        'Targets/TruckSim_TTC580/User Channels/NI-XNET/VCAN-B/ReAX_GearA (486535187)/ReAX_GearA (486535187) Disable')
    ReAX_GearB_Disable_chan = ChannelReference(
        'Targets/TruckSim_TTC580/User Channels/NI-XNET/VCAN-B/ReAX_GearB (486535443)/ReAX_GearB (486535443) Disable')
    Power_On_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/DAQ/PXI1Slot2/Digital Output/port0/Power on')

    SystemStatus_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Server CAN/Incoming/Single-Point'
        '/SystemStatus(69785)/SystemStatus')
    Autonomous_Drive_chan = ChannelReference('Targets/TruckSim_TTC580/Hardware/Chassis/DAQ'
                                             '/PXI1Slot2/Digital Output/port0/Autonomous Drive')
    MODE_TRANS_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Simulation Models/Models/trucksim_LVRT/Inports/MODE_TRANS')

    with multitask() as mt:
        @task(mt)
        def enter_30():

            ReAX_GearA_Disable_chan.value = 0
            ReAX_GearB_Disable_chan.value = 0
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

@nivs_rt_sequence
def enter_30():
    error_status = BooleanValue(True)
    # channel references
    Power_On_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/DAQ/PXI1Slot2/Digital Output/port0/Power on')
    ReAX_GearA_Disable_chan = ChannelReference(
        'Targets/TruckSim_TTC580/User Channels/NI-XNET/VCAN-B/ReAX_GearA (486535187)/ReAX_GearA (486535187) Disable')
    ReAX_GearB_Disable_chan = ChannelReference(
        'Targets/TruckSim_TTC580/User Channels/NI-XNET/VCAN-B/ReAX_GearB (486535443)/ReAX_GearB (486535443) Disable')
    RemoteAccelPedalPos_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Vehicle CAN/Incoming/Single-Point/EEC2_CMD (418382648)/RemoteAccelPedalPos')
    XBRBrakeDemand_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Vehicle CAN/Incoming/Single-Point/XBR (201591804)/XBRBrakeDemand')
    XPRPReq_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/VCAN-B/Incoming/Single-Point/XPRCmd (218060344)/XPRPReq')
    Autonomous_Drive_chan = ChannelReference('Targets/TruckSim_TTC580/Hardware/Chassis/DAQ'
                                             '/PXI1Slot2/Digital Output/port0/Autonomous Drive')
    MODE_TRANS_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Simulation Models/Models/trucksim_LVRT/Inports/MODE_TRANS')
    SystemStatus_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Server CAN/Incoming/Single-Point/SystemStatus (69785)/SystemStatus')

    # *** end initialization

    # *** steps
    # start sending lateral drive
    ReAX_GearA_Disable_chan.value = 0
    ReAX_GearB_Disable_chan.value = 0

    # power on VCU
    Power_On_chan.value = 1

    wait(DoubleValue(3))
    if SystemStatus_chan.value != 25:
        error_status.value = False
    Autonomous_Drive_chan.value = 1
    wait(DoubleValue(1))
    Autonomous_Drive_chan.value = 0
    if SystemStatus_chan.value != 30:
        error_status.value = False
    MODE_TRANS_chan.value = 18
    return error_status.value


@nivs_rt_sequence
def self_check():
    # *** initialization
    # variables
    TestPass = BooleanValue(True)
    # channel references
    Power_On_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/DAQ/PXI1Slot2/Digital Output/port0/Power on')
    ReAX_GearA_Disable_chan = ChannelReference(
        'Targets/TruckSim_TTC580/User Channels/NI-XNET/VCAN-B/ReAX_GearA (486535187)/ReAX_GearA (486535187) Disable')
    ReAX_GearB_Disable_chan = ChannelReference(
        'Targets/TruckSim_TTC580/User Channels/NI-XNET/VCAN-B/ReAX_GearB (486535443)/ReAX_GearB (486535443) Disable')
    RemoteAccelPedalPos_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Vehicle CAN/Incoming/Single-Point/EEC2_CMD (418382648)/RemoteAccelPedalPos')
    XBRBrakeDemand_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Vehicle CAN/Incoming/Single-Point/XBR (201591804)/XBRBrakeDemand')
    XPRPReq_chan = ChannelReference(
        'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/VCAN-B/Incoming/Single-Point/XPRCmd (218060344)/XPRPReq')

    # *** end initialization

    # *** steps
    # start sending lateral drive
    ReAX_GearA_Disable_chan.value = 0
    ReAX_GearB_Disable_chan.value = 0

    # power on VCU
    Power_On_chan.value = 1

    wait(DoubleValue(3))
    # check RemoteAccelPedalPos, XBRBrakeDemand and XPRPReq has been zeroed
    if RemoteAccelPedalPos_chan.value != 0 or \
            -0.02 > XBRBrakeDemand_chan.value or XBRBrakeDemand_chan.value > 0.02 or \
            XPRPReq_chan.value != 0:
        TestPass.value = False

    # wait for relays to switch on
    wait(DoubleValue(5))
    # *** end steps
    return TestPass.value


if __name__ == '__main__':
    try:
        print(power_supply(13))
        # launch_veristand()
        # result_workspace = deploy_veristand("C:\\Users\\Public\\"
        #                                   "Documents\\National Instruments\\NI VeriStand 2018"
        #                                   "\\Examples\\Stimulus Profile\\Engine Demo\\Engine Demo.nivssdf")
        result_workspace = deploy_veristand("C:\\NI\\TTC580_TruckSim_Tusimple_C\\"
                                           "TTC580_TruckSim_Tusimple_C.nivssdf")
        print("deploy Success")
        print(enter_30())
    finally:
        disconnect_veristand(result_workspace)