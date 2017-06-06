#!/usr/bin/python

import sys
import time
from datetime import datetime, timedelta


def _usage():
    print """
Usage: ./gen_freq.py [Start time "YYYYMMDDHHmm"] [End time "YYYYMMDDHHmm"] [Fequency "5m,15m,hourly,daily"] [Output "s" for single line or "l" for list]
"""


def gen_timestamp(start_time, end_time, frequency):
    _ts = []
    _delta = {
        '5m': 300,
        '15m': 900,
        '30m': 1800,
        '45m': 2700,
        'hourly': 3600,
        'daily': 86400,
        'weekly': 604800,
        'monthly': 2592000,
    }
    _time_format = {
        '5m': '%Y%m%d%H%M',
        '15m': '%Y%m%d%H%M',
        '30m': '%Y%m%d%H%M',
        '45m': '%Y%m%d%H%M',
        'hourly': '%Y%m%d%H',
        'daily': '%Y%m%d',
        'weekly': '%Y%m%d',
        'monthly': '%Y%m',
    }

    if not int(end_time) > int(start_time):
        print "End time has to be greater then start time." + end_time + ":" + start_time
        raise

    if frequency in ['hourly', 'mth']:
        start_corrected = start_time[0:-2] + '00'
        end_corrected = end_time[0:-2] + '59'
    elif frequency in ['daily', 'mtd', 'weekly']:
        start_corrected = start_time[0:-4] + '0000'
        end_corrected = end_time[0:-4] + '2359'
    else:
        start_corrected = start_time
        end_corrected = end_time

    e_start = int(time.mktime(time.strptime(start_corrected, "%Y%m%d%H%M")))
    e_end = int(time.mktime(time.strptime(end_corrected, "%Y%m%d%H%M")))
    _ts.append(datetime.fromtimestamp(e_start).strftime(_time_format[frequency]))

    while True:
        e_start = e_start + int(_delta[frequency])
        if not e_start > e_end:
            _ts.append(datetime.fromtimestamp(e_start).strftime(_time_format[frequency]))
        else:
            break

    return _ts


if __name__ == "__main__":
    if len(sys.argv) <= 4:
        _usage()
    else:
        if str(sys.argv[4]) == 'l':
            for _freq in gen_timestamp(sys.argv[1], sys.argv[2], sys.argv[3]):
                print _freq
        elif str(sys.argv[4]) == 's':
            print ','.join(gen_timestamp(sys.argv[1], sys.argv[2], sys.argv[3]))
        else:
            _usage()
