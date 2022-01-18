"""
Module for the BMP180 temperature, altitude, and humidity sensor.
"""
import smbus
import time
from ctypes import c_short


class BMP180:
    """
    Class to manage the BMP180 temperature, altitude, and humidity sensor.

    Attributes
    ----------
    channel : int (default = 0x77)
            Channel from which to read data. Default for the BMP180 is 0x77.
    bus : smbus2.SMBus(bus) (default bus = 1)
            Bus on the cpu-device from which to read from an I2C bus.
            On raspberry pi 4B this is defaulted to 1.
    """
    def __init__(self, channel: int = 0x77, bus: int = 1):
        """
        Constructor for the BMP180 class.

        Parameters
        ----------
        channel : int (default = 0x77)
                I2C channel to read data from. This sensor defaults to 0x77.
        bus : int (default = 1)
                I2C bus to look for. Raspberry Pi 4 defaults to 1.
        """
        self.channel = channel
        self.bus = smbus2.SMBus(bus)

    @staticmethod
    def convert_to_string(data: list):
        """
        Convert binary data to string data.

        Parameters
        ----------
        data : list
                Binary data to convert.

        Returns
        -------
        converted_data : str
                Converted data to be printed.
        """
        return str((data[1] + (256 * data[0])) / 1.2)

    @staticmethod
    def get_short(data: list, index: int):
        """
        Return two signed bytes from the data to get sensor information.

        Parameters
        ----------
        data : list
                Binary data to be read
        index : int
                Index to reference first of the two read in.

        Returns
        -------
        Data as signed integers.
        """
        return c_short((data[index] << 8) + data[index + 1]).value

    @staticmethod
    def get_u_short(data: list, index: int):
        """
        Get two bytes from the data as an unsigned int.

        Parameters
        ----------
        data : list
                Data from which to read.
        index
                Index of the first of the two bytes to read.

        Returns
        -------
        data as an unsigned 16-bit integer.
        """
        # return two bytes from data as an unsigned 16-bit value
        return (data[index] << 8) + data[index + 1]

    def read_sensor_id(self):
        """
        Read the sensor id from the register.

        Returns
        -------
        chip_id : int
                ID of the sensor chip.
        chip_version : int
                Version of the sensor chip.
        """
        reg_id = 0xD0
        chip_id, chip_version = self.bus.read_i2c_block_data(
            self.channel, reg_id, 2
        )
        return chip_id, chip_version

    def read_sensor(self):
        """
        Read the data from the sensor.

        Returns
        -------
        sensor_data : dict
                Dict of sensor data. Within this data is contained:
            temperature : float
                    Current temperature as measured by the sensor.
            pressure : float
                    Air pressure measured by the sensor.
            altitude : float
                    Altitude measured by the sensor.
        """
        # Register Addresses
        reg_calib = 0xAA
        reg_meas = 0xF4
        reg_msb = 0xF6
        reg_lsb = 0xF7
        # Control Register Address
        crv_temp = 0x2E
        crv_pres = 0x34
        # Oversample setting
        oversample = 3  # 0 - 3

        # Read calibration data
        # Read calibration data from EEPROM
        cal = self.bus.read_i2c_block_data(self.channel, reg_calib, 22)

        # Convert byte data to word values
        ac1 = self.get_short(cal, 0)
        ac2 = self.get_short(cal, 2)
        ac3 = self.get_short(cal, 4)
        ac4 = self.get_u_short(cal, 6)
        ac5 = self.get_u_short(cal, 8)
        ac6 = self.get_u_short(cal, 10)
        b1 = self.get_short(cal, 12)
        b2 = self.get_short(cal, 14)
        mb = self.get_short(cal, 16)
        mc = self.get_short(cal, 18)
        md = self.get_short(cal, 20)

        # Read temperature
        self.bus.write_byte_data(self.channel, reg_meas, crv_temp)
        time.sleep(0.005)
        (msb, lsb) = self.bus.read_i2c_block_data(self.channel, reg_msb, 2)
        ut = (msb << 8) + lsb

        # Read pressure
        self.bus.write_byte_data(
            self.channel, reg_meas, crv_pres + (oversample << 6)
        )
        time.sleep(0.04)
        msb, lsb, xsb = self.bus.read_i2c_block_data(
            self.channel, reg_msb, 3
        )
        up = ((msb << 16) + (lsb << 8) + xsb) >> (8 - oversample)

        # Refine temperature
        x1 = ((ut - ac6) * ac5) >> 15
        x2 = (mc << 11) / (x1 + md)
        b5 = x1 + x2
        temperature = int(b5 + 8) >> 4
        temperature = temperature / 10.0

        # Refine pressure
        b6 = b5 - 4000
        b62 = int(b6 * b6) >> 12
        x1 = (b2 * b62) >> 11
        x2 = int(ac2 * b6) >> 11
        x3 = x1 + x2
        b3 = (((ac1 * 4 + x3) << oversample) + 2) >> 2

        x1 = int(ac3 * b6) >> 13
        x2 = (b1 * b62) >> 16
        x3 = ((x1 + x2) + 2) >> 2
        b4 = (ac4 * (x3 + 32768)) >> 15
        b7 = (up - b3) * (50000 >> oversample)

        p = (b7 * 2) / b4

        x1 = (int(p) >> 8) * (int(p) >> 8)
        x1 = (x1 * 3038) >> 16
        x2 = int(-7357 * p) >> 16
        pressure = int(p + ((x1 + x2 + 3791) >> 4))
        # pressure = float(pressure / 100.0)

        altitude = 44330.0 * (1.0 - pow(pressure / 101325.0, (1.0 / 5.255)))
        altitude = round(altitude, 2)

        sensor_data = {
            'temperature': temperature,
            'air_pressure': pressure,
            'altitude': altitude
        }

        return sensor_data
