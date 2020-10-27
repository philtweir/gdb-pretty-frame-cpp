import gdb
import cpp_pretty_frame
import functools

try:
    from itertools import imap
except ImportError:
    imap=map


class CppFrameDecorator(gdb.FrameDecorator.FrameDecorator):

    def __init__(self, fobj, frame_printer):
        super(CppFrameDecorator, self).__init__(fobj)
        self.fobj = fobj
        self.frame_printer = frame_printer

    def function(self):
        frame = self.fobj.inferior_frame()
        name = self.frame_printer.parse_line(str(frame.name()))

        return name


class CppFrameFilter():

    def __init__(self):
        self.name = "C++ frame filter"
        self.priority = 100
        self.enabled = True
        self.frame_printer = cpp_pretty_frame.PrettyFrame()

        gdb.frame_filters[self.name] = self

    def filter(self, frame_iter):
        frame_iter = imap(
            functools.partial(CppFrameDecorator,
                              frame_printer=self.frame_printer),
            frame_iter)

        return frame_iter
