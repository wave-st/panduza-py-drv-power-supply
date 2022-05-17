import time
import serial
from loguru import logger
from panduza_platform import MetaDriverPsu

class DriverRnd320_KA005P(MetaDriverPsu):
    """ Driver to manage the HM7044 power supply
    """

    ###########################################################################
    ###########################################################################
    
    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "rnd320-ka3005p",
            "info": { "type": "psu", "version": "1.0" },
            "settings": {
                "serial_port" : "Serial port on which the power supply is connected",
            }
        }
        
    ###########################################################################
    ###########################################################################

    def setup(self, tree):
        """ FROM MetaDriver
        """
        # Initialize variables
        self.serial_port = tree["settings"]["serial_port"]

        # 
        self.__serial = serial.Serial(self.serial_port, 9600, timeout=1)

        # Register commands
        self.register_command("state/set", self.__set_state)
        self.register_command("volts/set", self.__set_volts)
        self.register_command("amps/set", self.__set_amps)

    ###########################################################################
    ###########################################################################

    def on_start(self):
        #
        # self.push_io_value(self.value)
        pass

    ###########################################################################
    ###########################################################################
        
    def loop(self):
        """ FROM MetaDriver
        """
        # if self._loop % 2 == 0:
        #     self.__push_attribute_value()
        #     self.__push_attribute_direction()
        # self._loop += 1
        # time.sleep(0.5)
        return False

    ###########################################################################
    ###########################################################################

    def __set_state(self, payload):
        """
        """
        req = self.payload_to_dict(payload)
        req_state = req["state"]
        # Update enable
        self.state=req_state
        if self.state == "on":
            cmd = bytearray(b'OUT1')
        elif self.state == "off":
            cmd = bytearray(b'OUT0')
        self.__serial.write(cmd)
        self.push_psu_enable(self.state)
        logger.info(f"new state :" + str(payload))

    ###########################################################################
    ###########################################################################

    def __set_volts(self, payload):
        """
        """
        req = self.payload_to_dict(payload)
        req_volts = req["volts"]
        self.volts = req_volts
        cmd = bytearray(b'VSET1:') + bytearray(self.volts, encoding='utf8')
        self.__serial.write(cmd)
        # Update enable
        self.push_psu_volts(self.volts)
        logger.info(f"new volts :" + str(payload))

    ###########################################################################
    ###########################################################################

    def __set_amps(self, payload):
        """
        """
        pass