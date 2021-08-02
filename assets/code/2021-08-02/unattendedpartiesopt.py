""" Unattended parties optimized
Uses a defined number of people to generate a large number
of simulated birthdays, then checks if anyone shares a birthday.
Runs this 100,000 times."""

import random, time, sys
from multiprocessing import Pool

# set random seed for consistency
random.seed(23)

default_bdays = 30
default_processes = 1

# check to see if any arguments were passed in,
# otherwise use default values
if len(sys.argv) == 3:
    # make sure first argument is a decimal
    if sys.argv[1].isdecimal():
        NUM_BDAYS = int(sys.argv[1])
    else: NUM_BDAYS = default_bdays

    # make sure second argument is a decimal
    if sys.argv[2].isdecimal():
        NUM_PROCESSES = int(sys.argv[2])
    else: NUM_PROCESSES = default_processes
else:
    # define constants
    NUM_BDAYS = default_bdays
    NUM_PROCESSES = default_processes

def getBirthdays(n):
    """ n is an integer;
    getBirthdays generates n birthdays for n people,
    returns a list of birthdays of length n """
    birthdays = [random.randint(1,365) for i in range(n)]
    return birthdays

def checkCollisions(dates):
    """ checks a list of integer values for duplicates / collisions """
    if len(set(dates)) == len(dates):
        return False
    else:
        return True

def generateAndCheckBirthdays(n):
    """ generates n dates, and checks the dates for collisions """
    birthdays = getBirthdays(n)
    result = checkCollisions(birthdays)
    if result: return 1
    else: return 0

def main():
    print('''Checking {} random birthdays using
{} process(es) 100,000 times...\n'''.format(NUM_BDAYS, NUM_PROCESSES))

    maplist = [NUM_BDAYS for i in range(100_000)]

    with Pool(NUM_PROCESSES) as p:
        ord_start = time.time()
        resultsord = p.map(generateAndCheckBirthdays, maplist)
        ord_total = time.time() - ord_start
        print('map               {:f} seconds.\n'.format(
            round(ord_total,5)))

        unord_start = time.time()
        resultsunord = p.imap_unordered(generateAndCheckBirthdays, maplist)
        unord_total = time.time() - unord_start
        print('imap_unordered    {:f} seconds.\n'.format(
            round(unord_total,9)))

    time_ratio = ord_total / unord_total
    print('''imap_unordered    {} times faster than map
                  in {}% of the ordered time.\n'''.format(
        round(time_ratio,4),
        round((1/time_ratio)*100,5)))

    total_collisions = sum(resultsord)

    # display simulation results
    probability = round(total_collisions / 100_000 * 100,2)

    print('''{}/100,000 trials had matching birthdays.
Group of {} has a {}% chance of matching birthdays.\n'''.format(
    total_collisions,
    NUM_BDAYS,
    probability))

# if the program is run (instead of imported), run the game
if __name__ == '__main__':
    main()
