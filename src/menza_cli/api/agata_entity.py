"""
Doc available at
https://agata-new.suz.cvut.cz/jidelnicky/JAPI/JAPI-popis.html
"""

from typing import Any, Callable


class DataClass:
    """Defines toString() method for it's ancestors"""

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, obj: Any):
        return isinstance(obj, DataClass) and obj.__dict__ == self.__dict__


def mstr(data: Any | None) -> str | None:
    if data == None:
        return None
    else:
        return str(data)

def map_not_none(data: Any, block: Callable[[Any], Any]) -> Any:
    if data == None:
        return None
    else:
        return block(data)
    


class Subsystem(DataClass):
    """TPodsystem entity"""

    def __init__(self, resp: dict[str, Any]):
        self.id = int(resp["id"])
        self.description = str(resp["popis"])
        self.open = bool(resp["otevreno"])
        self.daily = bool(resp["jidelnicek_denni"])
        self.weekly = bool(resp["jidelnicek_tydenni"])
        self.order = int(resp["poradi"])


class ServingPlace(DataClass):
    """TVydejna entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsystem_id = int(data["podsystem_id"])
        self.name = str(data["nazev"])
        self.description = str(data["popis"])
        self.abbrev = str(data["zkratka"])


class DishType(DataClass):
    """TTypStravy entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsystem_id = int(data["id"])
        self.name = str(data["nazev"])
        self.description = str(data["popis"])
        self.order = int(data["poradi"])


class Dish(DataClass):
    """TDish entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsystem_id = int(data["podsystem_id"])
        self.date = mstr(data["datum"])
        self.serving_places: list[int] = [int(x) for x in list(data["vydejny"])]
        self.type = int(data["kategorie"])
        self.weight = mstr(data["vaha"] or "")
        self.name = str(data["nazev"])
        self.side_dish_a = mstr(data["priloha_a"] or "")
        self.side_dish_b = mstr(data["priloha_b"] or "")
        self.price_student = float(data["cena_stud"])
        self.price_normal = float(data["cena"])
        self.allergens: list[int] = [int(x) for x in list(data["alergeny"])]
        self.photo = mstr(data["foto"])
        self.active = bool(data["aktivni"])

        self.complete = self.name
        self.complete += " " + str(self.side_dish_a or "")
        self.complete += " " + str(self.side_dish_b or "")

        self.warn: bool | None = None


# --- Menza Info --------------------------------------------------------------
class Info(DataClass):
    """TInfo entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"] or -1)
        self.subsystem_id = int(data["podsystem_id"])
        self.subsystem_web = mstr(data["podsystem_web"])
        self.footer = map_not_none(data["text_dole"], lambda x: str(x).replace("<BR>", "\n").strip())


class News(DataClass):
    """TAktuality entity"""

    def __init__(self, data: str):
        self.header = map_not_none(data, lambda x: str(x).replace("<BR>", "\n").strip())


class OpenTime(DataClass):
    """TOtDoba entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsytem_id = int(data["podsystem_id"])
        self.serving_id = int(data["vydejna_id"])
        self.serving_name = str(data["vydejna_nazev"])
        self.serving_abbrev = str(data["vydejna_zkratka"])
        self.serving_order = int(data["vydejna_poradi"])
        self.from_desc = mstr(data["od_popisek"])
        self.from_order = int(data["od_poradi"])
        self.day_from = mstr(data["od_den_od"])
        self.day_to = mstr(data["od_den_do"])
        self.time_from = mstr(data["od_cas_od"])
        self.time_to = mstr(data["od_cas_do"])


class Contact(DataClass):
    """TKontakt entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsystem_id = int(data["podsystem_id"])
        self.gps = str(data["maps"])
        self.order = int(data["poradi"] or 0)
        self.role = mstr(data["pozice"])
        self.name = mstr(data["jmeno"])
        self.phone = mstr(data["telefon"])
        self.email = mstr(data["email"])


class Address(DataClass):
    """TAdresa entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsystem_id = int(data["podsystem_id"])
        self.subsystem_name = str(data["podsystem_nazev"])
        self.address = str(data["adresa"])
        self.gps = str(data["mapag"])


# --- Week --------------------------------------------------------------------
class WeekInfo(DataClass):
    """TTyden entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.description = str(data["popis"])
        self.valid_from = str(data["platnost_do"])
        self.valid_to = str(data["platnost_od"])


days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class DayDish(DataClass):
    """TDenJidlo"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.id_week = int(data["id_tyden"])
        self.date = str(data["datum"])
        self.day_of_week = int(data["den"])
        self.type = int(data["typstravy"])
        self.name = str(data["nazev"])
        self.weight = mstr(data["vaha"])
        self.type_name = str(data["typstravy_nazev"])

        self.day_of_week_name = days_of_week[self.day_of_week]
