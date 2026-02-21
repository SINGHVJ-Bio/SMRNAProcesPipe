import os
import psutil
from datetime import date
from datetime import datetime
import time
import psutil
from pathlib import Path
import subprocess

UPDATE_DELAY = 10 # in seconds
def convertTuple(tup):
    # initialize an empty string
    strn = ''
    for item in tup:
        strn = strn + str(item) + "\t"
    strn = strn.strip()
    return strn

def cache_mem():
    process = subprocess.Popen(['free', '-m'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    #print(out)
    # decode bytes to python string
    out = out.decode('utf-8')
    #print(out)
    # convert to python list
    out = out.split('\n')
    result = " ".join(out[1].split())
    return int(result.split(" ")[5])

def get_RAM_info():
    """
    Returns size of bytes in a nice format
    """
    ram = psutil.virtual_memory()
    total_ram = ram.total
    available_ram = ram.available
    used_ram = ram.used
    free_ram = ram.free
    percent_ram = ram.percent
    return total_ram, available_ram, used_ram, free_ram, percent_ram

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def getPathSize(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

# get the network I/O stats from psutil on each network interface
# by setting `pernic` to `True`
# io = psutil.net_io_counters(pernic=True)
 
# assign folder path
if not os.path.exists('/home/ubuntu/DATA_DRIVE/WGS_run'):
    os.makedirs('/home/ubuntu/DATA_DRIVE/WGS_run')
workpath = '/home/ubuntu/DATA_DRIVE/WGS_run'
readpath = '/home/ubuntu/DATA_DRIVE/WGS_run/reads'
workdirpath = '/home/ubuntu/DATA_DRIVE/WGS_run/work'
resultpath = '/home/ubuntu/DATA_DRIVE/WGS_run/results'
maindirpath = '/home/ubuntu/DATA_DRIVE/WGS_run'


# Open file to write
file = open(workpath+'/server_resource_utilization_details.tsv', 'w')

som = ("Date", "Time", "CPU_Usage(%)", "Memory_Usage(%)", "Reads_path_Size(GB)", "Work_Size(GB)", "Results_Size(GB)", "Main_Dir_Size(GB)", "total_ram(GB)", "available_ram(GB)", "used_ram(GB)", "free_ram(GB)", "percent_ram(%)", "Cache_used(GB)") # , "Upload_Speed(/s)", "Download_Speed(/s)
strn = convertTuple(som)
file.write(strn + '\n')
file.close() # Close the file

print("Date", "Time", "CPU_Usage(%)", "Memory_Usage(%)", "Reads_path_Size(GB)", "Work_Size(GB)", "Results_Size(GB)", "Main_Dir_Size(GB)", "total_ram(GB)", "available_ram(GB)", "used_ram(GB)", "free_ram(GB)", "percent_ram(%)", "Cache_used(GB)")  # , "Upload_Speed(/s)", "Download_Speed(/s)"
# i=0
while 1:
    # sleep for `UPDATE_DELAY` seconds
    file = open(workpath+'/server_resource_utilization_details.tsv', 'a')
    time.sleep(UPDATE_DELAY)
    try:
        # Getting current date and time
        now = datetime.now()
        total_ram, available_ram, used_ram, free_ram, percent_ram = get_RAM_info()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # Getting loadover at a time interval in minutes
        load1, load5, load15 = psutil.getloadavg()
        
        cpu_usage = round((load15/os.cpu_count()) * 100, 2)
        
        # Getting all memory using os.popen()
        total_memory, used_memory, free_memory = map(
            int, os.popen('free -t -m').readlines()[-1].split()[1:])
        
        # Getting reads dir size
        refsize = round(getPathSize(readpath)/1024000000, 2)
        
        # Getting work dir size
        wfsize = round(getPathSize(workdirpath)/1024000000, 2)

        # Getting work dir size
        rfsize = round(getPathSize(resultpath)/1024000000, 2)

        # Getting work dir size
        mdsize = round(getPathSize(maindirpath)/1024000000, 2)

        # Getting cache size
        cache = cache_mem()

        # get the network I/O stats again per interface
        # io_2 = psutil.net_io_counters(pernic=True)

        # for iface, iface_io in io.items():
        #     # new - old stats gets us the speed
        #     upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[iface].bytes_recv - iface_io.bytes_recv
        #     Download = get_size(io_2[iface].bytes_recv)
        #     Upload = get_size(io_2[iface].bytes_sent)
        #     # Upload_Speed = f"{get_size(upload_speed / UPDATE_DELAY)}/s"
        #     # Download_Speed = f"{get_size(download_speed / UPDATE_DELAY)}/s"
        #     Upload_Speed = get_size(upload_speed / UPDATE_DELAY)
        #     Download_Speed = get_size(download_speed / UPDATE_DELAY)
        
        # # update the I/O stats for the next iteration
        # io = io_2

        # Writing resource details and usage in file
        som = (str(now.strftime("%d/%m/%Y")), str(now.strftime("%H:%M:%S")), str(cpu_usage), str(round((used_memory/total_memory) * 100, 2)), str(refsize), str(wfsize), str(rfsize), str(mdsize)+"   "+str(total_ram/1024000000)+"   "+str(available_ram/1024000000)+"   "+str(used_ram/1024000000)+"   "+str(free_ram/1024000000)+"   "+str(percent_ram)+"   "+str(cache/1000))  # , str(Upload_Speed), str(Download_Speed)
        strn = convertTuple(som)
        file.write(strn + '\n')
        print(str(now.strftime("%d/%m/%Y"))+"   "+str(now.strftime("%H:%M:%S"))+"   "+str(cpu_usage)+"   "+str(round((used_memory/total_memory) * 100, 2))+"   "+str(refsize)+"   "+str(wfsize)+"   "+str(rfsize)+"   "+str(mdsize)+"   "+str(total_ram/1024000000)+"   "+str(available_ram/1024000000)+"   "+str(used_ram/1024000000)+"   "+str(free_ram/1024000000)+"   "+str(percent_ram)+"   "+str(cache/1000)) #+"   "+str(Upload_Speed)+"   "+str(Download_Speed)
    except:
        print("Something went wrong in I/O ")
    file.close() # Close the file
    
