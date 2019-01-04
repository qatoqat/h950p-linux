from Xlib import X
from Xlib.protocol import rq
from sys import stderr
from traceback import print_exc
extname = 'XTEST'


class FakeInput(object):
    _request = rq.Struct(rq.Card8('opcode'),
                         rq.Opcode(2),
                         rq.RequestLength(),
                         rq.Set('event_type', 1, (X.KeyPress,
                                                  X.KeyRelease,
                                                  X.ButtonPress,
                                                  X.ButtonRelease,
                                                  X.MotionNotify)),
                         rq.Card8('detail'),
                         rq.Pad(2),
                         rq.Card32('time'),
                         rq.Window('root', (X.NONE, )),
                         rq.Pad(8),
                         rq.Int16('x'),
                         rq.Int16('y'),
                         rq.Pad(8)
                         )

    def __init__(self, display, onerror = None, *args, **keys):
        self._errorhandler = onerror
        self._binary = self._request.to_binary(*args, **keys)
        self._serial = None
        display.send_request(self, onerror is not None)

    def _set_error(self, error):
        if self._errorhandler is not None:
            return call_error_handler(self._errorhandler, error, self)
        else:
            return 0

def fake_input(self, event_type, detail = 0, time = X.CurrentTime,
               root = X.NONE, x = 0, y = 0):

    FakeInput(display = self.display,
              opcode = self.display.get_extension_major(extname),
              event_type = event_type,
              detail = detail,
              time = time,
              root = root,
              x = x,
              y = y)

def call_error_handler(handler, error, request):
    try:
        return handler(error, request)
    except:
        stderr.write('Exception raised by error handler.\n')
        print_exc()
        return 0
