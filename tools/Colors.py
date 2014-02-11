# Copyright (c) 2014.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import re

__author__ = 'Edoxile'


class IRCToHTML:
    def __init__(self):
        self.tokens = {
            '\x03': 'color',
            '\x02': 'bold',
            '\x15': 'italic',
            '\x1f': 'underline',
            '\x0f': 'reset'
        }
        self.formats = {
            'bgcolor': '<span style="background-color: #{};">',
            'fgcolor': '<span style="color: #{};">',
            'bold': '<span style="font-weight: bold;">',
            'italic': '<span style="font-style: italic;">',
            'underline': '<span style="text-decoration: underline;">'
        }
        self.colors = [
            'ffffff', '000000', '000088', '008800', 'ff0000', '880000', '880088', 'ff8800', 'ffff00', '00ff00',
            '008888', '00ffff', '0000ff', 'ff00ff', '888888', 'cccccc'
        ]
        self.color_data = re.compile('(\d{1,2})(?:,(\d{1,2}))?')

    def parse(self, line):
        (split, contexts) = self._tokenize(line)
        for i in range(len(split)):
            for c in contexts[i]:
                if c[1]:
                    if 'color' in c[0]:
                        split[i] = self.formats[c[0]].format(self.colors[c[2]]) + split[i]
                    else:
                        split[i] = self.formats[c[0]] + split[i]
                else:
                    split[i-1] += '</span>'
        return ''.join(split)

    def _tokenize(self, line):
        raw = list(line)
        open_contexts = []
        contexts = [[]]
        split = ['']
        i = 0
        while i < len(raw):
            if raw[i] in self.tokens.keys():
                if len(split[-1]):
                    split.append('')
                    contexts.append([])
                if self.tokens[raw[i]] == 'reset':
                    for c in open_contexts.copy():
                        if 'color' not in c[0]:
                            contexts[c[1]].append((c[0], True))
                        else:
                            contexts[c[1]].append((c[0], True, c[2]))
                        contexts[-1] = [(c[0], False)] + contexts[-1]
                        del open_contexts[open_contexts.index(c)]
                elif self.tokens[raw[i]] == 'color':
                    m = self.color_data.match(''.join(raw[i + 1:]))
                    if m:
                        if m.group(2):
                            for c in [c for c in open_contexts.copy() if 'color' in c[0]]:
                                contexts[c[1]].append((c[0], True, c[2]))
                                contexts[-1] = [(c[0], False)] + contexts[-1]
                                del open_contexts[open_contexts.index(c)]
                            open_contexts.append(('fgcolor', len(split) - 1, int(m.group(1))))
                            open_contexts.append(('bgcolor', len(split) - 1, int(m.group(2))))
                        else:
                            for c in [c for c in open_contexts.copy() if c[0] == 'fgcolor']:
                                contexts[c[1]].append((c[0], True, c[2], c[3]))
                                contexts[-1] = [(c[0], False)] + contexts[-1]
                                del open_contexts[open_contexts.index(c)]
                            open_contexts.append(('fgcolor', len(split) - 1, int(m.group(1))))
                        i += len(m.group(0))
                else:
                    open_contexts.append((self.tokens[raw[i]], len(split) - 1))
            else:
                split[-1] += raw[i]
            i += 1
        for c in open_contexts.copy():
            if 'color' not in c[0]:
                contexts[c[1]].append((c[0], True))
            else:
                contexts[c[1]].append((c[0], True, c[2]))
            contexts[-1] = [(c[0], False)] + contexts[-1]
            del open_contexts[open_contexts.index(c)]
        return split, contexts


if __name__ == '__main__':
    #tokenizer = ColorTokenizer('\x02Hoi, \x0312ik \x0312,03ben \x1fKlaas\x0f.')
    irc2html = IRCToHTML()
    parsed = irc2html.parse('\x02Hoi, \x0312ik \x0312,03ben \x1fKlaas\x0f.')
    print(parsed)