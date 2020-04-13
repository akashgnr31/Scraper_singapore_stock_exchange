from os.path import basename
import os
from urllib.parse import urlsplit
import urllib.request
import logging
import wget
import sys, getopt
import numpy as np
from datetime import datetime

def down_WEBPXTICK_DT(code,out_path):
    url = 'https://links.sgx.com/1.0.0/derivatives-historical/'+str(code)+'/WEBPXTICK_DT.zip'
    try:
        wget.download(url,out_path)
        logging.info('Successful download of'+ str(code)+ ' WEBPXTICK_DT.zip')
        return 1
    except OSError as error:
        return 0
        

def down_TickData_structure(code,out_path):
    url = 'https://links.sgx.com/1.0.0/derivatives-historical/'+str(code)+'/TickData_structure.dat'
    try:
        wget.download(url,out_path)
        logging.info('Successful download of'+ str(code)+ ' TickData_structure.dat')
        return 1
    except OSError as error:
        return 0


def down_TC(code,out_path):
    url = 'https://links.sgx.com/1.0.0/derivatives-historical/'+str(code)+'/TC.txt'
    try:
        wget.download(url,out_path)
        logging.info('Successful download of'+ str(code)+ ' TC.txt')
        return 1
    except OSError as error:
        return 0



def down_TC_structure(code,out_path):
    url = 'https://links.sgx.com/1.0.0/derivatives-historical/'+str(code)+'/TC_structure.dat'

    try:
        wget.download(url,out_path)
        logging.info('Successful download of'+ str(code)+ ' TC_structure.dat')
        return 1
    except OSError as error:
        return 0


def downloadAll(code,out_path):
    WEBPXTICK_DT = down_WEBPXTICK_DT(code,out_path)
    TickData_structure = down_TickData_structure(code,out_path)
    TC = down_TC(code,out_path)
    TC_structure = down_TC_structure(code,out_path)
    f = open('DownloadFailed.txt', "a")
    if(WEBPXTICK_DT==0):
        logging.info('Download Failed of '+str(code)+' WEBPXTICK_DT.zip')
        f.write(str(code)+' WEBPXTICK_DT.zip\n')
    

    if(TickData_structure==0):
        logging.info('Download Failed of '+str(code)+' TickData_structure')
        f.write(str(code)+' TickData_structure.dat\n')
    
    if(TC==0):
        logging.info('Download Failed of '+str(code)+' TC')
        f.write(str(code)+' TC.txt\n')
    
    
    if(TC_structure==0):
        logging.info('Download Failed of '+str(code)+' TC_structure')
        f.write(str(code)+' TC_structure.dat\n')
    f.close()


def downloadPrevious(code,files,path):
    url = 'https://links.sgx.com/1.0.0/derivatives-historical/' + code+'/'+files
    try:
        wget.download(url,path)
        logging.info('Successful recovery of '+code+' '+files)
        return 1

    except OSError as error:
        logging.info('Failed recovery of '+code+' '+files)
        return 0

def codeExtractionfile(filename):
    try:
        f = open(filename, "r")
        lines = f.readlines()
        code= []
        first = (lines[0]).split()
        code.append(int(first[0]))
        code.append(int(first[0]))
        if(len(lines)>1):
            second = (lines[1]).split()
            code[1]= int(second[0])

        return code


        
    except OSError as error:
        logging.error('Either the file Download_codes.txt is not present or they are not entered in it in proper format')
        
def NextDaycodestored(filename,code):
    code = code + 1
    f = open(filename, "w")
    f.write(str(code)+'\n')
    f.write(str(code)+'\n')    
