import time
import usb
import pyautogui
import os
from Xlib.display import Display
from Xlib.X import MotionNotify
from Xlib.ext.xtest import fake_input

pyautogui.FAILSAFE = False
util = usb.util
core = usb.core

auto_find: bool = True
ids = [0x256c, 0x006e]
interfaces = [0, 1]  # 2 interface only afaik

PEN_MAX_X = 44000  # 50800
PEN_MAX_Y = 27300  # 31750
PEN_MAX_Z = 8192  # 2048 	#pressure

_display = Display(os.environ['DISPLAY'])

# 1 - detect tablet
def find_device(ids):
    return core.find(idVendor=ids[0], idProduct=ids[1])


def device_found(ids):
    return True if find_device(ids) is not None else False


def timestamp():
    return time.strftime("%X")


def plog(msg):
    print("[{}] {}".format(timestamp(), msg))


def claim_interface(device, interface_nums):
    for i in interface_nums:
        if device.is_kernel_driver_active(i) is True:
            plog("Kernel driver of interface {} is active".format(i))
            device.detach_kernel_driver(i)
            util.claim_interface(device, i)
            plog("Interface {} is claimed".format(i))


finding = False
found = False
not_found = True


def id_pen(data):
    x = round(((data[3] * 255 + data[2]) / PEN_MAX_X) * 1366)
    y = round(((data[5] * 255 + data[4]) / PEN_MAX_Y) * 768)
    fake_input(_display, MotionNotify, x=x, y=y)
    _display.sync()



def xlib_control(endpoint1):
    try:
        data1 = dev.read(endpoint1.bEndpointAddress, endpoint1.wMaxPacketSize)
        plog(data1[1])
        id_pen(data1)
    except Exception as e:
        if not "Errno 110" in str(e):
            plog(e)

running = True
while running:
    if finding is False:
        finding = True
        plog("Finding device...")
    dev = find_device(ids)
    if device_found(ids):
        if found is False:
            not_found = False
            found = True
            plog("Device is found")
        claim_interface(dev, interfaces)
        plog("Entering xlib loop...")
        endpoint1 = dev[0][(0, 0)][0]
        entered_evdev = False
        while device_found(ids):
            if entered_evdev is False:
                entered_evdev = True
                plog("Entered xlib loop")
            xlib_control(endpoint1)
            # time.sleep(1)
        entered_evdev = False
        plog("Exited from xlib loop")
        # 4 send data to evdev
    else:
        if not_found is False:
            not_found = True
            found = False
            plog("Device is not found")
            finding = False
    time.sleep(1)
    running = auto_find
