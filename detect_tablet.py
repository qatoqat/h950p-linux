import usb.core as core
def detect_tablet():
    try:
        dev  = core.find(idVendor=0x256c, idProduct=0x006e)
        return True if dev is not None else False
    except Exception as e:
        print("An error has occurred upon detecting device: {}".format(e))
    return False

print(detect_tablet())