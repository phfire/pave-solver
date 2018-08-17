#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
from DATA_elastic_modules import elatic_modules_polylines
from DATA_opan_napr_mejd import *


class Polyline:
    def __init__(self, z, defaultDegree):
        self.z = z
        self.xArr = []
        self.yArr = []
        self.defaultDegree = defaultDegree

    def getLeftY(self):
        if self.xArr[0] > self.xArr[-1]:
            return self.yArr[-1]
        else:
            return self.yArr[0]

    def solve_y(self, x):
        xArr = np.array(self.xArr)
        yArr = np.array(self.yArr)
        polynom, res, _, _, _ = np.polyfit(xArr, yArr, self.defaultDegree, full=True)
        print (res)
        return np.polyval(polynom, x)

    def solve_x(self, y):
        xArr = np.array(self.xArr)
        yArr = np.array(self.yArr)
        polynom, res, _, _, _ = np.polyfit(yArr, xArr, self.defaultDegree, full=True)
        print (res)
        return np.polyval(polynom, y)


def parse_coordinate_line(line):
    line = line.strip().replace("at point", "").replace("X", "").replace("Y", "").replace("Z", "").strip()
    line = re.sub('\s+', ' ', line)
    line = line.split(" ")
    return [float(line[0]), float(line[1]), float(line[2])]


def parse_polylines(polylines_string_data, degree):
    polys = []
    poly = None
    for line in polylines_string_data:
        if "Polyline" in line and poly is not None:
            polys.append(poly)
            poly = None
        elif "at point" in line:
            point = parse_coordinate_line(line)
            if poly is None:
                poly = Polyline(point[2], degree)
            poly.xArr.append(point[0])
            poly.yArr.append(point[1])
    polys.append(poly)
    return polys


def find_nearest_polyline_by_y(y, polylines):
    array = []
    for poly in polylines:
        array.append(poly.getLeftY())
    array = np.array(array)
    idx = (np.abs(array - y)).argmin()
    return polylines[idx]


def find_nearest_polyline_by_z(z, polylines):
    array = []
    for poly in polylines:
        array.append(poly.z)
    array = np.array(array)
    idx = (np.abs(array - z)).argmin()
    return polylines[idx]

elatic_modules_polylines = parse_polylines(elatic_modules_polylines.split("\n"), 6)
opan_napr_mejd_lines = parse_polylines(opan_napr_mejd_lines.split("\n"), 1)
opan_napr_mejd_curves = parse_polylines(opan_napr_mejd_curves.split("\n"), 6)

def identify_elatic_modules(x, y):
    selectedNearestPoly = find_nearest_polyline_by_y(y, elatic_modules_polylines)
    print("Selected neatest y is " + str(selectedNearestPoly.getLeftY()))
    result = selectedNearestPoly.solve_y(x)
    print("Solution is " + str(result))
    return result

def identify_opan_napr_mejd(selectedLine, selectedCurve, HD):
    selectedNearestCurve = find_nearest_polyline_by_z(selectedCurve, opan_napr_mejd_curves)
    HD_y_intersect = selectedNearestCurve.solve_y(HD)
    print("H/D = {} intersects curve {} at Y = ".format(HD, selectedNearestCurve.z) + str(HD_y_intersect))
    selectedNearestLine = find_nearest_polyline_by_z(selectedLine, opan_napr_mejd_lines)
    result = selectedNearestLine.solve_x(HD_y_intersect)
    if result > HD:
        print("Warning: intersected x on line surpasses intersected x on curve!!!")
    result = result/2
    print("Intersected curve at Y = {} now intersects line {} at X = ".format(HD_y_intersect, selectedNearestLine.z) + str(result))
    return result

identify_elatic_modules(1,0.4)
identify_opan_napr_mejd(4,12,1.3)

if __name__ == "__main__" and False:
    print("================== Hello to Rozi's program ====================")
    while True:
        possible_answers = ['e', 'onm']
        print("================== Type one of the options ====================")
        print("'e'          for 'elastic modules' identification")
        print("'onm'        for 'opan naprejenie mejdinno; identification")
        selected_identification = input('Enter your option: ')
        if selected_identification in possible_answers:
            if selected_identification == 'e':
                print("You have selected 'elastic modules' identification. if you want to exit - simply type 'exit' and hit enter")

                while True:
                    try:
                        askY = float(input('Enter your Y: '))
                        askX = float(input('Enter your X: '))
                        identify_elatic_modules(askX, askY)
                    except:
                        print("The value is not a number - exiting...")
                        break
            elif selected_identification == 'onm':
                print("You have selected 'opan naprejenie mejdinno' identification. if you want to exit - simply type 'exit' and hit enter")
                while True:
                    try:
                        selectedLine = float(input('Enter your selectedLine: '))
                        selectedCurve = float(input('Enter your selectedCurve: '))
                        HD = float(input('Enter your HD: '))
                        identify_opan_napr_mejd(selectedLine, selectedCurve, HD)
                    except:
                        print("The value is not a number - exiting...")
                        break
        else:
            print("you entered wrong option\n")






