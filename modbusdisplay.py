import win_inet_pton
import socket
import time
from threading import Thread, Lock
from pyModbusTCP.client import ModbusClient

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 502

# set global
regs = []
poll_rate = 0.5

# init a thread lock
regs_lock = Lock()

# modbus polling thread
def polling_thread():
    global regs
    try:
        c = ModbusClient(host=SERVER_HOST, port=502)
        c.debug(True)
    except ValueError:
        print("Error with host or port params")    # polling loop
    while True:
        # keep TCP open
        if not c.is_open():
            c.open()
        # do modbus reading on socket
        reg_list = c.read_input_registers(0)
        # if read is ok, store result in regs (with thread lock synchronization)
        if reg_list:
            with regs_lock:
                regs.append(reg_list[0])
        else:
            with regs_lock:
                regs = ['Failed to read']
        # 1s before next polling
        time.sleep(poll_rate)


# start polling thread
tp = Thread(target=polling_thread)
# set daemon: polling thread will exit if main thread exit
tp.daemon = True
tp.start()

# display loop (in main thread)
while True:
    # print regs list (with thread lock synchronization)
    with regs_lock:
        if regs:
            print(regs)
    # 1s before next print
    time.sleep(poll_rate)