"""
Module for the BH170 light sensor.
"""
import smbus


class BH170:
    """
    Class to manage the BH170 light sensor.

    Attributes
    ----------
    channel : int (default = 0x23)
            Channel from which to read data. Default for the BH170 is 0x77.
    bus : smbus2.SMBus(bus) (default bus = 1)
            Bus on the cpu-device from which to read from an I2C bus. On Raspi 4B this
            is defaulted to 1.
    """
    def __init__(self, channel: int = 0x23, bus: int = 1):
        """
        Constructor for the BH170 sensor class.

        Parameters
        ----------
        channel : int (default = 0x23)
            Channel from which to read data. Default for the BH170 is 0x77.
        bus : int (default = 1)
            Bus on the cpu-device from which to read from an I2C bus. On Raspi 4B this
            is defaulted to 1.
        """
        self.channel = channel
        self.bus = smbus2.SMBus(bus)

    @staticmethod
    def convert_to_number(data: list):
        """
        Convert the sensor read to a number.

        Parameters
        ----------
        data : list
                Binary data to convert.

        Returns
        -------
        number_value : float
                Float value for the given binary input.
        """
        number_value = (data[1] + (256 * data[0])) / 1.2

        return number_value

    def read_sensor(self):
        """
        Read the sensor value.

        Returns
        -------
        sensor_data : dict
                Dict of sensor data. Within this data is contained:
            light_value : float
                    Light value measured in lux with the key name light_intensity.
        """
        data = self.bus.read_i2c_block_data(self.channel, 0x20)

        sensor_data = {"light_intensity": self.convert_to_number(data)}

        return sensor_data
