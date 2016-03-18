#!/usr/bin/env python3

# CC-BY-SA: Author Phil Weir <phil.weir@numa.ie>
# With thanks to Paul McGuire:
# http://stackoverflow.com/questions/4801403/how-can-i-use-pyparsing-to-parse-nested-expressions-that-have-mutiple-opener-clo

import colorama
import fileinput
import textwrap
import pyparsing as pyp

enclosed = pyp.Forward()
nestedAngles = pyp.nestedExpr('<', '>', content=enclosed)
enclosed << (pyp.Word('_' + pyp.alphanums) | '{' | '}' | '(' | ')' | '*' | '&' | ',' | pyp.Word("::") | nestedAngles)

types = ['auto', 'bool', 'char', 'double', 'float', 'int', 'long', 'short']
keywords = ['const', 'mutable', 'public', 'private', 'protected', 'virtual']
redwords = ['null', 'true', 'false']
known_namespaces = ['std', 'boost']


def format_nested(nested, level=0):
    formatted = ''
    sublevels = False
    segments = []
    flat_segments = []
    name = []
    for tok in nested:
        if isinstance(tok, list):
            sublevels = True
            name.append(format_nested(tok, level + 1))
        elif tok == ',':
            if name:
                segments.append(name)
            name = []
        else:
            if tok in redwords:
                tok = colorama.Fore.RED + tok + colorama.Style.RESET_ALL
            elif tok in keywords:
                tok = colorama.Fore.BLUE + tok + colorama.Style.RESET_ALL
            elif tok in types:
                tok = colorama.Fore.MAGENTA + tok + colorama.Style.RESET_ALL
            name.append(tok)

    segments.append(name)
    multiline = False

    for segment in segments:
        if not segment:
            continue
        if isinstance(segment, list):
            if segment[0] not in known_namespaces and '::' in segment:
                sep = len(segment) - segment[-1::-1].index('::') - 1
                segment[sep + 1] = colorama.Fore.YELLOW + segment[sep + 1] + colorama.Style.RESET_ALL
            flat_segment = ''.join(segment)
            if segment[0] in known_namespaces:
                flat_segment = colorama.Fore.CYAN + flat_segment + colorama.Style.RESET_ALL
        else:
            flat_segment = segment

        if '\n' in flat_segment:
            multiline = True

        flat_segments.append(flat_segment)

    formatted += (',\n' if multiline else ', ').join(flat_segments)

    indent = colorama.Style.DIM + ('  ' if level % 4 else '| ') + colorama.Style.RESET_ALL

    if sublevels:
        formatted = '<\n%s\n>' % textwrap.indent(formatted, indent)
    else:
        formatted = '<%s>' % formatted
    formatted = colorama.Style.RESET_ALL + formatted + colorama.Style.RESET_ALL
    return formatted


def parse_line(line):
    e = None
    was_missing_end_bracket = True
    added_brackets = 0
    while was_missing_end_bracket:
        was_missing_end_bracket = False

        try:
            nested = enclosed.parseString(line)
        except Exception as e:
            if str(e).startswith('Expected ">"'):
                was_missing_end_bracket = True
                line += '>'
                added_brackets += 1
            else:
                print(e)
            nested = []

    print("Parsed")
    print(format_nested(nested.asList()))
    print(added_brackets)

line = ''
for line in fileinput.input():
    parse_line('<%s>' % line)
