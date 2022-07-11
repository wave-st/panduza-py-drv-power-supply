from asyncio import selector_events
import time
import serial
from loguru import logger
from panduza_platform import MetaDriverPsu
from threading import Lock

class DriverHm7044(MetaDriverPsu):
    """ Driver to manage the HM7044 power supply
    """
    PSU_SERIALS = {} # dictionnary used to track multiple channels

    ###########################################################################
    ###########################################################################
    
    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "psu_hm7044",
            "info": { "type": "psu", "version": "1.0" },
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

        # Initialize variables
        self.supported_settings = self.api_settings.copy()
        
        
        self.api_attributes["volts"]["max"] = 32
        self.api_attributes["volts"]["scale"] = 0.01

        self.api_attributes["amps"]["max"] = 3
        self.api_attributes["amps"]["scale"] = 0.001
        
        self.api_attributes["model_name"] = "HM7044"

        if "serial_port" not in tree["settings"]:
            logger.error("Setting serial_port is mandatory for this driver")
            return False

        if "channel" not in tree["settings"]:
            logger.error("Setting channel is mandatory for this driver")
            return False

        self.serial_port = tree["settings"]["serial_port"]
        self.channel = tree["settings"]["channel"]

        print("serial port ", end="")
        print(self.serial_port)

        print("channel ", end="")
        print(self.channel)

        if self.serial_port not in DriverHm7044.PSU_SERIALS : # no existing device, create entry
            DriverHm7044.PSU_SERIALS[self.serial_port] = {  "channel_list" : [self.channel],
                                                            "dev" : serial.Serial(),
                                                            "mutex" : Lock(),
                                                            "output_enabled" : []
                                                        }
            DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].port = self.serial_port
            DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].baudrate = 9600
            print(DriverHm7044.PSU_SERIALS[self.serial_port]["dev"])

        elif self.channel not in DriverHm7044.PSU_SERIALS[self.serial_port]["channel_list"] : # add channel to channel list
            DriverHm7044.PSU_SERIALS[self.serial_port]["channel_list"].append(self.channel)
        
        self.enable=False
        self.volts=0
        self.amps=0

        DriverHm7044.PSU_SERIALS[self.serial_port]["mutex"].acquire()
        if not DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].isOpen() :
            DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].open()
        DriverHm7044.PSU_SERIALS[self.serial_port]["mutex"].release()


        # Register commands
        self.register_command("state/set", self.__set_state)
        self.register_command("volts/set", self.__set_volts)
        self.register_command("amps/set", self.__set_amps)
        self.api_attributes["settings"] = self.supported_settings


    ###########################################################################
    ###########################################################################

    def on_start(self):
        super().on_start()
        pass

    ###########################################################################
    ###########################################################################
        
    def loop(self):
        """ FROM MetaDriver
        """
        return False

    ###########################################################################
    ###########################################################################


    def __set_state(self, payload):
        """
        """
        # Parse request
        req = self.payload_to_dict(payload)
        req_state = req["state"]
        # Update enable
        self.state = req_state

        DriverHm7044.PSU_SERIALS[self.serial_port]["mutex"].acquire()
        
        if self.state == "on" :
            DriverHm7044.PSU_SERIALS[self.serial_port]["output_enabled"].append(self.channel)
        elif self.state == "off" :
            DriverHm7044.PSU_SERIALS[self.serial_port]["output_enabled"].remove(self.channel)
        
        disabled_channels = list(set([1, 2, 3, 4]) - set(DriverHm7044.PSU_SERIALS[self.serial_port]["output_enabled"]))

        if(len(disabled_channels) != 0):
            select_cmd_disable = "SEL " + str(disabled_channels).strip("[]")

            DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(bytes(select_cmd_disable, "utf-8") + b'\r\n')
            DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(bytearray(b'DIS\r\n'))
            print("disabled: " + select_cmd_disable)

        if(len(DriverHm7044.PSU_SERIALS[self.serial_port]["output_enabled"]) != 0):
            select_cmd_enable = "SEL " + str(DriverHm7044.PSU_SERIALS[self.serial_port]["output_enabled"]).strip("[]")
            
            DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(bytes(select_cmd_enable, "utf-8") + b'\r\n')
            DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(bytearray(b'EN\r\n'))
            print("enabled: " + select_cmd_enable)

        DriverHm7044.PSU_SERIALS[self.serial_port]["mutex"].release()

        self.psu_push_attribute("state", self.state)
        logger.info(f"new state :" + str(payload))
        
    ###########################################################################
    ###########################################################################

    def __set_volts(self, payload):
        """
        """
        # Parse request
        req = self.payload_to_dict(payload)
        self.api_attributes["volts"]["value"] = req["volts"]
        print(req["volts"])
        volts = req["volts"]
        
        DriverHm7044.PSU_SERIALS[self.serial_port]["mutex"].acquire()

        #DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(bytearray(b'SEL NONE\r\n'))
        msg1 = bytearray(b'SEL ' + bytes(str(self.channel), "utf-8") + b'\r\n')
        print(msg1)
        DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(msg1)
        time.sleep(0.1)

        msg2 = bytearray(b'SET ' + bytes(f"{volts:.2f}", "utf-8") + b' V\r\n')
        print(msg2)
        DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(msg2)
        time.sleep(0.1)

        DriverHm7044.PSU_SERIALS[self.serial_port]["mutex"].release()

        self.psu_push_attribute("volts", self.api_attributes["volts"])
        logger.info(f"new volts :" + str(payload))

    ###########################################################################
    ###########################################################################

    def __set_amps(self, payload):
        """
        """
        # Parse request
        req = self.payload_to_dict(payload)
        self.api_attributes["amps"]["value"] = req["amps"]
        print(req["amps"])
        amps = req["amps"]
        
        DriverHm7044.PSU_SERIALS[self.serial_port]["mutex"].acquire()

        msg1 = bytearray(b'SEL ' + bytes(str(self.channel), "utf-8") + b'\r\n')
        print(msg1)
        DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(msg1)
        time.sleep(0.1)

        msg2 = bytearray(b'SET ' + bytes(f"{amps:.3f}", "utf-8") + b' A\r\n')
        print(msg2)
        DriverHm7044.PSU_SERIALS[self.serial_port]["dev"].write(msg2)
        time.sleep(0.1)

        DriverHm7044.PSU_SERIALS[self.serial_port]["mutex"].release()

        self.psu_push_attribute("amps", self.api_attributes["amps"])
        logger.info(f"new amps :" + str(payload))


