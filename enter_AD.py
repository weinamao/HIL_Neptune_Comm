from hil_server_lib import *



if __name__ == '__main__':
    # step 1: launch Veristand
    result_workspace = launch_veristand()
    # step 2: deploy Veristand system definition file
    deploy_veristand(result_workspace,"C:\\Users\\Public\\"                                               
                                      "Documents\\National Instruments\\NI VeriStand 2018"                
                                      "\\Examples\\Stimulus Profile\\Engine Demo\\Engine Demo.nivssdf")
    print("deploy Success")
    # step 3: write test steps

    set_val(ReAX_GearA_Disable_chan, 0)
    set_val(ReAX_GearB_Disable_chan, 0)
    set_power_supply_voltage(13, 8)
    check_val(SystemStatus_chan, 25)
    power_on_button()
    autonomous_on_button()
    set_val(MODE_TRANS_chan, 18)
    # step 4: undeploy Veristand
    disconnect_veristand(result_workspace)