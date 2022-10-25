#!/bin/python

from src.api import agata_api as a
from src.api import lasta_api as l
import sys

print(sys.path)

print(str(a.get_dish_list()))
print(str(a.get_sub_systems()))
print(str(a.get_serving_places(1)))
print(str(a.get_dish_types(1)))
print(str(a.get_dishes(1)))
print(str(a.get_info(1)))
print(str(a.get_from_times(1)))
print(str(a.get_contact()))
print(str(a.get_address()))
print(str(a.get_week_info(1)))
print(str(a.get_day_dish(a.get_week_info(1)[0].id)))

print(str(l.post_rating(l.dish_id("", ""), 4)))
print(str(l.post_sold_out(l.dish_id("", ""))))
print(str(l.get_status()))
print(str(l.get_statistics()))
