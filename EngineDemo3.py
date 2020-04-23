from hil_server_lib import *
import time
from address import *


set_val(engine_power_chan, True)
set_val(desired_rpm_chan, 2500)
time.sleep(20)
set_val(engine_power_chan, False)
set_val(desired_rpm_chan, 0)