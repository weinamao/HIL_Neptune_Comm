from hil_server_lib2 import *
from TruckSimControl import *


if __name__ == '__main__':
    # step 1: launch Veristand
    result_workspace = launch_veristand()
    # step 2 : open TruckSim (do not RUN)
    TruckSim_item = Trucksimcontrol
    TruckSim_item.open_trucksim()
    TruckSim_item.trucksim_nirt_open()
    time.sleep(3)
    TruckSim_item.trucksim_nirt_send()
    # step 3: deploy Veristand system definition file
    deploy_veristand(result_workspace,"C:\\Users\\Public\\"                                               
                                      "Documents\\National Instruments\\NI VeriStand 2018"                
                                      "\\Examples\\Stimulus Profile\\Engine Demo\\Engine Demo.nivssdf")
    print("deploy Success")
    # step 4: write test steps

    # step 5: undeploy Veristand
    disconnect_veristand(result_workspace)