'''
This library is used for communication with delay stages being integrated into the PyMMS software.
If a new class is added make sure to follow the function calls, see newport class, to ensure no code is broken.
'''
import sys
import os
from epics import caget,caput

#########################################################################################
# Class used for communicating with the Newport delay stage
#########################################################################################
class newport_delay_stage():
    '''
    Controls communication with Newport delay stages.\n
    If the name of the dll is different pass that when the function is called.\n
    Imported at the end of the script to prevent conflicts with PyQt library.\n
    Requires the pythonnet and serial libraries.
    '''

    def __init__(self, *args):
        self.hardware_id = 'EPICS'
        self.dls_files_present = True

    def get_com_ports(self):
        '''
        List the available devices on the computer.\n
        The Newport stage used in B2 has hardware ID PID=104D:3009\n
        If the hardware id is different, figure out which id belongs\n 
        to your stage and pass that variable to the class call.
        '''
        com_list = ['EPICS']
        return com_list

    def connect_stage(self):
        '''Connect to the delay stage by providing a COM port.'''
        return 1

    def get_position(self):
        '''
        Returns the position of the delay stage.
        TP returns a tuple, 0 index is error code, 1 index is the value
        '''
        return str(caget('XPS:DL'))
    
    def get_minimum_position(self):
        '''Get the minimum position of the delay stage (mm).'''
        return str(caget('XPS:DL.DLLM'))
    
    def get_maximum_position(self):
        '''Get the maximum position of the delay stage (mm).'''
        return str(caget('XPS:DL.DHLM'))
    
    def set_position(self,value):
        '''Set the position of the delay stage.'''
        caput('XPS:DL',value,wait=True)

    def set_velocity(self,value):
        '''Set the velocity.\n Maximum velocity is 300 mm/s'''
        caput('XPS:DL.VELO',value)

    def get_velocity(self):
        '''Get the velocity.'''
        return str(caget('XPS:DL.VELO'))
    
    def set_acceleration(self,value):
        '''Set the acceleration.'''
        caput('XPS:DL.ACCL',value)

    def get_acceleration(self):
        '''Get the acceleration.'''
        return str(caget('XPS:DL.ACCL'))

    def disconnect_stage(self):
        '''
        Disconnect from the delay stage
        '''
        pass
