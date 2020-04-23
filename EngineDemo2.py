from niveristand import nivs_rt_sequence, NivsParam, realtimesequencetools
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue
from niveristand.library import wait

""" This module contains a basic example of how to create an RT sequence in Python.

This example mirrors the 'Engine Demo Basic' example that installs with VeriStand.
Open the 'Engine Demo Basic' stimulus profile to help you understand the following example.
"""


# You must mark RT sequences with the following decorator:
@nivs_rt_sequence
# You must also specify parameter data types, default values, and whether to pass parameters by value or by reference.
@NivsParam('engine_power', BooleanValue(0), NivsParam.BY_REF)
@NivsParam('desired_rpm', DoubleValue(0), NivsParam.BY_REF)
def engine_demo_basic(engine_power, desired_rpm):
    """Turn on the engine, set the desired_rpm to the passed value for 20 seconds, and shut down the engine.

    You must access parameters through their ".value" property.
    """
    # You can access a channel with a ChannelReference
    engine_power_chan = ChannelReference('Aliases/EnginePower')
    desired_rpm_chan = ChannelReference('Aliases/DesiredRPM')
    engine_power_chan.value = engine_power.value
    desired_rpm_chan.value = desired_rpm.value
    wait(DoubleValue(20))
    engine_power_chan.value = False
    desired_rpm_chan.value = 0


if __name__ == '__main__':
    engine_demo_basic(BooleanValue(True), DoubleValue(2500))
    print('Finished non-deterministic')

