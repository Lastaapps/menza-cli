"""
Doc available at
https://agata-new.suz.cvut.cz/jidelnicky/JAPI/JAPI-popis.html
"""

from typing import Any
import re


class DataClass:
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


class DishList(DataClass):
    """TJidelnicek entity"""

    def __init__(self, resp: dict[str, Any]):
        self.id = int(resp["id"])
        self.name = str(resp["nazev"])
        self.description = str(resp["popis"])
        self.systems = [int(x) for x in str(resp["podsystemy"]).split(";")]
        self.price = str(resp["cena"])


class Subsystem(DataClass):
    """TPodsystem entity"""

    def __init__(self, resp: dict[str, Any]):
        self.id = int(resp["id"])
        self.description = str(resp["popis"])
        self.open = int(resp["otevreno"]) == 1


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

    @staticmethod
    def __parse_allergens(allergens: str) -> list[str]:
        return list(filter(lambda x: x != "", re.split(",| |;|\\.", allergens)))

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsystem_id = int(data["podsystem_id"])
        self.date = str(data["datum"])
        self.dish_list_ids = str(data["jidelnicek"]).split(";")
        self.type = int(data["kategorie"])
        self.weight = str(data["vaha"] or "")
        self.name = str(data["nazev"])
        self.side_dish_a = str(data["priloha_a"])
        self.side_dish_b = str(data["priloha_b"])
        self.price_student = float(data["cena_stud"])
        self.price_normal = float(data["cena"])
        self.allergens = Dish.__parse_allergens(str(data["alergeny"]))
        self.photo = str(data["foto"])

        self.complete = self.name
        self.complete += (self.side_dish_a + " ") if self.side_dish_a else ""
        self.complete += (self.side_dish_b + " ") if self.side_dish_b else ""

        self.warn: bool | None = None


# --- Menza Info --------------------------------------------------------------
class Info(DataClass):
    """TInfo entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"] or -1)
        self.subsystem_id = int(data["podsystem_id"])
        self.subsystem_web = str(data["podsystem_web"])
        self.header = str(data["text_nahore"]).replace("<BR>", "\n").strip()
        self.footer = str(data["text_dole"]).replace("<BR>", "\n").strip()


class OpenTime(DataClass):
    """TOtDoba entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsytem_id = int(data["podsystem_id"])
        self.serving_id = int(data["vydejna_id"])
        self.serving_name = str(data["vydejna_nazev"])
        self.serving_abbrev = str(data["vydejna_zkratka"])
        self.serving_order = int(data["vydejna_poradi"])
        self.from_desc = str(data["od_popisek"])
        self.from_order = str(data["od_poradi"])
        self.day_from = str(data["od_den_od"])
        self.day_to = str(data["od_den_do"])
        self.time_from = str(data["od_cas_od"])
        self.time_to = str(data["od_cas_do"])


class Contact(DataClass):
    """TKontakt entity"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.subsystem_id = int(data["podsystem_id"])
        self.gps = str(data["maps"])
        self.order = int(data["poradi_web"] or 0)
        self.role = str(data["pozice"])
        self.name = str(data["jmeno"])
        self.phone = str(data["telefon"])
        self.email = str(data["email"])


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


class DayDish(DataClass):
    """TDenJidlo"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.id_week = int(data["id_tyden"])
        self.date = str(data["datum"])
        self.day_of_week = int(data["den"])
        self.type = int(data["typstravy"])
        self.name = str(data["nazev"])
        self.weight = str(data["vaha"] or "")
