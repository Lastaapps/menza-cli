#!python3
# /bin/ is omitted because venv is expected

# from src.api import agata_api as a
# from src.api import lasta_api as l
# from src.repo import repo
# import ascii_magic
from src.gui.main import Main
import sys

print(sys.path)

#subsystems = repo.get_menza_list()
#dish_list = repo.get_dish_list(subsystems[5])
#print("\n".join([str(x) for x in subsystems]))
#print(dish_list)

#ascii_magic.to_terminal(repo.get_image(dish_list["Minutka"][0]))

Main().start_app()



# print(str(a.get_dish_list()))
# print(str(a.get_sub_systems()))
# print(str(a.get_serving_places(1)))
# print(str(a.get_dish_types(1)))
# print(str(a.get_dishes(1)))
# print(str(a.get_info(1)))
# print(str(a.get_from_times(1)))
# print(str(a.get_contact()))
# print(str(a.get_address()))
# print(str(a.get_week_info(1)))
# print(str(a.get_day_dish(a.get_week_info(1)[0].id)))
#
# print(str(l.post_rating(l.dish_id("", ""), 4)))
# print(str(l.post_sold_out(l.dish_id("", ""))))
# print(str(l.get_status()))
# print(str(l.get_statistics()))
