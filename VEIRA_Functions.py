from PyQt6.QtCore import *
from BNC_575.comm_BNC575 import communicate_BNC575, get_com_port_list

class veira_settings(QObject):
    run = pyqtSignal()

    def __init__(self, main_variables):
        super().__init__()

        # Read the appropriate widgets from the GUI into the class
        self.sigCycles = main_variables.sigAcqCycles
        self.bgCycles = main_variables.bgAcqCycles
        self.sigDelay = main_variables.sigDelay
        self.bgDelay = main_variables.bgDelay
        self.repeats = main_variables.VEIRARepeats
        self.currentRun = main_variables.currentVEIRARun
        self.delayChannelCombo = main_variables.delayChannelCombo

        self.comPort = main_variables.bncComPort
        self.connectPortButton = main_variables.bncConnect

        self.cycles_to_run = main_variables._n_of_frames
        self.startVEIRA = main_variables._buttonVEIRA
        self.startButton = main_variables._button

        # Read all the COM ports currently in use
        self.populate_com_port_list('COM12')

        # BNC pulse box is not connected
        self.bnc_connected = False

        # Initialise the run array
        self.run_array = []

        self.current_run_type = 'None'

    def populate_com_port_list(self, default='None'):
        com_port_list = get_com_port_list()

        # Reset the list
        self.comPort.clear()
        self.comPort.addItems(com_port_list)

        # Set the value to the default value if it exists
        if default in com_port_list:
            self.comPort.setCurrentIndex(com_port_list.index(default))


    def connect_bnc(self):
        self.bnc = communicate_BNC575(self.comPort.currentText())
        if self.bnc.success:
            self.startVEIRA.setEnabled(self.startButton.isEnabled())
            self.bnc_connected = True
            self.connectPortButton.setText('Connected')

        
    def reset_run(self):
        self.run_array = []
        self.current_run_type = 'None'


    def populate_run_array(self, camera_running):
        # Clear the run array and stop the camera if it already running
        if camera_running:
            self.reset_run()
            self.run.emit()
            return

        # Get the required data from the GUI
        sig_cycle_count = self.sigCycles.value()
        bg_cycle_count = self.bgCycles.value()

        # Delay needs to be in s, so convert from us
        sig_delay = self.sigDelay.value() / 1000000
        bg_delay = self.bgDelay.value() / 1000000

        # The channels need to be indexed 1, rather than indexed 0
        delay_channel = self.delayChannelCombo.currentIndex() + 1

        # Redefine and populate a run array
        self.run_array = []
        for i in range(self.repeats.value()):
            # SIGNAL
            self.run_array.append({})
            self.run_array[-1]['Label'] = f'Currently running: Signal (repeat {i+1})'
            self.run_array[-1]['Cycles'] = sig_cycle_count
            self.run_array[-1]['Delay'] = sig_delay
            self.run_array[-1]['Delay channel'] = delay_channel
            self.run_array[-1]['Type'] = 'Signal'

            # BACKGROUND
            self.run_array.append({})
            self.run_array[-1]['Label'] = f'Currently running: Background (repeat {i+1})'
            self.run_array[-1]['Cycles'] = bg_cycle_count
            self.run_array[-1]['Delay'] = bg_delay
            self.run_array[-1]['Delay channel'] = delay_channel
            self.run_array[-1]['Type'] = 'Background'

        self.run_next()

    def run_next(self):
        try:
            next_run = self.run_array.pop(0)
            self.current_run_type = next_run['Type']
        except IndexError:
            # No runs left
            return

        # Set the delay
        self.bnc.open_connection()
        self.bnc.set_channel_delay(next_run['Delay channel'], next_run['Delay'])
        self.bnc.close_connection()

        # Set the number of acquisition cycles
        self.cycles_to_run.setValue(next_run['Cycles'])

        # Set the current run
        self.currentRun.setText(next_run['Label'])

        self.run.emit()