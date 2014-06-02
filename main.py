from skimage import io
from numpy import zeros, uint8
__author__ = 'nikolas'
import math
import threading
import cProfile
from multiprocessing import Pool, Process

# class Tile(object):
#
#     # __metaclass__ = TileMeta
#
#     tile_size = None
#     fp = None
#     calc_method = None
#
#     def __init__(self, tile_size, tile_name):
#         self.tile_name = tile_name
#         self.tile_size = tile_size
#         self.fp = zeros((self.tile_size, self.tile_size, 3), dtype=uint8)
#         self.calc_method = calc(tile_name)
#
#
# class SphereToCube(object):
#     tiles = None
#     tile_size = None
#     sphere_image = None
#
#     def __init__(self, image_path, *args):
#         self.tiles = args
#         self.tile_size = self.tiles[0].tile_size
#         self.sphere_image = io.imread(image_path)
#         self.shpere_image_size = self.sphere_image.shape
#         self.pool = Pool(len(self.tiles))
#
#     def convert(self):
#         threads = []
#         self.pool.map(map_tile, [(tile, self.sphere_image) for tile in self.tiles])
#         # for tile in self.tiles:
#         #     sphere_image = self.sphere_image.copy()
#         #     thread = threading.Thread(target=map_tile, args=(tile, sphere_image))
#         #     print 'Thread for tile {} started..'.format(tile.tile_name)
#         #     thread.start()
#         #     threads.append(thread)
#         # [thread.join() for thread in threads]
#
#
# def map_tile(tile, sphere_image):
#         image = []
#         half_size = tile.tile_size / 2
#         rect_x = 0
#         rect_y = 0
#         for tile_y in xrange(1, tile.tile_size):
#             rect_y = float(tile_y) / half_size - 1
#             for tile_x in xrange(1, tile.tile_size):
#                 rect_x = float(tile_x) / half_size - 1
#                 tile.fp[tile_y, tile_x] = process_cords(tile, rect_x, rect_y, sphere_image)
#         io.imsave(tile.tile_name + '.jpg', tile.fp)
#
# def process_cords(tile, rect_x, rect_y, sphere_image):
#
#     x, y, z, pi_shift1, pi_shift2, phi_01, phi_02 = tile.calc_method(rect_x, rect_y)
#
#     theta = math.acos(z / math.sqrt(x**2 + y**2 + z**2))
#     if x != 0:
#         phi = math.atan(y / x)
#         if x > 0:
#             phi = phi + pi_shift1
#         else:
#             phi = phi + pi_shift2
#     else:
#         if y < 0:
#             phi = phi_01
#         else:
#             phi = phi_02
#
#     sphere_height, sphere_width, __channels = sphere_image.shape
#     sp_x = max(round(phi2width(sphere_width, phi) -1), 1)
#     sp_y = max(round(theta2height(sphere_height, theta) -1), 1)
#     # print '{}x{}\n'.format(sp_y, sp_x)
#     return sphere_image[sp_y, sp_x]




def worker(tile_name, tile_size, image_path):

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

        x, y, z, pi_shift1, pi_shift2, phi_01, phi_02 = calc_method(rect_x, rect_y)

        theta = math.acos(z / math.sqrt(x**2 + y**2 + z**2))
        if x != 0:
            phi = math.atan(y / x)
            if x > 0:
                phi = phi + pi_shift1
            else:
                phi = phi + pi_shift2
        else:
            if y < 0:
                phi = phi_01
            else:
                phi = phi_02

        sphere_height, sphere_width, __channels = sphere_image.shape
        sp_x = max(round(phi2width(sphere_width, phi) -1), 1)
        sp_y = max(round(theta2height(sphere_height, theta) -1), 1)
        # print '{}x{}\n'.format(sp_y, sp_x)
        return sphere_image[sp_y, sp_x]

    def calc(tile_name):

        def up(rect_x, rect_y):
            x = -rect_y
            y = -rect_x
            z = 1
            pi_shift1 = math.pi
            pi_shift2 = 0
            phi_01 = math.pi / 2
            phi_02 = - math.pi / 2
            return (x, y, z, pi_shift1, pi_shift2, phi_01, phi_02)

        def down(rect_x, rect_y):
            x = rect_y
            y = -rect_x
            z = -1
            pi_shift1 = math.pi
            pi_shift2 = 0
            phi_01 = math.pi / 2
            phi_02 = - math.pi / 2
            return (x, y, z, pi_shift1, pi_shift2, phi_01, phi_02)

        def front(rect_x, rect_y):
            x = 1
            y = rect_x
            z = - rect_y
            pi_shift1 = 0
            pi_shift2 = 0
            return (x, y, z, pi_shift1, pi_shift2, None, None)

        def right(rect_x, rect_y):
            x = - rect_x
            y = 1
            z = -rect_y
            pi_shift1 = 0
            pi_shift2 = math.pi
            phi_01 = math.pi / 2
            phi_02 = math.pi / 2
            return (x, y, z, pi_shift1, pi_shift2, phi_01, phi_02)

        def back(rect_x, rect_y):
            x = -1
            y = -rect_x
            z = -rect_y
            pi_shift1 = math.pi
            pi_shift2 = math.pi
            return (x, y, z, pi_shift1, pi_shift2, None, None)

        def left(rect_x, rect_y):
            x = rect_x
            y = -1
            z = -rect_y
            pi_shift1 = 0
            pi_shift2 = math.pi
            phi_01 = - math.pi / 2
            phi_02 = - math.pi / 2
            return (x, y, z, pi_shift1, pi_shift2, phi_01, phi_02)

        return locals()[tile_name]
    print 'Process for tile: {} --> started'.format(tile_name)
    tile = zeros((tile_size, tile_size, 3), dtype=uint8)
    half_size = tile_size / 2
    method_for_calc = calc(tile_name)
    sphere_image = io.imread(image_path)
    for tile_y in xrange(1, tile_size):
            rect_y = float(tile_y) / half_size - 1
            for tile_x in xrange(1, tile_size):
                rect_x = float(tile_x) / half_size - 1
                tile[tile_y, tile_x] = process_cords(rect_x, rect_y, sphere_image, method_for_calc)
    io.imsave(tile_name + '.jpg', tile)
    print 'Process for tile: {} --> finished'.format(tile_name)




# import pstats



if __name__ == '__main__':
    import time
    processes = []
    tiles_names = ['up', 'down', 'front', 'right', 'back', 'left']
    start_time = time.time()
    for tile_name in tiles_names:
        process = Process(target=worker, args=(tile_name, 500, 'panorama.jpg'))
        process.start()
        processes.append(process)
    [process.join() for process in processes]
    execution_time = time.time() - start_time
    print 'Execution time is: {}s'.format(execution_time)
    # tiles = [Tile(500, tile_name) for tile_name in tiles_names]
    # cProfile.run("SphereToCube('panorama.jpg', *tiles).convert()", 'profile.pf')
    # SphereToCube('panorama.jpg', *tiles).convert()
    # stats = pstats.Stats('profile.pf')
    # stats.strip_dirs().sort_stats('time').print_stats()





