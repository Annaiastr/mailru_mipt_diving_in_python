
import sys
from math import sqrt

a, b, c = [int(n) for n in sys.argv[1:]]

discr = b ** 2 - 4 * a * c

x1 = int((-b+sqrt(discr)) / (2*a))
x2 = int((-b-sqrt(discr)) / (2*a))

print(str(x1) + '\n' + str(x2))