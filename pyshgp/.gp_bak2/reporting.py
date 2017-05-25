"""
The :mod:`reporting` module records timings and other reports to be displayed
at the end of a evolutionary run.

.. todo::
    Create more robust system to handle the generation of reports. Write to file
    or database. More than just timings.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from prettytable import PrettyTable

class Report:
    """Class that stores a report.
    """

    #: List or tuple of field names recoreded in the report.
    fields = None

    def __init__(self, fields):
        self._num_fields = len(fields)
        self.fields = fields
        self._values = None

    def update(self, *args):
        if len(args) == self._num_fields:
            if self._values is None:
                self._values = np.array(args, dtype='|S32')
            else:
                self._values = np.vstack(
                    (self._values, np.array(args, dtype='|S32'))
                )
                self._values = np.reshape(self._values, (-1, len(self.fields)))
        else:
            raise TypeError('Report update takes exactly ' +
                '{0} fields ({1} given)'.format(self._num_fields, len(args)))

    def show(self):
        pt = PrettyTable(self.fields)
        if not self._values is None:
            if len(self._values) == 0:
                pt.add_row(self._values)
            else:
                np.apply_along_axis( pt.add_row, axis=1, arr=self._values )
        print(pt)

    # def save(self, filename='', database=False):
    #     pass


BASIC_REPORTS = {
    'timings' : ('Generation Number', 'Generation Time', 'Evaluation Time',
        'Genetics Time'),
    'error' : ('Generation Number', '')
}
