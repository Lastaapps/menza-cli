#!/bin/python

from src.api import agata_api as a
import sys

print(sys.path)

print(str(a.get_dish_list()))

