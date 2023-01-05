import ascii_magic
from result import as_result

from src.api.agata_api import AgataApi
from src.api.agata_entity import OpenTime
from src.api.agata_entity import Subsystem, Dish
from src.api.lasta_api import LastaApi
from .repo import Repo, CompleteInfo, TimeGroup, DishRatingMapper


class RepoImpl(Repo):
    def __init__(
        self,
        agata_api: AgataApi,
        lasta_api: LastaApi,
        allergens: list[int],
    ):
        self.agata_api = agata_api
        self.lasta_api = lasta_api
        self.allergens = allergens

    @as_result(Exception)
    def get_menza_list(self) -> list[Subsystem]:
        """Gets list of all the CTU menzas"""

        return sorted(
            sorted(
                self.agata_api.get_sub_systems(),
                key=lambda s: s.description,
            ),
            key = lambda x: x.id,
        )

    def __update_warn(self, dish: Dish) -> Dish:
        dish.warn = len(set(self.allergens) & set(dish.allergens)) != 0
        return dish

    @as_result(Exception)
    def get_dish_list(self, system: Subsystem) -> dict[str, list[Dish]]:
        """Get today dish menu in a menza"""

        types = sorted(self.agata_api.get_dish_types(system.id), key=lambda s: s.order)
        dishes = self.agata_api.get_dishes(system.id)
        dishes = list(map(self.__update_warn, dishes))
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
    def get_rating(self) -> DishRatingMapper:
        """Get the current rating status"""

        self.rating_list = self.lasta_api.get_status()

        def ratingProvider(subsystem: Subsystem, dish: Dish) -> tuple[float, int]:
            id = self.lasta_api.dish_id(subsystem.description, dish.complete)
            return next(
                ((x.rating, x.rate_count) for x in self.rating_list if x.id == id),
                (0, 0),
            )

        return ratingProvider

    @as_result(Exception)
    def get_image(self, dish: Dish, width: int, height: int) -> str:
        """Gets image in ascii_art format"""

        text = ascii_magic.from_url(
            self.agata_api.get_image_url(dish.subsystem_id, dish.photo),
            columns=width,
            char="❚",
        )

        lines = text.split("\n")
        if len(lines) >= height:
            diff = height - len(lines)
            return "\n".join(lines[diff // 2 : height - diff // 2])
        else:
            diff = len(lines) - height
            l = [""] * (diff // 2) + lines + [""] * (diff // 2)
            return "\n".join(l)

    def get_image_url(self, dish: Dish) -> str | None:
        """Gets image web url"""
        if len(dish.photo) == 0:
            return None
        return self.agata_api.get_image_url(dish.subsystem_id, dish.photo)

    @as_result(Exception)
    def send_rating(self, subsystem: Subsystem, dish: Dish, rating: int) -> None:
        id = self.lasta_api.dish_id(subsystem.description, dish.complete)
        self.rating_list = self.lasta_api.post_rating(id, rating)
