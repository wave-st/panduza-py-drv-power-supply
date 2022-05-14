import time
import serial
from loguru import logger
from pza_platform import MetaDriver

class DriverHm7044(MetaDriver):
    """ Driver to manage the HM7044 power supply
    """

    ###########################################################################
    ###########################################################################
    
    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "psu_hm7044",
            "info": { "type": "power_supply", "version": "1.0" },
            "settings": {
                "serial_port" : "Serial port on which the power supply is connected",
                "channel" : "Channel number that must be driven by this interfaces [1,2,3,4]"
            }
        }
        
    ###########################################################################
    ###########################################################################

    def setup(self, tree):
        """ FROM MetaDriver
        """
        # Initialize variables
        self.serial_port = tree["settings"]["serial_port"]
        self.channel = tree["settings"]["channel"]

        # 
        # self.__serial = serial.Serial(self.serial_port, 9600, timeout=1)

        # Register commands
        self.register_command("enable/set", self.__set_enable)
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

    def __set_enable(self, payload):
        """
        """

        # message_on = bytearray(b'EN\r\n')
        # read_v = bytearray(b'\r\n')
        # ser.write(message_on)

    #     # Parse request
    #     req = self.payload_to_dict(payload)
    #     req_value = req["value"]
    #     self.value=req_value

    #     try:
    #         path = "/sys/class/gpio/gpio%s/value" % self.id
    #         f = open(path, "w")         
    #         # Update value
    #         f.write(str(self.value))
    #         self.push_io_value(self.value)
    #         # log
    #         logger.info(f"new value : {self.value}")

    #         f.close()
    #     except IOError as e:
    #         # mogger.error("Unable to set value %s to GPIO %s (%s) | %s", str(val), self.id, path, repr(e))
        pass

    ###########################################################################
    ###########################################################################

    def __set_volts(self, payload):
        """
        """
    #     # Parse request
    #     req = self.payload_to_dict(payload)
    #     req_direction = req["direction"]
    #     # Update direction
    #     self.direction=req_direction
    #     # log
    #     logger.info(f"new direction : {self.direction}")

    #     try:
    #         f = open("/sys/class/gpio/gpio%s/direction" % self.id, "w")
    #         f.write(self.direction)
    #         self.push_io_direction(self.direction)
    #         f.close()
    #     except IOError:
    #         # mogger.error("Unable to export set value")
        pass

    ###########################################################################
    ###########################################################################

    def __set_amps(self, payload):
        """
        """

        pass
    

    # ###########################################################################
    # ###########################################################################

    # def __push_attribute_value(self):
    #     """ To read and push value attribute of the gpio
    #     """
    #     if self.direction == 'out':
    #         return

    #     try:
    #         # Read the value from the driver
    #         f = open("/sys/class/gpio/gpio%s/value" % self.id, "r")
    #         value = f.read(1)
    #         f.close()
    #         value = int(value)

    #         # Push the attribute if it changed
    #         if self.value != value:
    #             self.value = value
    #             logger.debug("gpio '{}' value modified : {}", self.name, self.value)
    #             self.push_io_value(self.value)
    #     except IOError as e:
    #         logger.error("Unable to get value %s", repr(e))

    # ###########################################################################
    # ###########################################################################

    # def __push_attribute_direction(self):
    #     """ To read and push direction attribute of the gpio
    #     """
    #     try:
    #         # Read the direction from the driver
    #         f = open("/sys/class/gpio/gpio%s/direction" % self.id, "r")
    #         direction = f.read()
    #         f.close()
    #         direction = direction.rstrip("\n")

    #         # Push the attribute if it changed
    #         if self.direction != direction:
    #             self.direction = direction
    #             logger.debug("gpio '{}' direction modified : {}", self.name, self.direction)
    #             self.push_io_direction(self.direction)
    #     except IOError:
    #         logger.error("Unable to get direction %s", repr(e))



