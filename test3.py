import time
import usb
util = usb.util
core = usb.core

auto_find: bool = True
ids = [0x256c, 0x006e]
interfaces = [0, 1]  # 2 interface only afaik

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
        plog("Entering evdev loop...")
        entered_evdev = False
        while device_found(ids):
            if entered_evdev is False:
                entered_evdev = True
                plog("Entered evdev loop")
                time.sleep(1)
        entered_evdev = False
        plog("Exited from evdev loop")
        # 4 send data to evdev
    else:
        if not_found is False:
            not_found = True
            found = False
            plog("Device is not found")
            finding = False
    time.sleep(1)
    running = auto_find


