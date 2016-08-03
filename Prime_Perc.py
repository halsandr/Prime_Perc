import time
import sys
import os
import getopt
import math
# from multiprocessing import Pool, cpu_count
from multiprocess import Pool, cpu_count


class PrimePercCalculator:
    one, three, seven, nine = 0, 0, 0, 0

    @staticmethod
    def _try_composite(a, d, n, s):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True  # n is definitely composite

    def is_prime(self, n, _precision_for_huge_n=16):
        if n in self._known_primes or n in (0, 1):
            return True
        if any((n % p) == 0 for p in self._known_primes):
            return False
        d, s = n - 1, 0
        while not d % 2:
            d, s = d >> 1, s + 1
        # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
        if n < 1373653:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3))
        if n < 25326001:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5))
        if n < 118670087467:
            if n == 3215031751:
                return False
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7))
        if n < 2152302898747:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
        if n < 3474749660383:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
        if n < 341550071728321:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
        # otherwise
        return not any(self._try_composite(a, d, n, s)
                       for a in self._known_primes[:_precision_for_huge_n])

    def __init__(self, minimum_prime, maximum_prime):
        self.maximum_prime = maximum_prime
        self.minimum_prime = minimum_prime
        self._known_primes = [2, 3]
        self._known_primes += [x for x in range(5, 1000, 2) if self.is_prime(x)]

    def prime_calculator(self, start, stop):
        n_one, n_three, n_seven, n_nine = 0, 0, 0, 0
        for x in range(start, stop):
            if self.is_prime(x):
                if x % 10 == 1:
                    n_one += 1
                elif x % 10 == 3:
                    n_three += 1
                elif x % 10 == 7:
                    n_seven += 1
                elif x % 10 == 9:
                    n_nine += 1
                else:
                    continue
            else:
                continue
        return (n_one, n_three, n_seven, n_nine)

    def update_num(self, list_of):
        n_one, n_three, n_seven, n_nine = list_of
        self.one += n_one
        self.three += n_three
        self.seven += n_seven
        self.nine += n_nine

    def prime_calculate(self):
        break_points = []  # List that will have start and stopping points
        for i in range(cores):  # Creates start and stopping points based on length of range_finish
            break_points.append(
                {"start": int(math.ceil(((self.maximum_prime + 1) + 0.0) / cores * i)),
                 "stop": int(math.ceil(((self.maximum_prime + 1) + 0.0) / cores * (i + 1)))})

        p = Pool(cores)  # Number of processes to create.
        for i in break_points:  # Cycles though the breakpoints list created above.
            a = p.apply_async(self.prime_calculator, kwds=i, args=tuple(),
                              callback=self.update_num)  # This will start the separate processes.
        p.close()  # Prevents any more processes being started
        p.join()  # Waits for worker process to end

    def rounder(self, n):
        return round((100 / ((self.one + self.three + self.seven + self.nine + 0.0) / n)), 2)

    def result(self):
        try:
            perc_sum, count_sum = 0, 0
            for i in (self.one, self.three, self.seven, self.nine):
                count_sum += i
                perc_sum += self.rounder(i)
            print "\n" + "one" + "\t" + "= %.2f" % self.rounder(self.one) + "%" + "\t" + "(%i)" % self.one
            print "three" + "\t" + "= %.2f" % self.rounder(self.three) + "%" + "\t" + "(%i)" % self.three
            print "seven" + "\t" + "= %.2f" % self.rounder(self.seven) + "%" + "\t" + "(%i)" % self.seven
            print "nine" + "\t" + "= %.2f" % self.rounder(self.nine) + "%" + "\t" + "(%i)" % self.nine
            print "\n" + "Sum" + "\t" + "= %.2f" % perc_sum + "%" + "\t" + "(%i)" % count_sum
        except ZeroDivisionError:
            print "\nNo primes found!"


if __name__ == '__main__':

    cores = cpu_count()


    def screen_clear():  # Small function for clearing the screen on Unix or Windows
        if os.name == 'nt':
            return os.system('cls')
        else:
            return os.system('clear')


    def usage():  # any incorrect input will display the usage instructions
        screen_clear()
        print """Prime_Perc.py
    Version 0.1 - Written by Halsandr

    =======
    Usage
    =======

    	Prime_Perc.py -n 1000000

    =======
    Options
    =======

    	-n,	What number you want to search up to

    	"""
        sys.exit(2)


    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:")
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ("-n"):
            up_lim = int(arg)

    try:
        if not up_lim:
            usage()
    except NameError:
        usage()

    time1 = time.time()

    run_prime = PrimePercCalculator(5, up_lim)
    run_prime.prime_calculate()
    run_prime.result()

    time2 = time.time()
    time_total = time2 - time1

    if time_total < 1:
        print "\n" + "Completed in less that 1 second"
    else:
        print "\n" + "Completed in %i seconds" % time_total
