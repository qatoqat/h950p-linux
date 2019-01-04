import usb
# 256c:006e
dev = usb.core.find(idVendor=0x256c, idProduct=0x006e)

print(dev)

if dev is not None:
    endpoint1 = dev[0][(0, 0)][0]
    endpoint2 = dev[0][(1, 0)][0]
    print(endpoint1)
    print(endpoint2)


