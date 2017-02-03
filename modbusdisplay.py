import win_inet_pton
import socket
import time
from pyModbusTCP.client import ModbusClient
from threading import Thread, Lock

SERVER_HOST = "192.168.1.74"
SERVER_PORT = 502


# set global
regs = []

# init a thread lock
regs_lock = Lock()

# modbus polling
def polling_thread():
    global regs
    c = ModbusClient(SERVER_HOST, auto_open = True, auto_close = True)
    # polling loop
    while True:
        # modbus read
        reg_list = c.read_holding_registers(3000, 11)
        # if read is ok, store result in regs (with thread lock synchronization)
        if reg_list:
            with regs_lock:
                regs = reg_list
        # polling delay
        time.sleep(1)


# start polling thread
tp = Thread(target=polling_thread)
# set daemon: polling thread will exit if main thread exit
tp.daemon = True
tp.start()

# display loop (in main thread)
while True:
    # print regs list
    with regs_lock:
        print('ARM - Firmware version %s' % regs)
    # printing delay
    time.sleep(1)