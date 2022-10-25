import src.api.agata_api as agata
import src.api.lasta_api as lasta
from src.api.agata_entity import Info, OpenTime, Contact, Address
import ascii_magic
from src.api.agata_entity import Subsystem, Dish

TimeServingGroup = dict[int, list[OpenTime]]
TimeGroup = dict[int, TimeServingGroup]


class CompleteInfo:
    def __init__(
        self,
        info: Info,
        openTimes: TimeServingGroup,
        contacts: list[Contact],
        addresses: list[Address],
    ):
        self.header = info.header
        self.footer = info.footer
        self.times = openTimes
        self.contacts = contacts
        self.addresses = addresses


def get_menza_list() -> list[Subsystem]:
    return sorted(agata.get_sub_systems(), key=lambda s: s.description)


def get_dish_list(system: Subsystem) -> dict[str, list[Dish]]:
    types = sorted(agata.get_dish_types(system.id), key=lambda s: s.order)
    dishes = agata.get_dishes(system.id)
    out: dict[str, list[Dish]] = {}
    for t in types:
        out[t.name] = list(filter(lambda dish: dish.type == t.id, dishes))
    return out


def group_times(times: list[OpenTime]) -> TimeGroup:
    out: TimeGroup = {}

    for time in times:
        group = out.get(time.subsytem_id, {})
        target = group.get(time.serving_id, [])
        target.append(time)
        group[time.serving_id] = target
        out[time.subsytem_id] = group
    return out


def get_complete_info(subsystem_id: int) -> CompleteInfo:
    info = list(
        filter(lambda x: x.subsystem_id == subsystem_id, agata.get_info(subsystem_id))
    )[0]

    all_times = agata.get_open_times(subsystem_id)
    times = group_times(all_times).get(subsystem_id, {})

    contacts = list(
        filter(lambda x: x.subsystem_id == subsystem_id, agata.get_contact())
    )
    addresses = list(
        filter(lambda x: x.subsystem_id == subsystem_id, agata.get_address())
    )

    return CompleteInfo(info, times, contacts, addresses)


def get_image(dish: Dish) -> ascii_magic.AsciiArt:
    print(agata.get_image_url(dish.subsystem_id, dish.photo))
    return ascii_magic.from_url(
        agata.get_image_url(dish.subsystem_id, dish.photo), columns=200, char="❚"
    )
