__author__ = 'nikolas'

import numpy as np
from numpy.ma import arccos, sqrt, arctan


def cache_angles(tile_size=500):
    _range = tile_size - 1
    half_size = _range / 2

    get_zp = lambda x, y: arccos(1 / sqrt(x**2 + y**2 + 1))
    get_zm = lambda x, y: arccos(-1 / sqrt(x**2 + y**2 + 1))
    get_xypm = lambda x, y: arccos(y / sqrt(x**2 + y**2 + 1))
    get_phi = lambda x, y: arctan(float(y) / x)

    cache = {
        'zp': np.zeros((tile_size, tile_size, ), dtype=np.int8),
        'zm': np.zeros((tile_size, tile_size, ), dtype=np.int8),
        'xypm': np.zeros((tile_size, tile_size, ), dtype=np.int8),
        'phi': np.zeros((tile_size, tile_size, ), dtype=np.int8)
    }
    print 'Perform cache angles...'
    for tile_y in xrange(_range):
        y = float(tile_y) / half_size - 1
        for tile_x in xrange(_range):
            x = float(tile_x) / half_size - 1
            cache['zp'][tile_y, tile_x] = get_zp(x, y)
            cache['zm'][tile_y, tile_x] = get_zm(x, y)
            cache['xypm'][tile_y, tile_x] = get_xypm(x, y)
            if x != 0:
                cache['phi'][tile_y, tile_x] = get_phi(x, y)
            print 'cache for: [{}, {}]'.format(tile_y, tile_x)
    return cache


cache = cache_angles(64)