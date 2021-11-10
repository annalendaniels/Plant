Plants Hardware
---------------

Processors
^^^^^^^^^^

* Raspberry Pi

I feel the raspi is the best choice. Specifically the Raspberry Pi 4 industrial
available `here <https://buyzero.de/products/compute-module-4-cm4?variant=32090358612070&src=raspberrypi>`_
for 90€.

Sensors
^^^^^^^

For the time being I would suggest we look at mostly wireless sensors using ultra low
energy BLE or wifi connections. We can have a nice watchdog type timer so it only
turns on for a moment, sends a message and goes back to sleep. That way it is maximally
compatible with a custom board in the future. Perhaps looking into arduino nanos
or something of the kind would be a good idea.

* Temperature
* Soil moisture
* Air moisture
* Light
* CO2
* biomass/weight

Plants
^^^^^^

* Venus fly trap: Very sensitive to soil conditions, water content, and sun.