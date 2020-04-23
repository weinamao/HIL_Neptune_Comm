import os
from EngineDemo2 import *
from niveristand import run_py_as_rtseq
from niveristand.errors import RunError
from niveristand.legacy import NIVeriStand
import time

def mix_legacy_and_rtseq_run():
    """Combines the legacy API with Python real-time sequences to run a deterministic test."""
    # Ensures NI VeriStand is running.
    NIVeriStand.LaunchNIVeriStand()
    print('wait')
    time.sleep(10)
    print('Wait end')
    # Uses the ClientAPI interface to get a reference to Workspace2
    workspace = NIVeriStand.Workspace2("localhost")
    engine_demo_path = "C:\\Users\\Public\\Documents\\" \
                       "National Instruments\\NI VeriStand 2018\\Examples\\Stimulus Profile\\Engine Demo\\Engine Demo.nivssdf"
    # Deploys the system definition.
    workspace.ConnectToSystem(engine_demo_path, True, 60000)
    try:
        # Uses Python real-time sequences to run a test.
        # run_py_as_rtseq(run_engine_demo)
        engine_demo_basic(BooleanValue(True), DoubleValue(2500))
        print("Test Success")
    except RunError as e:
        print("Test Failed: %d -  %s" % (int(e.error.error_code), e.error.message))
    finally:
        # You can now disconnect from the system, so the next test can run.
        workspace.DisconnectFromSystem('', True)


if __name__ == '__main__':
    mix_legacy_and_rtseq_run()