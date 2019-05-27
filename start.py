#!/usr/bin/python3
import schedule
import time
from record_to_computer import run

schedule.every(10).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
