import sys
import time
import pyautogui
import os
import imghdr
import cv2

class Objective(object):

    def __init__(self, name="Objective"):
        self._name = name

    def name(self):
        return self._name

    def locateImg(self, img):
        path = r'./images/' + img

        # Pre-condition: path to img file must exist
        if not os.path.exists(path):
            raise Exception(self._name + ".locateImg() pre-condition failed, " + path + " does not exist!")

        # Pre-condition: file must be of valid img type
        if not (imghdr.what(path) == 'png') and not (imghdr.what(path) == 'jpeg'):
            raise Exception(self._name + ".locateImg() pre-condition failed, " + path + " is not of type jpeg nor png")
        
        image = cv2.imread(path)

        # Post-condition: returns 4-integer tuple (left, top, width, height)
        coordinates = pyautogui.locateOnScreen(image, confidence=0.8)
        if coordinates == None:
            raise Exception(self._name + "./locateImg() failed, could not detect " + path + " on screen")

        return coordinates

    def clickAtCoord(self, coordinates):
        # Pre-condition: coordinates must be given
        if (coordinates == None):
            raise Exception(self._name + ".clickAt() pre-condition failed, coordinates == None")

        # Pre-condition: coordinates must be within a valid range
        screenSize = pyautogui.size()
        if (coordinates[0] > screenSize[0]) or (coordinates[1] > screenSize[1]):
            raise Exception(self._name + ".clickAt() pre-condition failed, cannot reach " + coordinates[slice(2)] + " on " + screenSize)

        pyautogui.click(x=coordinates[0], y=coordinates[1])

    def clickAtImg(self, img):
        self.clickAtCoord(pyautogui.center(self.locateImg(img)))

    def hotkey(self, *arg):
        # Pre-condition: at least one argument passed
        if not len(arg) > 0:
            raise Exception(self._name + ".hotkey() pre-condition failed, " + len(arg) + " arguments passed!")

        # Pre-condition: arguments must be of type string
        for argument in arg:
            if not isinstance(argument, str):
                raise Exception(self._name + ".hotkey() pre-condition failed, " + argument + " is not of type string!")

        pyautogui.hotkey(*arg)

    def write(self, input):
        # Pre-condition: input must be of type string
        if not isinstance(input, str):
            raise Exception(self._name + ".write() pre-condition failed, " + input + " is not of type string!")

        pyautogui.write(input)

    def dragRelative(self, startCoord, xDist, yDist):
        # TODO: refactor code for DRY principle, here are duplicate pre-conditions of function clickAtCoord()
        # Pre-condition: coordinates must be given
        if (startCoord == None):
            raise Exception(self._name + ".clickAt() pre-condition failed, startCoord == None")

        # Pre-condition: coordinates must be within a valid range
        screenSize = pyautogui.size()
        if (startCoord[0] > screenSize[0]) or (startCoord[1] > screenSize[1]):
            raise Exception(self._name + ".clickAt() pre-condition failed, cannot reach " + startCoord[slice(2)] + " on " + screenSize)

        pyautogui.moveTo(x=startCoord[0], y=startCoord[1])
        pyautogui.drag(xDist, yDist, 0.3, button='left')


