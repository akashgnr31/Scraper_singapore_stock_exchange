from os.path import basename
import os
from urllib.parse import urlsplit
import urllib.request
import logging
import wget
import sys, getopt
from datetime import datetime
import config as conf

logger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d")

# Set up the console handler
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

# Set up the file handler 
fileHandler = logging.FileHandler("All_time_log.log",'a')
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# Set up logging levels
consoleHandler.setLevel(logging.WARNING)
fileHandler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)


#Main Function            
def main(argv):
    if(len(argv)<3):
        #Logging for less argument passed
        logging.error('Too few arguments were passed in the Job from server.py')
        logging.error('First argument should either be 0 or 1 where 0 for daily downloads and 1 for failed recoverys')
        logging.error('Second argument should be the file name where Download codes should be stored')
        logging.error('Third argument should be the Directory name where you want to store all the files')

    elif(argv[0]=='0'):  # Downloads
        
        logging.info("Daily download Job started")
        #Extracting the download codes from Download_codes txt file
        code = conf.codeExtractionfile(argv[1])
        #Code to which it is to be downloaded
        present_code = code[0]
        #Code from where it is to be downloaded 
        previous_code = code[1]
        code = present_code
        if(code<previous_code):
            logging.error('In Download_codes.txt first integer should be the present day uploaded files directory and second should be the first minus number of days for which you want download minus 1')
        
        
        #Iterate over all codes for which it is to be downloaded
        while(code>=previous_code):
            #Set the location where you want to create the directories to download the files
            path = os.path.join(argv[2], str(code))
            #Make directory with exception handling to store files
            try:  
            
                os.makedirs(path)
                logging.info("Directory Created "+str(code))
                #download all the files with given download code to given paths
                conf.downloadAll(code,path)  
                    
            except OSError as error:
                #if error in making the directory which means the it was already made so we just have to download the files
                conf.downloadAll(code,path)  
            
            #decrement in the codes
            code = code -1 

        #Updating the next day codes in the file
        conf.NextDaycodestored(argv[1],present_code)
        logging.info("Daily download Job Ended")
        

    elif(argv[0]=='1'): #All Failed download if any download got failed 
        
        logging.info("Recovery Job started")
        try:
            #Reads all the pending downloads
            with open("DownloadFailed.txt", "r") as f:
                lines = f.readlines()
            
            #Try to run all the pending Downloads and if any redownload becomes successfull than that name is removed form list otherwise it is not removed from list
            with open("DownloadFailed.txt", "w") as f:
                for line in lines:
                    Pending_Download = line.split()     #break each line into a list
                    code =  Pending_Download[0]
                    files = Pending_Download[1]
                    path = os.path.join(argv[2], code)
                    try:  
                        #Try to download all the previous failed downloads if directory of that day was not made
                        os.makedirs(path)
                        logging.info("Directory Created "+str(code))    
                        
                        l = conf.downloadPrevious(code,files,path)
                        
                    except OSError as error:  
                        #Try to download all the previous failed downloads if directory of that day was made previously
                        l = conf.downloadPrevious(code,files,path)
                                
                    if(l==0):
                        f.write(line)

        except:
                    #If no file exists then no pending downloads are left
                    logging.info('No Pending Download')
        logging.info("Recovery Job ended")
        
    

    else:
            logging.error("2nd Argument should be either 0 or 1 \n1. 0 if you want to New Download \n2. 1 if you want to download Failed download")


if __name__ == "__main__":
    main(sys.argv[1:])
