from Jacob_Pump import Pump

Pump1 = Pump("COM6","11 PICO PLUS ELITE 3.0.6")

# Define a class that communicates the values from the GUI to the pumps when the GO button is pushed
class Backend:

    def __init__(self, gui):

        # Call in values from the GUI
        self.gui = gui

        # Set slider values to 0
        self.oldVal1 = 0
        self.curVal1 = 0

    def buttonPush(self):

        # Slide all the current slider values to the old slider values
        self.oldVal1 = self.curVal1

        # Set all current slider values equal to values from the GUI
        self.curVal1 = self.gui.c1.get()

        # Set the values for percent change in volume from each slider
        self.deltVal1 = self.curVal1 - self.oldVal1

        # Multiply by the max volume per channel and divide by 100 to get the absolute
        # change in volume for each channel
        self.deltVol1 = 0.01 * self.deltVal1 * float(self.gui.maxvol_entry.get())

        # Define other GUI parameters
        self.rate = float(self.gui.rate_entry.get())
        self.vol = float(self.gui.vol_entry.get())
        self.diam = float(self.gui.diam_entry.get())
        self.numPump = float(self.gui.varPump.get())

        # Print volume changes for each channel as a sanity check
        print(str(self.deltVol1), str(self.deltVol2), str(self.deltVol3))

        # Check that each pump is properly connected
        Pump1.check_pump("11 ELITE I/W Single 3.0.6")

        # Set the pump parameters for Pump 1
        Pump1.c_volume()
        Pump1.ci_volume()
        Pump1.cw_volume()
        Pump1.syringe_vol(str(self.vol))
        Pump1.syringe_diam(str(self.diam))
        Pump1.infuse_rate(str(self.rate), "ml/min")
        Pump1.withdraw_rate(str(self.rate), "ml/min")
        Pump1.target_volume(str(abs(self.deltVol1)), "ml")

        # Actuate each pump
        if self.deltVol1 < 0:
            Pump1.withdraw_pump()
        elif self.deltVol1 > 0:
            Pump1.infuse_pump()
        else:
            Pump1.stop_pump()
