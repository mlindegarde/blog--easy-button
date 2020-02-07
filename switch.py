import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

btn_pressed = False
last_sent_ts = 0
throttle = 3

while True:
    input_state = GPIO.input(14)
    current_ts = time.time();
    delta = current_ts - last_sent_ts

    if input_state == 0 and not btn_pressed:
        btn_pressed = True

        if delta >= throttle:
            try:
                url = 'https://hooks.slack.com/services/[your]/[slack]/[link]'
                payload = '{"text": "You should turn around... now."}'

                requests.request("POST", url, data=payload)
                last_sent_ts = current_ts
                
                print('Notification sent')
                
            except requests.exceptions.RequestException as e:
                print(e)

            time.sleep(0.2)

    elif input_state == 1 and btn_pressed:
        btn_pressed = False
        
# Add this script to the /etc/rc.local file.  That will start the
# script when the pi boots.  Just put the following line at the bottom
# before "exit 0"
#
# sudo python /home/pi/switch.py &
#
# This is what my /etc/rc.local file looks like:
# #
# # By default this script does nothing.
# 
# # Print the IP address
# _IP=$(hostname -I) || true
# if [ "$_IP" ]; then
#   printf "My IP address is %s\n" "$_IP"
# fi
# 
# sudo python /home/pi/switch.py &
# 
# exit 0