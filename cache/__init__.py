__author__ = 'nikolas'

import numpy as np
from numpy.ma import arccos, sqrt, arctan


def cache_angles(tile_size=500):
    half_size = float(tile_size - 1) / 2

    get_zp = lambda x, y: arccos(1 / sqrt(x**2 + y**2 + 1))
    get_zm = lambda x, y: arccos(-1 / sqrt(x**2 + y**2 + 1))
    get_xypm = lambda x, y: arccos(y / sqrt(x**2 + y**2 + 1))
    get_phi = lambda x, y: arctan(float(y) / x)

    cache = {
        'zp': np.zeros((tile_size, tile_size, ), dtype=np.float),
        'zm': np.zeros((tile_size, tile_size, ), dtype=np.float),
        'xypm': np.zeros((tile_size, tile_size, ), dtype=np.float),
        'phi': np.zeros((tile_size, tile_size, ), dtype=np.float)
    }
    print 'Perform cache angles...'
    for tile_y in xrange(tile_size):
        y = float(tile_y) / half_size - 1
        for tile_x in xrange(tile_size):
            x = float(tile_x) / half_size - 1
            cache['zp'][tile_y, tile_x] = get_zp(x, y)
            cache['zm'][tile_y, tile_x] = get_zm(x, y)
            cache['xypm'][tile_y, tile_x] = get_xypm(x, y)
            if x != 0:
                cache['phi'][tile_y, tile_x] = get_phi(x, y)
            # print 'cache for: [{}, {}] -> [{},{}]'.format(tile_y, tile_x, y, x)
    return cache


cache = cache_angles(512)