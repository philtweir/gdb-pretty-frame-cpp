#!/usr/bin/env python3

# This file:
# CC-BY-SA: Author Phil Weir <phil.weir@numa.ie>
# With thanks to Paul McGuire:
# http://stackoverflow.com/questions/4801403/how-can-i-use-pyparsing-to-parse-nested-expressions-that-have-mutiple-opener-clo

import colorama
import pyparsing as pyp


def _indent(text, indent):
    return indent + ('\n' + indent).join(text.split('\n'))


def _color_wrap(c, text):
    return c + text + colorama.Style.RESET_ALL


class PrettyFrame:
    types = ['auto', 'bool', 'char', 'double', 'float', 'int', 'long', 'short']
    keywords = ['const', 'mutable', 'public', 'private', 'protected',
                'virtual']
    redwords = ['null', 'true', 'false']
    known_namespaces = ['std', 'boost']

    def __init__(self):
        self.enclosed = pyp.Forward()
        nestedAngles = pyp.nestedExpr('<', '>', content=self.enclosed)
        self.enclosed << (pyp.Word('_' + pyp.alphanums) | '{' | '}' |
                          '(' | ')' | '*' | '&' | ',' | pyp.Word("::") |
                          nestedAngles)

    def format_nested(self, nested, level=0):
        formatted = ''
        sublevels = False
        segments = []
        flat_segments = []
        name = []
        for tok in nested:
            if isinstance(tok, list):
                sublevels = True
                name.append(self.format_nested(tok, level + 1))
            elif tok == ',':
                if name:
                    segments.append(name)
                name = []
            else:
                if tok in self.redwords:
                    tok = _color_wrap(colorama.Fore.RED, tok)
                elif tok in self.keywords:
                    tok = _color_wrap(colorama.Fore.BLUE, tok)
                elif tok in self.types:
                    tok = _color_wrap(colorama.Fore.MAGENTA, tok)
                name.append(tok)

        segments.append(name)
        multiline = False

        for segment in segments:
            if not segment:
                continue
            if isinstance(segment, list):
                if segment[0] not in self.known_namespaces and '::' in segment:
                    sep = len(segment) - segment[-1::-1].index('::') - 1
                    segment[sep + 1] = _color_wrap(colorama.Fore.YELLOW,
                                                   segment[sep + 1])
                flat_segment = ''.join(segment)
                if segment[0] in self.known_namespaces:
                    flat_segment = _color_wrap(colorama.Fore.CYAN,
                                               flat_segment)
            else:
                flat_segment = segment

            if '\n' in flat_segment:
                multiline = True

            flat_segments.append(flat_segment)

        formatted += (',\n' if multiline else ', ').join(flat_segments)

        indent = _color_wrap(colorama.Style.DIM, '  ' if level % 4 else '| ')

        if sublevels:
            formatted = '<\n%s\n>' % _indent(formatted, indent)
        else:
            formatted = '<%s>' % formatted
        formatted = _color_wrap(colorama.Style.RESET_ALL, formatted)
        return formatted

    def parse_line(self, line):
        e = None
        was_missing_end_bracket = True
        added_brackets = 0
        while was_missing_end_bracket:
            was_missing_end_bracket = False

            try:
                nested = self.enclosed.parseString('<%s>' % line)[0]
            except Exception as e:
                if str(e).startswith('Expected ">"'):
                    was_missing_end_bracket = True
                    line += '>'
                    added_brackets += 1
                else:
                    print(e)
                nested = []

        return self.format_nested([] if nested == [] else nested.asList())
