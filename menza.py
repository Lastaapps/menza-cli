#!/bin/python

from src.api import endpoints as e
import sys

print(sys.path)

print(str(e.get_dish_list()))

