#!/usr/bin/env python

from itertools import product
from pprint import pformat
import argparse
import logging
import sys

GEAR_TYPES = (1.0, 8.0, 12.0, 16.0, 20.0, 24.0, 36.0, 40.0, 56.0)

MIN_GEARS = 2
MAX_GEARS = 8

# http://codereview.stackexchange.com/questions/66450/simplify-a-fraction
def greatest_common_divisor(a, b):
    """
    Return the greatest common divisor of a and b
    """
    while b:
        a, b = b, a % b
    return a


def simplify_fraction(numerator, denominator):
    """
    Divide the numerator and denominator by their greatest common divisor
    """
    gcd = greatest_common_divisor(numerator, denominator)
    return (int(numerator/gcd), int(denominator/gcd))


def fraction_to_one(x, y):

    # Make either x or y so that instead of saying "27:2" we say "13.5:1"
    if x != 1 and y != 1:
        if x > y:
            x = float(x/y)
            y = 1
        else:
            y = float(y/x)
            x = 1

    return (x, y)


def find_gear_train_ratio(gears):
    """
    Given a tuple of gears return the gear ratio for the entire train. This is
    done by multiplying a series of fractions...say you have gears A,B,C,D.
    The ratio for the entire train is A/B * C/D
    """

    # Build a list of all of the ratios for every other pair of gears
    ratios = []
    prev_gear = gears[0]

    for gear in gears[1:]:
        if prev_gear:

            # A worm gear cannot be a follower
            if gear == 1.0:
                return None

            # A work gear cannot easily drive a 36 tooth gear, it doesn't line up
            if prev_gear == 1.0 and gear == 36.0:
                return None

            # Skip any gear train that use 1:1 pairs of gears
            if gear == prev_gear:
                return None

            ratios.append(simplify_fraction(prev_gear, gear))
            prev_gear = None
        else:
            prev_gear = gear

    # Mulitple all of the numerators and all of the denominators
    ratio_x = 1
    ratio_y = 1

    for (x, y) in ratios:
        ratio_x *= x
        ratio_y *= y

    # Reduce the fraction
    (ratio_x, ratio_y) = simplify_fraction(ratio_x, ratio_y)
    # (ratio_x, ratio_y) = fraction_to_one(ratio_x, ratio_y)

    #log.info("ratios: %s, gear train ratio %d/%d" % (ratios, ratio_x, ratio_y))
    return (ratio_x, ratio_y)


def gear_train_string(gt):
    result = []
    prev_x = None

    # dwalton - stopped here...make:
    # "1:24 24:36" print as "1:24:36"
    for (i, x) in enumerate(gt):
        if prev_x is None or x != prev_x or True:
            result.append("%d" % int(x))

        if i % 2:
            result.append(" ")
        else:
            result.append (":")

        prev_x = x
    return ''.join(result)


def find_gear_train(x, y):
    """
    Given a desired gear ratio of x:y return a tuple of gears
    that provide that ratio
    """

    assert MAX_GEARS % 2 == 0, "MAX_GEARS must be a multiple of two"
    closest_delta = None
    closest_ratio = None
    closest_gears = None
    target_ratio_fraction = float(x/y)
    results = []

    # Work through every permutation starting with MIN_GEARS all the way up to
    # MAX_GEARS. We work with gears in pairs so iterate by 2.
    #
    # Return as soon as we find a solution because that will be the
    # answer that takes the minimum number # of gears.
    for number_of_gears in xrange(MIN_GEARS, MAX_GEARS+1, 2):

        # itertools.product() allows for gears to repeat which is what we want
        # since most own several copies of a particular gear.
        # itertools.permutations() does not allow for repetitions.
        for gears in product(GEAR_TYPES, repeat=number_of_gears):
            ratio = find_gear_train_ratio(gears)

            if ratio:
                if ratio[0] == x and ratio[1] == y:
                    results.append((True, ratio, gears))
                else:
                    ratio_fraction = float(ratio[0]/ratio[1])
                    delta = abs(ratio_fraction - target_ratio_fraction)

                    if closest_delta is None or delta < closest_delta:
                        closest_delta = delta
                        closest_ratio = ratio
                        closest_gears = gears
                        log.debug("New Closest: ratio %d:%d, gear train %s" %
                                  (ratio[0], ratio[1], gear_train_string(gears)))

        if results:
            return results

    results.append((False, closest_ratio, closest_gears))
    return results


if __name__ == '__main__':
    # Need 316800:1
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)5s: %(message)s')

    # Color the errors and warnings in red
    logging.addLevelName(logging.ERROR, "\033[91m  %s\033[0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.WARNING, "\033[91m%s\033[0m" % logging.getLevelName(logging.WARNING))
    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser("Lego Gear Calculator")
    parser.add_argument('numberX', type=float, help='The x in x:y gear ratio')
    parser.add_argument('numberY', type=float, help='The y in x:y gear ratio')
    args = parser.parse_args()

    # If the user says they want 6:2 reduce that to 3:1
    (numberX, numberY) = simplify_fraction(args.numberX, args.numberY)
    # (numberX, numberY) = fraction_to_one(numberX, numberY)

    if numberX != args.numberX or numberY != args.numberY:
        print "NOTE: %d:%d reduces to %s:%s" % (args.numberX, args.numberY, numberX, numberY)

    first = True
    printed = []

    for (exact, ratio, gt) in find_gear_train(numberX, numberY):

        if first:
            print "\nRatio: %s:%s" % (ratio[0], ratio[1])
            first = False

            if exact:
                print "\nSolutions"
                print "========="
            else:
                print "Could not find an exact match...best result:\n"

        # 1:8 8:36 vs 8:36 1:8 have the same end result so only
        # print one of them
        gt_sorted = sorted(gt)
        if gt_sorted not in printed:
            gt_string = gear_train_string(gt)
            print "Gear Train: %s" % gt_string
            printed.append(gt_sorted)
    print ''
