#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   gaofei
#   Date    :   18/1/24 17:16:21
#   Desc    :

import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        return self.plus(v)

    def __getitem__(self, *args):
        return self.coordinates.__getitem__(*args)

    def __iter__(self, *args):
        return self.coordinates.__iter__(*args)

    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    # length
    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return sum(coordinates_squared).sqrt()

    # unit
    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/magnitude)
        except ZeroDivisionError:
            raise Exception("Cannot normalized zero vector")

    # 点积，内积
    def dot(self, v):
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])

    def dot_geometry(self, v):
        radians = self.angle_with(v)
        return self.magnitude() * v.magnitude() * Decimal(math.cos(radians))

    # 夹角
    def angle_with(self, v, in_dgrees = False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            # print "self:%s,v:%s,u1:%s,u2:%s,u1.dot(u2):%s" % (self, v, u1, u2, u1.dot(u2))
            angle_in_radians = math.acos(u1.dot(u2))
            if in_dgrees:
                return angle_in_radians * 180./math.pi
            else:
                return angle_in_radians
        except Exception as e:
            raise e

    # 平行投影
    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            raise e

    # 垂直投影
    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            raise e

    # 正交
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    # 平行
    def is_parallel_to(self, v):
        return (self.is_zero() or
            v.is_zero() or
            self.angle_with(v) == 0 or
            self.angle_with(v) == math.pi)

    # 叉积. only 3D allowed
    def cross(self, v):
        if len(self.coordinates) != len(v.coordinates):
            raise Exception("Not same dimension")
        if len(self.coordinates) > 3:
            raise Exception("dimension>3")
        while len(self.coordinates) < 3:
            self.coordinates = self.coordinates + ('0',)
            v.coordinates = v.coordinates + ('0',)
        
        x_1, y_1, z_1 = self.coordinates
        x_2, y_2, z_2 = v.coordinates
        new_coordinates = [ y_1*z_2 - y_2*z_1,
                            -(x_1*z_2 - x_2*z_1),
                            x_1*y_2 - x_2*y_1   ]
        return Vector(new_coordinates)

    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    # 零向量
    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance


def vector_pos_relation(v, w):
    if v.is_orthogonal_to(w):
        print "orthogonal:", v, w
    elif v.is_parallel_to(w):
        print "parallel:", v, w
    else:
        print "not orthogonal or parallel:", v, w

if '__main__' == __name__:
    v = Vector([1,2])
    w = Vector([3,4])
    print v.plus(w)
    print v+w
    print "magnitude:", w.magnitude()
    print "normalize:", w.normalized()
    v = Vector(['7.887', '4.138'])
    w = Vector(['-8.802', '6.776'])
    print "dot.", v.dot(w)
    print "dot_geometry:", v.dot_geometry(w)

    v = Vector(['3.183', '-7.627'])
    w = Vector(['-2.668', '5.319'])
    print "angle_with.", v.angle_with(w)

    v = Vector(['7.35', '0.221', '5.188'])
    w = Vector(['2.751', '8.259', '3.985'])
    print "angle_with,in_degree.", v.angle_with(w, True)

    v = Vector(['-7.579', '-7.88'])
    w = Vector(['22.737', '23.64'])
    vector_pos_relation(v, w)

    # getcontext().prec = 8
    v = Vector(['3.039', '1.879'])
    w = Vector(['0.825', '2.036'])
    print "component parallel:", v.component_parallel_to(w)

    v = Vector(['-9.88', '-3.264', '-8.159'])
    w = Vector(['-2.155', '-9.353', '-9.473'])
    print "component orthgonal:", v.component_orthogonal_to(w)

    v = Vector(['8.462', '7.893', '-8.187'])
    w = Vector(['6.984', '-5.975', '4.778'])
    print 'cross:', v.cross(w)

    v = Vector(['1.5', '9.547', '3.691'])
    w = Vector(['-6.007', '0.124', '5.772'])
    print 'triangle:', v.area_of_triangle_with(w)
