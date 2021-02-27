import numpy as np

import pycuda.driver as cuda
from pycuda.compiler import SourceModule
from pycuda.tools import make_default_context, clear_context_caches

import glob
import sys
import os
from datetime import datetime
import ctypes
import atexit
import argparse
import subprocess
import psutil
import itertools

from signal import signal, SIGINT
from sys import exit
from multiprocessing import Process, Value, set_start_method, Pool, cpu_count, current_process
from codetiming import Timer
from utils import calc_bws, calc_gbs

global cuda_devices

parser = argparse.ArgumentParser(description="A program for simulating load on GPU memory and system bus")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--single', type=int, help="Run with a N constant size array")
group.add_argument('--batch', action='store_true')
group.add_argument('--hwinfo', type=int, help="Gets info for CUDA device with ID")
parser.add_argument('-d', '--num_devices', type=int, help="Number of CUDA devices to use")
parser.add_argument('-i', '--iterations', type=int, default=1, help="number of iterations to run")
parser.add_argument('-w', '--workers', type=int, default=4, help="number of workers to spawn")
parser.add_argument('-e', '--elements', type=int, default=4, help="number of numpy arrays to work on")
parser.add_argument('--debug', action='store_true')
parser.add_argument('-n', '--name', type=str, help='name to use for the run')
args = parser.parse_args()

def get_hw_info(device_id):
    device = cuda.Device(device_id)
    return "device_id: {}, bus_id: {}, name: {}, cuda_version: {}".format(device_id, device.pci_bus_id(), device.name(), cuda.get_version())

def handler(signal_received, frame):
    print('Shutting down...')
    exit(0)

def np_to_hmem(src, dest):
    source = src.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    destination = dest.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    size = src.size * ctypes.sizeof(ctypes.c_float)
    ctypes.memmove(source,destination,size)

def load_single_array(mb_size):
    return np.random.randn(int(mb_size * (10**6)/4)).astype(np.float32)

def transfer_data(size):
    t1 = Timer(name="total_memcpy_time", logger=None)
    t1.start()
    cuda.init()
    device = cuda.Device(0)
    context = device.make_context()
    dev_id = context.get_device().pci_bus_id()
    np_array = np.random.randn(int(size * (10**6)/4)).astype(np.float32)
    np_return = np.empty_like(np_array)
    mem_gpu = cuda.mem_alloc(np_array.nbytes)
    mem_host = cuda.register_host_memory(np_array)
    np_to_hmem(np_array,mem_host)
    t2 = Timer(name="hmem_to_dmem", logger=None)
    t2.start()
    cuda.memcpy_htod(mem_gpu, mem_host)
    t2.stop()
    t3 = Timer(name="dmem_to_hmem", logger=None)
    t3.start()
    return_data = np.empty_like(np_array)
    cuda.memcpy_dtoh(mem_host, mem_gpu)
    t3.stop()
    mem_host.base.unregister()
    mem_gpu.free()
    context.pop()
    context = None
    clear_context_caches()
    t1.stop()
    if(args.debug):
        print("{},{},{},{},{},{},{},{}".format('htod-'+args.name+'-debug',args.single,format(t2.last, '.4f'),calc_gbs(size,t2.last),psutil.Process().cpu_num(),psutil.Process().pid,dev_id,current_process().name))
        print("{},{},{},{},{},{},{},{}".format('dtoh-'+args.name+'-debug',args.single,format(t3.last, '.4f'),calc_gbs(size,t3.last),psutil.Process().cpu_num(),psutil.Process().pid,dev_id,current_process().name))
    return {'total_time':t1.last, 'htod': calc_gbs(size,t2.last), 'htod_time':t2.last, 'dtoh': calc_gbs(size,t3.last), 'dtoh_time':t3.last}

def devices_to_workers():
    cuda.init()
    global cuda_devices
    available_devices = args.num_cuda_devices
    for i in range(args.workers):
        cuda_devices[i] = 0

if __name__ == "__main__":
    signal(SIGINT, handler)
    set_start_method('fork')
    np_list = [args.single for x in range(args.elements)]
    pool = Pool(processes=args.workers)
    for i in range(args.iterations):
        total_size = args.single * args.elements
        res = pool.map(transfer_data, np_list)
        hotd_bandwidth = sum([float(x['htod']) for x in res])/args.elements
        dtoh_bandwidth = sum([float(x['dtoh']) for x in res])/args.elements
        total_time = sum([float(x['total_time']) for x in res])
        htod_time = sum([float(x['htod_time']) for x in res])
        dtoh_time = sum([float(x['dtoh_time']) for x in res])
        print("{},{},{},{},{},{},{},{},{},{}".format(args.name,args.single,format(total_time, '.4f'),format(hotd_bandwidth, '.4f'),format(htod_time, '.4f'),format(dtoh_bandwidth, '.4f'),format(dtoh_time, '.4f'),args.workers,'epoch-'+str(i),datetime.now().strftime("%H:%M:%S:%f")))
    if args.hwinfo != None:
            print(get_hw_info(args.hwinfo))