#!/bin/bash
cd /home/makeathon/real/makeathon2026/SensorVersion
filename="photo_$(date +%Y%m%d_%H%M%S).jpg"
python3 camera.py --save "$filename"
echo "Saved $filename"
