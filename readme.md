# ✨ About

Here is all our codes and records, include OpenCV experiment codes and the whole system on **Raspberry Pi** to communicate with **PLC**. All of them are written by python.

## 📃 Contents

* [Folder](#folder)

## 📁 Folder

* **📂 CV_experiment**
    This folder puts some codes here, which are some ~~useless~~ experiments.

* **📂 Main Struct**
    Mainly system run with **Raspberri Pi**.
    
* **📂 Main Struct New**
    Same as **Main Struct**, but code are cleaner, and can input with **computer keyboard**.
    
* **📂 solder_speed_experiment**
    Solder speed statistics and plots.

## Autostart

We use a `.sh` script file, every time the **Raspberry Pi** boots it will automatically start the system. Through we have graphic window, it needs to edit `/etc/xdg/lxsession/LXDE-pi/autostart` to run our system rightly.
Add this line in the `autostart` file:

```bash
@sh /home/pi/autostart.sh
```
