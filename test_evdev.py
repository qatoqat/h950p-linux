from evdev import UInput, InputEvent, AbsInfo, ecodes
import time


ev = InputEvent(1334414993, 274296, ecodes.EV_ABS, ecodes.ABS_X, 1)
ey = InputEvent(1334414993, 274296, ecodes.EV_ABS, ecodes.ABS_X, 1)
time.sleep(2)
with UInput() as ui:
   ui.write_event(ev)
   ui.write_event(ey)
   ui.syn()

#
# cap = {
#     e.EV_KEY: [e.KEY_A, e.KEY_B],
#     e.EV_ABS: [
#         (e.ABS_X, AbsInfo(value=0, min=0, max=255,
#                           fuzz=0, flat=0, resolution=0)),
#         (e.ABS_Y, AbsInfo(0, 0, 255, 0, 0, 0)),
#         (e.ABS_MT_POSITION_X, (0, 128, 255, 0))]
# }
#
# ui = UInput(cap, name='example-device', version=0x3)
# print(ui)
# """
# name
# "example-device", bus
# "BUS_USB", vendor
# "0001", product
# "0001", version
# "0003"
# event
# types: EV_KEY
# EV_ABS
# EV_SYN
# """
#
# print(ui.capabilities())
#
# # move mouse cursor
# ui.write(e.EV_ABS, e.ABS_X, 20)
# ui.write(e.EV_ABS, e.ABS_Y, 20)
# ui.write(e.EV_KEY, e.KEY_B, 1)
# ui.write(e.EV_KEY, e.KEY_B, 0)
# time.sleep(1)
# ui.syn()
# # from evdev import UInput, AbsInfo, ecodes
# # import time
# #
# #
# # cap_pen = {
# #     ecodes.EV_KEY: [ecodes.BTN_TOUCH, ecodes.BTN_TOOL_PEN, ecodes.BTN_MOUSE, ecodes.BTN_LEFT, ecodes.BTN_RIGHT,
# #                     ecodes.BTN_MIDDLE],
# #     ecodes.EV_ABS: [
# #         (ecodes.ABS_X, AbsInfo(0, 0, 44000, 0, 0, 5080)),  # value, min, max, fuzz, flat, resolution
# #         (ecodes.ABS_Y, AbsInfo(0, 0, 27300, 0, 0, 5080)),
# #         (ecodes.ABS_PRESSURE, AbsInfo(0, 0, 8192, 0, 0, 0)), ] # ,
# #     # ecodes.EV_MSC: [ecodes.MSC_SCAN], #not sure why, but it appears to be needed
# # }
# #
# # EV_ABS = 3
# # EV_CNT = 32
# # EV_FF = 21
# #
# # ABS_X = 0
# # ABS_Y = 1
# # ABS_Z = 2
# #
# # ABS_MT_DISTANCE = 59
# # ABS_MT_ORIENTATION = 52
# #
# # ABS_MT_POSITION_X = 53
# # ABS_MT_POSITION_Y = 54
# #
# # ABS_MT_PRESSURE = 58
# # ABS_MT_SLOT = 47
# #
# # while True:
# #     ui = UInput(cap_pen, "meow", 3)
# #     ui.write(ecodes.EV_ABS, ecodes.ABS_X, 100)
# #     ui.write(ecodes.EV_ABS, ecodes.ABS_Y, 100)
# #     ui.syn()
# #     ui.close()
