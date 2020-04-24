import win32com.client

class Trucksimcontrol():
    def __init__(self):
        self.h = win32com.client.Dispatch("TruckSim.Application")

    def open_trucksim(self, truck_type="C"):
        self.h.GoHome()
        # Select Truck Model
        self.h.Gotolibrary('', 'NI RT w/ tusimple truck', 'Tusimple SD NI RT Simulation')
        # Select Truck Type
        self.h.BlueLink('#BlueLink12', 'Models: Transfer to NI-RT Target', 'For TTC580 use Type ' + truck_type,
                   'VeriStand: Tusimple')

    def trucksim_nirt_open(self):
        # Click Open button
        self.h.RunButtonClick(1)

    def trucksim_nirt_send(self):
        # Click Send button
        self.h.RunButtonClick(2)

    def change_trailer_weight(self, trailer_weight='8000'):
        self.h.GoHome()
        self.h.Gotolibrary('Vehicle: Loaded Combination', 'Truck C 6-30 Sleeper Tractor w/o Trailer Tusimple',
                   'TS 3A - Tractors')
        self.h.Gotolibrary('Vehicle: Trailer with 2 Axles', '2A Trailer (Short) w/ Hitch #TuSimple', 'TS Van / Container Trailers')
        self.h.Gotolibrary('Vehicle: Trailer Sprung Mass', '2A Trailer (Short) #TuSimple', '2A Trailer')
        self.h.Yellow('M_SU', trailer_weight)


if __name__== "__main__":
    TruckSim = Trucksimcontrol()
    TruckSim.change_trailer_weight()