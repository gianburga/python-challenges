# -*- coding: utf-8 -*-
"""
PRISONER OR CITIZEN
CHALLENGE DESCRIPTION:

No matter where you are, there are always good and bad people everywhere,
those who have never broken the law, and those who are constantly abusing it.
The goal of our challenge is not to persuade you to obey the laws,
become better, or vice versa. Everyone has a right to make his own life choice.
Your task is to find out where a person is—in jail or at large—depending
on the coordinates.

"""

class Challenge224:
    path_file = './challenge_224.txt'
    coordinate_valid_range = (0, 10)
    coordinates_valid_range = (3, 12)

    def __init__(self, path_file=None):
        if path_file:
            self.path_file = path_file

    def read_file(self):
        f = open(self.path_file, 'r')
        lines = f.readlines()
        return lines

    def parse_point(self, point):
        return float(point)

    def parse_coordinate(self, coordinate):
        x, y = coordinate.strip().split(' ')
        is_valid = self.is_valid_coordinate(x) and self.is_valid_coordinate(y)
        if not is_valid:
            raise ValueError, '`%s` and `%s` are invalid, coordinates are '\
                'from %d to %d and cannot be negative.' % (
                    x, y,
                    self.coordinate_valid_range[0],
                    self.coordinate_valid_range[1]
                )
        return x, y

    def get_polygon(self, coordinates):
        list_coordinates = coordinates.strip().split(',')
        if len(list_coordinates) not in range(*self.coordinates_valid_range):
            raise ValueError, 'the number of coordinates of a prison can be from %d to %d.' % (
                self.coordinates_valid_range[0],
                self.coordinates_valid_range[1]
            )
        return [
            [self.parse_point(point) \
                for point in self.parse_coordinate(coordinate)] \
                    for coordinate in list_coordinates
        ]

    def get_point(self, coordinate):
        return [self.parse_point(point) for point \
            in self.parse_coordinate(coordinate)]

    def is_valid_coordinate(self, coordinate):
        coordinate = float(coordinate)
        coordinate_min, coordinate_max = self.coordinate_valid_range
        return coordinate >= 0 and coordinate in range(coordinate_min, coordinate_max + 1)

    def get_coordinates(self, lines):
        coordinates = []
        for line in lines:
            p1, p2 = line.split('|')
            coordinates.append([
                self.get_polygon(p1),
                self.get_point(p2)
            ])
        return coordinates

    def in_polygon(self, point, polygon):
        """
        * Versión modificada para incluir prisionero si se encuentra en la línea.

        Comprueba si un punto se encuentra dentro de un polígono
        polygon - Lista de tuplas con los puntos que forman los
        vértices [(x1, x2), (x2, y2), ..., (xn, yn)]

        https://sakseiw.wordpress.com/2013/10/04/punto-dentro-de-poligono/
        """
        x, y = point
        j = len(polygon) - 1
        into = False

        if point in polygon:
            return True

        for i, polygon_point in enumerate(polygon):
            if (polygon_point[1] < y and polygon[j][1] >= y) \
               or (polygon[j][1] < y and polygon_point[1] >= y):
                if polygon_point[0] + (y - polygon_point[1]) / (polygon[j][1] - polygon_point[1]) \
                   * (polygon[j][0] - polygon_point[0]) <= x:
                    into = not into
            j = i
        return into

    def play(self):
        lines = self.read_file()
        coordinates = self.get_coordinates(lines)
        for i, coordinate in enumerate(coordinates):
            print 'Case %d' % i
            polygon, point = coordinate
            print 'Prizoner' if self.in_polygon(point, polygon) else 'Citizen'


if __name__ == '__main__':
    challenge = Challenge224()
    challenge.play()
