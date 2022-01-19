"""
Module for a plant instance.
"""


class Plant:
    """
    Class to monitor a plant.
    """
    def __init__(self, sensors: list):
        """
        Constructor for the plant class.

        Parameters
        ----------
        sensors : list
                A list of sensors to use to characterize the plant.
        """
        self.sensor_list = sensors

    def collect_plant_data(self):
        """
        Loop over sensors and collect plant data.

        Returns
        -------
        plant_data : dict
                A dict of plant data. Keys are the sensor names taken
                from the cls.__name__ in-built method of each sensor class.
                Values are the outputs from the classes cls.read_sensor() method.
        """
        plant_data = {}

        for item in self.sensor_list:
            plant_data[item.__class__.__name__] = item.read_sensor()

        return plant_data

    @staticmethod
    def report_plant_data(data: dict):
        """
        Report the plant data by printing to the screen.

        Parameters
        ----------
        data : dict
                Data to be printed. Dict data generated from the
                collect_plant_data method.

        Returns
        -------
        Prints data to the screen.
        """
        for item in data:
            for sub_item in data[item]:
                print(f"{sub_item}: {data[item][sub_item]: .2f}")
        print("\n")  # newline for better formatting.
