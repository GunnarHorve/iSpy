#!/usr/bin/python3
import os
from time import sleep, gmtime, strftime

# per-phone params
MOUNT_POINT = './5'                 # location to find mounted iPhone
USER = 'root'                       # user to ssh into iPhone with
IP_ADDRESS = '192.168.0.102'        # local address phone is located at

# video frequency params
RECORDING_LENGTH = 10               # length of video recording (seconds)
COOLDOWN_PERIOD = 5                 # buffer to allow video to process (seconds)
OUTPUT_DIR = './storage'            # local path to write video to

# magic strings
EVENT = 'libactivator.motion.shake'
PHOTO_DIR = 'private/var/mobile/Media/DCIM/100APPLE'
THUMBNAIL_DIR = 'private/var/mobile/Media/PhotoData/Thumbnails/V2/DCIM/100APPLE'

def toggleCamera():
    os.system(f"ssh {USER}@{IP_ADDRESS} 'activator activate {EVENT}'")

def clearPhoneData():
    os.system(f"rm -rf {MOUNT_POINT}/{THUMBNAIL_DIR}/*")
    os.system(f"rm -rf {MOUNT_POINT}/{PHOTO_DIR}/*")

def copyToComputer(start_time):
    movies = os.listdir(f'{MOUNT_POINT}/{PHOTO_DIR}')
    if (len(movies) != 0):
        os.system(f"cp {MOUNT_POINT}/{PHOTO_DIR}/{movies[0]} ./{OUTPUT_DIR}/{start_time}.mov")
        print(f"SUCCESS:  {RECORDING_LENGTH}s recording at {start_time}")
    else:
        print(f"FAILURE:  {RECORDING_LENGTH}s recording at {start_time}")
        toggleCamera()

# simple, dumb logic
start_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
toggleCamera()
clearPhoneData()
sleep(RECORDING_LENGTH)
toggleCamera()
sleep(COOLDOWN_PERIOD)
copyToComputer(start_time)
