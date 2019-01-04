from evdev import ecodes
import time
# handlers for gesture actions

def btn1(vbtn): #eyedropper
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.syn()

def btn2(vbtn): #eraser
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_E, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_E, 0)
	vbtn.syn()

def btn3(vbtn): #pan (space)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 1)
	vbtn.syn()

	#save
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_S, 1)
	# vbtn.syn()

	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_S, 0)
	# vbtn.syn()

def btn4(vbtn): #pen size
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
	vbtn.syn()

def btn5(vbtn): #redo
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 0)

def btn6(vbtn): #zoom in
	vbtn.write(ecodes.EV_REL, ecodes.REL_WHEEL, 1)
	vbtn.syn()

def btn7(vbtn): #zoom out
	vbtn.write(ecodes.EV_REL, ecodes.REL_WHEEL, -1)
	vbtn.syn()

def btn8(vbtn): #undo
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 0)
	vbtn.syn()


def btn0(vbtn):
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)
	vbtn.syn()


def styl1(vbtn): #stylus 1 right click
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_RIGHT, 273)
	vbtn.syn()

def styl2(vbtn): #stylus 2 middle click
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_MIDDLE, 273)
	vbtn.syn()

def styl10(vbtn):
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_RIGHT, 0)
	vbtn.syn()

def styl20(vbtn):
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_MIDDLE, 0)
	vbtn.syn()
