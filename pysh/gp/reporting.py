from __future__ import absolute_import, division, print_function, unicode_literals

import datetime

timings = { "evaluation":[],
            "genetics":[]}
total_errors_in_evalutaion_order = []


def log_timings(stage, start, end):
    start = (start-datetime.datetime(1970,1,1)).total_seconds()
    end = (end-datetime.datetime(1970,1,1)).total_seconds()
    timings[stage].append(end - start)

def print_timings():
    print("Timings:")
    print("Average Evaluation Timing of Generation:", round(sum(timings['evaluation']) / float(len(timings['evaluation'])), 3))
    print("Average Selection/Variations Timing of Generation:", round(sum(timings['genetics']) / float(len(timings['genetics'])), 3))