"""
Example script to report plant data every 10 seconds
"""
import plant
import time
from tqdm import tqdm

light_sensor = plant.sensors.light_sensors.BH170()
temperature_sensor = plant.sensors.temperature_sensors.BMP180()

example_plant = plant.Plant(sensors=[light_sensor, temperature_sensor])

print("Initializing sensors")
for _ in tqdm(range(5), ncols=50):
    time.sleep(1)

while True:
    data = example_plant.collect_plant_data()  # collect a dict of data
    example_plant.report_plant_data(data=data)  # print it to the screen
    time.sleep(10)
