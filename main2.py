from multiprocessing import Process
from cache import cache
import numpy as np
from skimage import io
import math


def worker(tile_name, tile_size, image_path):

    def calc(tile_name):

        def up(tile_y, tile_x):
            theta = math_cache['zp'][tile_y, tile_x]
            phi = math_cache['phi'][tile_x, tile_y]
            phi = update_phi(half_size, phi, tile_y, tile_x, math.pi, 0, -math.pi/2, math.pi/2)
            return (theta, phi, )

        def down(tile_y, tile_x):
            theta = math_cache['zm'][tile_y, tile_x]
            phi = math_cache['phi'][tile_x, tile_size - tile_y]
            phi = update_phi(half_size, phi, tile_y, tile_x, 0, math.pi, -math.pi/2, math.pi/2)
            return (theta, phi, )

        def front(tile_y, tile_x):
            theta = math_cache['xypm'][tile_size - tile_y, tile_size - tile_x]
            phi = math_cache['phi'][tile_x, tile_size]
            phi = update_phi(half_size, phi, tile_y, tile_x, 0, 0, -math.pi/2, math.pi/2)
            return (theta, phi, )

        def right(tile_y, tile_x):
            theta = math_cache['xypm'][tile_size - tile_y, tile_size - tile_x]
            phi = math_cache['phi'][tile_size, tile_size - tile_x]
            phi = update_phi(half_size, phi, tile_x, tile_y, 0, math.pi, math.pi/2, math.pi/2)
            return (theta, phi, )

        def back(tile_y, tile_x):
            theta = math_cache['xypm'][tile_size - tile_y, tile_size - tile_x]
            phi = math_cache['phi'][tile_x, tile_size] + math.pi
            return (theta, phi, )

        def left(tile_y, tile_x):
            theta = math_cache['xypm'][tile_size - tile_y, tile_size - tile_x]
            phi = math_cache['phi'][tile_size, tile_size - tile_x]
            phi = update_phi(half_size, phi, tile_x, tile_y, math.pi, 0, -math.pi/2, -math.pi/2)
            return (theta, phi, )

        return locals()[tile_name]

    def update_phi(half_size, phi, major_dir, minor_dir, major_m, major_p, minor_m, minor_p):
        if major_dir < half_size:
            phi = phi + major_m
        elif major_dir > half_size:
            phi = phi + major_p
        elif major_dir < half_size:
            phi = minor_m
        else:
            phi = minor_p
        return phi

    def phi2width(width, phi):
        x = 0.5 * width*(phi/math.pi + 1)
        if x < 1:
            x += width
        elif x > width:
            x -= width
        return x

    def theta2height(height, theta):
        return height * theta / math.pi

    def process_cords(rect_x, rect_y, sphere_image, calc_method):

        theta, phi = calc_method(rect_x, rect_y)
        sphere_height, sphere_width, __channels = sphere_image.shape
        sp_x = max(round(phi2width(sphere_width, phi) -1), 1)
        sp_y = max(round(theta2height(sphere_height, theta) -1), 1)
        # print '{}x{}\n'.format(sp_y, sp_x)
        return sphere_image[sp_y, sp_x]


    print 'Process for tile: {} --> started'.format(tile_name)
    tile = np.zeros((tile_size, tile_size, 3), dtype=np.uint8)
    half_size = tile_size / 2
    method_for_calc = calc(tile_name)
    sphere_image = io.imread(image_path)
    for tile_y in xrange(tile_size):
        for tile_x in xrange(tile_size):
            tile[tile_y, tile_x] = process_cords(tile_x, tile_y, sphere_image, method_for_calc)
    io.imsave('{}.jpg'.format(tile_name), tile)


if __name__ == '__main__':
    import time
    processes = []
    tiles_names = ['up', 'down', 'front', 'right', 'back', 'left']
    tile_size = 64
    start_time = time.time()
    math_cache = cache
    # worker(tiles_names)
    for tile_name in tiles_names:
        worker(tile_name, tile_size, 'panorama.jpg')
        # process = Process(target=worker, args=(tile_name, tile_size, 'panorama.jpg'))
        # process.start()
        # processes.append(process)
    # [process.join() for process in processes]
    execution_time = time.time() - start_time
    print 'Execution time is: {}s'.format(execution_time)
