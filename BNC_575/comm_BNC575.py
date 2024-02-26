import serial
import time
import serial.tools.list_ports

class communicate_BNC575():
    # End of line is b'\r\n'

    def __init__(self, comPort):
        self.error_list = {}
        self.error_list['1']: 'Incorrect prefix, i.e. no colon or * to start command.'
        self.error_list['2']: 'Missing command keyword.'
        self.error_list['3']: 'Invalid command keyword.'
        self.error_list['4']: 'Missing parameter.'
        self.error_list['5']: 'Invalid parameter.'
        self.error_list['6']: 'Query only, command needs a question mark.'
        self.error_list['7']: 'Invalid query, command does not have a query form.'
        self.error_list['8']: 'Command unavailable in current system state.'

        self.success = False

        try:
            # Open connection
            self.ser = serial.Serial(port=comPort, baudrate=115200, timeout=1, write_timeout=1)

            # According to the manual, * sent in the boot-up phase may result in 
            # undesired lockup of the instrument. Implement a short wait to try
            # to alleviate this.
            time.sleep(1)

            # Check connected to BNC box
            self.ser.write(b'*IDN?\r\n')
            self.ser.flush()
            response = self.ser.read_until(expected=b'\r\n').decode().split(',')

            # Make sure the model matches
            if response[0] != 'BNC' and response[1][:3] != '575':
                print('BNC pulse generator not recognised')
                return

        except serial.serialutil.SerialTimeoutException:
            # BNC box not found
            return

        # Close the connection
        self.ser.close()

        self.success = True

    def open_connection(self):
        self.ser.open()

    def close_connection(self):
        self.ser.close()

    def set_channel_state(self, channel, new_state):
        self.ser.write(bytes(f':PULSE{channel}:STATE {new_state}\r\n', 'ascii'))
        self.ser.flush()
        response = self.ser.read_until(expected=b'\r\n').decode()

        # Check the command was processed
        if response != 'ok\r\n':
            print(self.error_list[response[1]])
            return -1

        time.sleep(0.1)

        # Confirm the state is now correct
        self.ser.write(bytes(f':PULSE{channel}:STATE?\r\n', 'ascii'))
        self.ser.flush()
        response = self.ser.read_until(expected=b'\r\n').decode()

        if response[0] != str(new_state):
            print(f'Error when setting state of channel {channel} to state {new_state}.')
            return -1

        return 0

    def set_channel_delay(self, channel, delay):
        self.ser.write(bytes(f':PULSE{channel}:DELAY {delay}\r\n', 'ascii'))
        self.ser.flush()
        response = self.ser.read_until(expected=b'\r\n').decode()

        # Check the command was processed
        if response != 'ok\r\n':
            print(self.error_list[response[1]])
            return -1

        return 0
	

    def set_channel_width(self, channel, width):
        pass

    def set_sync_channel(self, channel, sync_channel):
        pass

def get_com_port_list():
    # May have to try opening and closing all the ports if it does
    # not find the ports from the USB adaptor (just catch exceptions
    # up to perhaps 256)
    return [p.device for p in serial.tools.list_ports.comports()]

if __name__ == '__main__':
    bncBox = communicate_BNC575('COM12')

    bncBox.open_connection()

    #bncBox.set_channel_state(1,0)
    #time.sleep(5)
    #bncBox.set_channel_state(1,1)

    print(bncBox.set_channel_delay(1,0.05))
    
    bncBox.close_connection()