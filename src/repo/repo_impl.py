import ascii_magic
from result import Result, as_result

from src.api.agata_api import AgataApi
from src.api.agata_api_impl import AgataApiImpl
from src.api.agata_entity import Info, OpenTime, Contact, Address
from src.api.agata_entity import Subsystem, Dish

import src.api.lasta_api as lasta

from .repo import Repo, CompleteInfo, TimeGroup


class RepoImpl(Repo):
    def __init__(self, agata_api: AgataApi = AgataApiImpl()):
        self.agata_api = agata_api

    @as_result(Exception)
    def get_menza_list(self) -> list[Subsystem]:
        """Gets list of all the CTU menzas"""

        return sorted(self.agata_api.get_sub_systems(), key=lambda s: s.description)

    @as_result(Exception)
    def get_dish_list(self, system: Subsystem) -> dict[str, list[Dish]]:
        """Get today dish menu in a menza"""

        types = sorted(self.agata_api.get_dish_types(system.id), key=lambda s: s.order)
        dishes = self.agata_api.get_dishes(system.id)
        out: dict[str, list[Dish]] = {}
        for t in types:
            out[t.name] = list(filter(lambda dish: dish.type == t.id, dishes))
        return out

    @staticmethod
    def __group_times(times: list[OpenTime]) -> TimeGroup:
        """Groups times in common format"""

        out: TimeGroup = {}

        for time in times:
            group = out.get(time.subsytem_id, {})
            target = group.get(time.serving_id, [])
            target.append(time)
            group[time.serving_id] = target
            out[time.subsytem_id] = group
        return out

    @as_result(Exception)
    def get_complete_info(self, subsystem: Subsystem) -> CompleteInfo:
        """Combines all the info about a menza"""

        subsystem_id = subsystem.id
        info = list(
            filter(
                lambda x: x.subsystem_id == subsystem_id,
                self.agata_api.get_info(subsystem_id),
            )
        )[0]

        all_times = self.agata_api.get_open_times(subsystem_id)
        times = RepoImpl.__group_times(all_times).get(subsystem_id, {})

        contacts = list(
            filter(
                lambda x: x.subsystem_id == subsystem_id, self.agata_api.get_contact()
            )
        )
        addresses = list(
            filter(
                lambda x: x.subsystem_id == subsystem_id, self.agata_api.get_address()
            )
        )

        return CompleteInfo(info, times, contacts, addresses)

    @as_result(Exception)
    def get_image(self, dish: Dish) -> ascii_magic.AsciiArt:
        """Gets image in ascii_art format"""

        print(self.agata_api.get_image_url(dish.subsystem_id, dish.photo))
        return ascii_magic.from_url(
            self.agata_api.get_image_url(dish.subsystem_id, dish.photo),
            columns=200,
            char="❚",
        )
