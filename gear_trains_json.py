#!/usr/bin/env python3

"""
Write gear trains to a json file
"""

from gear_calculator import find_gear_train_ratio, gear_train_string, GEAR_TYPES
from itertools import product
from pprint import pformat
import json
import logging


MIN_GEARS = 2
MAX_GEARS = 6

assert MAX_GEARS % 2 == 0, "MAX_GEARS must be a multiple of two"


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)5s: %(message)s')

# Color the errors and warnings in red
logging.addLevelName(logging.ERROR, "\033[91m  %s\033[0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.WARNING, "\033[91m%s\033[0m" % logging.getLevelName(logging.WARNING))
log = logging.getLogger(__name__)

results = {}
total = 0

# dwalton
# min 2 max 2 produces 49 ratios, 63 gear trains, takes 55ms
# min 2 max 4 produces 465 ratios, 4032 gear trains, takes 104ms
# min 2 max 6 produces 1974 ratios, 254079 gear trains, takes 4000ms
# min 2 max 8 produces keys, takes Xms

# Work through every permutation starting with MIN_GEARS all the way up to
# MAX_GEARS. We work with gears in pairs so iterate by 2.
#
# Return as soon as we find a solution because that will be the
# answer that takes the minimum number # of gears.
for number_of_gears in range(MIN_GEARS, MAX_GEARS+1, 2):

    # itertools.product() allows for gears to repeat which is what we want
    # since most own several copies of a particular gear.
    # itertools.permutations() does not allow for repetitions.
    for gear_train in product(GEAR_TYPES, repeat=number_of_gears):
        ratio = find_gear_train_ratio(gear_train)
        if ratio is not None:
            # gear_trains.append((ratio, gear_train))

            gt_tuple = gear_train_string(gear_train).strip().split()
            ratio_as_string = "%d:%d" % (ratio[0], ratio[1])

            if ratio_as_string not in results:
                results[ratio_as_string] = []

            results[ratio_as_string].append(gt_tuple)
            total += 1

with open('gear_trains.json', 'w') as fh:
    json.dump(results, fh, indent=4)

print("%d gear ratios, %d gear trains" % (len(results.keys()), total))
