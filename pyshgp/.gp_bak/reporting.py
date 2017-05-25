"""
The :mod:`reporting` module records timings and other reports to be displayed
at the end of a evolutionary run.

.. todo::
    Create more robust system to handle the generation of reports. Write to file
    or database. More than just timings.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime

timings = { "evaluation":[],
            "genetics":[]}
total_errors_in_evalutaion_order = []


def log_timings(stage, start, end):
    """Temporary.
    """
    start = (start-datetime.datetime(1970,1,1)).total_seconds()
    end = (end-datetime.datetime(1970,1,1)).total_seconds()
    timings[stage].append(end - start)

def print_timings():
    """Temporary.
    """
    print("Timings:")
    print("Average Evaluation Timing of Generation:", round(sum(timings['evaluation']) / float(len(timings['evaluation'])), 3))
    print("Average Selection/Variations Timing of Generation:", round(sum(timings['genetics']) / float(len(timings['genetics'])), 3))