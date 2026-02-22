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
For example, we include a swappable head as well as different display modes. To this end we've open sourced both the code and CAD files 
to be transparent about our process 

### An Explanation of this Code 
This repo is incredibly messy unfortunately. We originally intended to run camera vision and a lot of our initial code was built around this idea.
Our real main code that is demoed is contained within the SensorVersion directory which was a fallback. 

### Run Instructions 
1. Set up the Rasberry PI Zero W 2 with the peripherals. The ports are specified in the config file inside SensorVision. More detailed resources can be
found on the official rasberry PI documentation if you are not familiar with the PI
2. Connect to the Rasberry PI
3. Clone this repo
4. Test by executing main
5. Add a cron job

### Some Notes 
- The image capturing is inconsistent, we ran into a lot of dependency issues so we did a work around by executing a bash script
- The device can delay on image capturing
