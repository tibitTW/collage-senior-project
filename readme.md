# Python part of our project

We use python scripts on Raspberry Pi,including interface, OpenCV, and communicate with PLC.

## Structure

```bash
├─CV_experiment
├─Main Struct
└─solder_speed_experiment
```

## Autostart

We create a sh script to run our system interface, and run this script in `/etc/xdg/lxsession/LXDE-pi/autostart` so it will autorun when RPi startup.
Add this line in `autostart` file:

```bash
@sh /home/pi/autostart.sh
```

## ToDo

`modbus.reset()`
