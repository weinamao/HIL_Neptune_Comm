from niveristand.clientapi import ChannelReference
Power_On_chan = ChannelReference(
    'Targets/TruckSim_TTC580/Hardware/Chassis/DAQ/PXI1Slot2/Digital Output/port0/Power on')
# ReAX_GearA_Disable_chan = ChannelReference(
#     'Targets/TruckSim_TTC580/User Channels/NI-XNET/VCAN-B/ReAX_GearA (486535187)/ReAX_GearA (486535187) Disable')
ReAX_GearB_Disable_chan = ChannelReference(
    'Targets/TruckSim_TTC580/User Channels/NI-XNET/VCAN-B/ReAX_GearB (486535443)/ReAX_GearB (486535443) Disable')
RemoteAccelPedalPos_chan = ChannelReference(
    'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Vehicle CAN/Incoming/Single-Point/EEC2_CMD (418382648)'
    '/RemoteAccelPedalPos')
XBRBrakeDemand_chan = ChannelReference(
    'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Vehicle CAN/Incoming/Single-Point/XBR (201591804)'
    '/XBRBrakeDemand')
XPRPReq_chan = ChannelReference(
    'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/VCAN-B/Incoming/Single-Point/XPRCmd (218060344)/XPRPReq')
SystemStatus_chan = ChannelReference(
    'Targets/TruckSim_TTC580/Hardware/Chassis/NI-XNET/CAN/Server CAN/Incoming/Single-Point'
    '/SystemStatus(69785)/SystemStatus')
Autonomous_Drive_chan = ChannelReference('Targets/TruckSim_TTC580/Hardware/Chassis/DAQ'
                                         '/PXI1Slot2/Digital Output/port0/Autonomous Drive')
MODE_TRANS_chan = ChannelReference('Targets/TruckSim_TTC580/Simulation Models/Models/trucksim_LVRT/Inports/MODE_TRANS')

# enginedemo
engine_power_chan = ChannelReference('Aliases/EnginePower')
desired_rpm_chan = ChannelReference('Aliases/DesiredRPM')
actual_rpm_chan = ChannelReference('Aliases/ActualRPM')
engine_temp_chan = ChannelReference('Aliases/EngineTemp')