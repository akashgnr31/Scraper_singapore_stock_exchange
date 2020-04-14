from crontab import CronTab
import subprocess
import sys
import os
import logging
import getpass
import datetime

logger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d")
logger.setLevel(logging.WARNING)



def dailyjobs(directory,Terminal_number):
    pwd = os.getcwd()
    username = getpass.getuser()
    cron = CronTab(user=username)
    now = datetime.datetime.now()
    now_plus_5 = now + datetime.timedelta(minutes = 2)

    now_plus_3hrs = now + datetime.timedelta(hours=  3)
    minute = now_plus_5.minute
    hour = now_plus_5.hour
    
    minute_recovery = now_plus_3hrs.minute
    hour_recovery = now_plus_3hrs.hour
    
    job_Daily = cron.new(command='cd '+pwd+' && python3 downloading.py 0 Download_codes.txt '+directory+' >'+Terminal_number)
    job_Daily.setall(minute, hour, None, None, '1-5')
        
    job_Recovery1 = cron.new(command='cd '+pwd+' && python3 downloading.py 1 Download_codes.txt '+directory+' >'+Terminal_number)
    job_Recovery1.setall(minute_recovery, hour_recovery , None, None, '1-5')
            
    cron.write()

def main(argv):
    try:
        Terminal_output_number = (subprocess.check_output(['tty'])).decode('UTF-8')    
    except OSError as error:
        Terminal_output_number = 'output.log'
        logging.warning("Unable to detect the Terminal Output Number So will output std outputs in output.log")
    

    dailyjobs(argv[0],Terminal_output_number)

       
    

if __name__ == "__main__":
    main(sys.argv[1:])
