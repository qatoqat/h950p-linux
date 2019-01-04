import usb.util
import time

found = 0

while True:
    dev = usb.core.find(idVendor=0x256c, idProduct=0x006e)
    if dev is not None:
        endpoint1 = dev[0][(0, 0)][0]
        endpoint2 = dev[0][(1, 0)][0]

        interface = [0, 1]
        for i in interface:
            dev.is_kernel_driver_active(i)
            if dev.is_kernel_driver_active(i) is True:
                print("[{}] Kernel driver of interface {} is active".format(time.ctime(), i))
                dev.detach_kernel_driver(i)
                # claim the device
                usb.util.claim_interface(dev, i)
                print("[{}] Interface {} is claimed".format(time.ctime(), i))
        time.sleep(1)
    else:
        print("[{}] Device not found".format(time.ctime()))
    time.sleep(1)
