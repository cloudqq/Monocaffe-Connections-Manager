# This code is from bob_f in #python at FreeNode
# Thanks!
"""
Small library for making plain text tables
"""

import sys
import itertools

class Table(object):
    def __init__(self, headings=None, rows=None):
        self.headings = headings
        self.rows = rows

    def _formatRows(self):
        maxes = {}
        for row in itertools.chain(self.headings, self.rows):
            for i, v in enumerate(row):
                maxes[i] = max(maxes.get(i, 0), len(v))

        yield self._formatRow(self.headings, maxes)
        yield '-' * (sum(maxes.values()) + (3 * len(maxes)))

        for row in self.rows:
            yield self._formatRow(row, maxes)

    def _formatRow(self, row, maxes):
        return ''.join(
            '%*.*s | ' % (-maxes[i], maxes[i], v)
            for i, v in enumerate(row))

    def render(self):
        for row in self._formatRows():
            yield row

    def output(self, where=sys.stdout):
        for row in self.render():
            where.write(row)
            where.write('\n')

if __name__ == '__main__':
    testHeaders = ['this', 'is', 'a', 'test']
    testRows = [
        ('huetnahntello', 'boom', 'bang', 'beeeef'),
        ('hellaoeuaeuooeuo', 'boom', 'bang', 'boooop'),
        ('hellaoeuaeuooeuo', 'boom', 'hatutneoauhntenbang', 'what'),
        ('hellaoeuaeuooeuo', 'boaeuhtaeuoom', 'bang', 'oh no'),
        ('hellaoeuaeuooeuo', 'boom', 'bang', 'blaaa'),
    ]

    table = Table(testHeaders, testRows)
    table.output()
