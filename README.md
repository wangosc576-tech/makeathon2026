# The Bootleg - Makeathon26 

### Materials 
- Rasberry PI Zero W 2
- RGB LED
- IR Sensor
- PI Camera
- OLED Screen
- 3D Printed Components

### The idea 
The bootleg is a toy designed for anyone with a creative and open mind. It is designed to be modular and user friendly to adapt to any person's needs. 
Some features include a flashlight that can be turned off with a hand gesture, a multi-mode display, and a camera. To this end we've open sourced both the code and CAD files (avaialable [here](https://cad.onshape.com/documents/59acc639e04d714ac042ef83/w/0c8d41f5bef0de1e2320df5d/e/d46d1a20cdd18e700e8d2546))
to be transparent about our process. 

### An Explanation of this Code 
This repo is a little messy unfortunately. We originally intended to run camera vision and a lot of our initial code was built around this idea. Unfortunately, we quickly learned that the Pi Zero 2 W was not meant for that, and after ~5 hours debugging and trying various solutions for faster builds and cameras realized that it was best to stick with traditional sensors.
Our  main code that is demoed at the makeathon is contained within the SensorVersion directory which was a fallback. 

### Run Instructions 
1. Set up the Rasberry PI Zero W 2 with the peripherals. The ports are specified in the config file inside SensorVision. More detailed resources can be
found on the official rasberry PI documentation if you are not familiar with the PI. 
2. Connect to the Rasberry PI
3. Clone this repo
```
git clone git@github.com:wangosc576-tech/makeathon2026.git
```
4. `cd` into the repo
```
cd makeathon2026
```
5. Make a `venv`
```
python -m venv .venv_name
```
6. Activate a `venv`
```
source .ven_name/bin/activate
```
7. Instal requirements.txt
```
pip install -r ./SensorVision/requirements.txt
```
8. Depending on the specific OS you flash onto the rasberry PI you may need to do additional work to get the camera python package to load properly. On the PI Legacy Debian 64 Bit Headless OS we had to edit `/boot/config.txt` and add the line `camera_auto_detect=1` but it differes on version.
6. Run Main
```
python ./SensorVision/main.py
```
7. Optionally you may want to enable the program to execute on start without needing to SSH. For this we simply added a cron job. First open the crontab through
```
crontab -e
```
Then you can simply execute the program every time on boot through
```
@reboot /PATH/TO/PYTHON/IN/VENV /PATH/TO/SensorVision/main.py >> /PATH/TO/SensorVision/main.log 2>&1
```
Absolute path must be used since it is run at root

### Some Notes 
- The image capturing is inconsistent, we ran into a lot of dependency issues so we did a work around by executing a bash script and doing a system execution. This is mainly because the camera worked best if installed as a global python package which was hard to reconcile with a virtual environment.
- The device can delay on image capturing and it is something that we've tried to minimize by having image capturing run on a background thread btu there are still delays.
