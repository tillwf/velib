import math
import numpy as np

def distance(points):
    p0, p1 = points
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
