#!/usr/bin/python3
from time import sleep, gmtime, strftime
import schedule
import os
import threading

# per-phone params
MOUNT_POINT = './5'                 # location to find mounted iPhone
USER = 'root'                       # user to ssh into iPhone with
IP_ADDRESS = '192.168.0.107'        # local address phone is located at

# magic strings
EVENT = 'libactivator.motion.shake'
PHOTO_DIR = 'private/var/mobile/Media/DCIM/101APPLE'
THUMBNAIL_DIR = 'private/var/mobile/Media/PhotoData/Thumbnails/V2/DCIM/101APPLE'

# magic sleeps
SAVE_TO_PHONE = 5                   # buffer to allow video to save to phone
SHUTTER_REST = 1                    # buffer to allow camera to reset between captures
SCHEDULER_FREQ = 1                  # buffer to make the scheduler run 'fast enough'

# video frequency params
RECORDING_LENGTH = 10               # length of video recording (seconds)
OUTPUT_DIR = './storage'            # local path to write video to

class iPhoneScraper:
    def __init__(self):
        self.start_time = ''
        self.is_recording = False
        self.resetCameraState()

    def resetCameraState(self):
        self.clearPhoneData()
        self.toggleCamera()
        sleep(SAVE_TO_PHONE)

        if (len(os.listdir(f'{MOUNT_POINT}/{PHOTO_DIR}')) == 0):
            print('program initialized while camera was OFF')
            self.toggleCamera()
            sleep(SAVE_TO_PHONE)
        else:
            print('program initialized while camera was ON')

        self.clearPhoneData()
        self.is_recording = False

    def toggleCamera(self):
        os.system(f"ssh {USER}@{IP_ADDRESS} 'activator activate {EVENT}'")
        self.is_recording = not self.is_recording

    def clearPhoneData(self):
        os.system(f"rm -rf {MOUNT_POINT}/{THUMBNAIL_DIR}/*")
        os.system(f"rm -rf {MOUNT_POINT}/{PHOTO_DIR}/*")

    def copyToComputer(self, start_time):
        sleep(SAVE_TO_PHONE)
        movies = os.listdir(f'{MOUNT_POINT}/{PHOTO_DIR}')
        os.system(f"cp {MOUNT_POINT}/{PHOTO_DIR}/{movies[0]} ./{OUTPUT_DIR}/{start_time}.mov")
        self.clearPhoneData()

        print(f"SUCCESS:  {RECORDING_LENGTH}s recording at {start_time}")

    def scrape(self):
        if (self.is_recording):
            self.toggleCamera()
            threading.Thread(
                target=self.copyToComputer,
                args=[self.start_time]
            ).start()
            sleep(SHUTTER_REST)

        self.start_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        self.toggleCamera()

# set up the scheduling task
scraper = iPhoneScraper()
schedule.every(RECORDING_LENGTH).seconds.do(scraper.scrape)

while True:
    schedule.run_pending()
    sleep(SCHEDULER_FREQ)
