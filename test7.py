import time
import usb
import os
import sys
from Xlib.display import Display
from Xlib import X
from xtest_fakeinput import fake_input

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

left_btn_state = 128
BUTTON_NAME_MAPPING = {'left': 1, 'middle': 2, 'right': 3, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}
screen_width = 1366
screen_height = 768


def id_pen(data):
    global left_btn_state
    x = round(((data[3] * 255 + data[2]) / PEN_MAX_X) * screen_width)
    y = round(((data[5] * 255 + data[4]) / PEN_MAX_Y) * screen_height)
    fake_input(_display, X.MotionNotify, x=x, y=y)
    if data[1] in [128, 130, 132]:
        fake_input(_display, X.ButtonRelease, BUTTON_NAME_MAPPING['left'])
        left_btn_state = 128
    if data[1] in [129, 131, 133]:
        fake_input(_display, X.ButtonPress, BUTTON_NAME_MAPPING['left'])
        left_btn_state = 129
    _display.sync()


def xlib_control(endpoint1):
    try:
        data1 = dev.read(endpoint1.bEndpointAddress, endpoint1.wMaxPacketSize)
        sys.stdout.write("\rDoing thing %a" % data1)
        sys.stdout.flush()
        id_pen(data1)
    except Exception as e:
        if "Errno 110" not in str(e):
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
