#!/usr/bin/env python3

# CC-BY-SA: Author Phil Weir <phil.weir@numa.ie>
# With thanks to Paul McGuire:
# http://stackoverflow.com/questions/4801403/how-can-i-use-pyparsing-to-parse-nested-expressions-that-have-mutiple-opener-clo

import fileinput
import cpp_pretty_frame

printer = cpp_pretty_frame.PrettyFrame()

line = ''
for line in fileinput.input():
    printer.parse_line('<%s>' % line)
