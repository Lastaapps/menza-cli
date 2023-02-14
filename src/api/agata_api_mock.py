# pylint: disable=R1705

"""Agata api used for testing"""

from .agata_api import AgataApi
from .agata_entity import (
    Address,
    Contact,
    DayDish,
    Dish,
    DishType,
    Info,
    News,
    OpenTime,
    ServingPlace,
    Subsystem,
    WeekInfo,
)


class AgataApiMock(AgataApi):
    """Agata api used for testing"""

    def __init__(self):
        """Create api object to get data from BE"""

    def get_sub_systems(self) -> list[Subsystem]:
        """Gets subsystems"""

        return [
            Subsystem(
                {
                    "id": 1,
                    "popis": "Kocourkov",
                    "otevreno": True,
                    "jidelnicek_denni": True,
                    "jidelnicek_tydenni": True,
                    "poradi": 1,
                }
            ),
            Subsystem(
                {
                    "id": 2,
                    "popis": "Bavorov",
                    "otevreno": False,
                    "jidelnicek_denni": True,
                    "jidelnicek_tydenni": True,
                    "poradi": 2,
                }
            ),
        ]

    def get_serving_places(self, subsystem_id: int) -> list[ServingPlace]:
        """Get serving places"""
        if subsystem_id == 1:
            return [
                ServingPlace(
                    {
                        "id": 1,
                        "podsystem_id": 1,
                        "nazev": "Kocourkov",
                        "popis": "Idk 1",
                        "zkratka": "K",
                    }
                ),
            ]
        else:
            return [
                ServingPlace(
                    {
                        "id": 2,
                        "podsystem_id": 2,
                        "nazev": "Bavorov",
                        "popis": "Idk 2",
                        "zkratka": "B",
                    }
                ),
            ]

    def get_dish_types(self, subsystem_id: int) -> list[DishType]:
        """Gets dish types in a subsystem"""
        if subsystem_id == 1:
            return [
                DishType(
                    {
                        "id": "1",
                        "podsystem_id": "1",
                        "nazev": "Polévka",
                        "popis": "Polévky",
                        "poradi": "1",
                    }
                ),
                DishType(
                    {
                        "id": "2",
                        "podsystem_id": "1",
                        "nazev": "Specialita",
                        "popis": "Specialita dne",
                        "poradi": "2",
                    }
                ),
            ]
        else:
            return [
                DishType(
                    {
                        "id": "1",
                        "podsystem_id": "2",
                        "nazev": "Vegeta",
                        "popis": "Vegetariánské",
                        "poradi": "1",
                    }
                ),
                DishType(
                    {
                        "id": "2",
                        "podsystem_id": "2",
                        "nazev": "Moučníky",
                        "popis": "Ňaminy",
                        "poradi": "2",
                    }
                ),
            ]

    def get_dishes(self, subsystem_id: int) -> list[Dish]:
        """Gets dishes for today in the subsystem given"""

        if subsystem_id == 1:
            return [
                Dish(
                    {
                        "id": 1,
                        "podsystem_id": 1,
                        "datum": "2022-12-24",
                        "vydejny": [1],
                        "kategorie": "1",
                        "vaha": "200g",
                        "nazev": "Utopenec",
                        "priloha_a": " okurky",
                        "priloha_b": " lidi",
                        "cena_stud": "42",
                        "cena": "69",
                        "alergeny": [1, 2, 3],
                        "foto": "IMG-2022-12-12-142136203.JPG",
                        "aktivni": True,
                    }
                ),
                Dish(
                    {
                        "id": 2,
                        "podsystem_id": 1,
                        "datum": "2022-12-24",
                        "vydejny": [1],
                        "kategorie": 2,
                        "vaha": "",
                        "nazev": "Utopenka",
                        "priloha_a": " paprika",
                        "priloha_b": " člověci",
                        "cena_stud": 42,
                        "cena": 69,
                        "alergeny": [1, 2, 4],
                        "foto": "",
                        "aktivni": True,
                    }
                ),
            ]
        else:
            return [
                Dish(
                    {
                        "id": 1,
                        "podsystem_id": 2,
                        "datum": "2022-12-24",
                        "vydejny": [2],
                        "kategorie": 1,
                        "vaha": "200g",
                        "nazev": "Utopenec",
                        "priloha_a": " okurky",
                        "priloha_b": " lidi",
                        "cena_stud": 42,
                        "cena": 69,
                        "alergeny": [1, 2, 3],
                        "foto": "IMG-2022-12-12-142136203.JPG",
                        "aktivni": False,
                    }
                ),
                Dish(
                    {
                        "id": 2,
                        "podsystem_id": 2,
                        "datum": "2022-12-24",
                        "vydejny": [2],
                        "kategorie": 2,
                        "vaha": "",
                        "nazev": "Utopenka",
                        "priloha_a": " paprika",
                        "priloha_b": " člověci",
                        "cena_stud": 42,
                        "cena": 69,
                        "alergeny": [1, 2, 4],
                        "foto": "",
                        "aktivni": True,
                    }
                ),
            ]

    def get_info(self, subsystem_id: int) -> list[Info]:
        """Gets info about the subsystem given"""

        if subsystem_id == 1:
            return [
                Info(
                    {
                        "id": 1,
                        "podsystem_id": 1,
                        "podsystem_web": "idk",
                        "text_dole": "Dolni",
                    }
                ),
            ]
        else:
            return [
                Info(
                    {
                        "id": 2,
                        "podsystem_id": 2,
                        "podsystem_web": "idk",
                        "text_dole": "Dolni, ale naopak",
                    }
                ),
            ]

    def get_news(self, subsystem_id: int) -> News:
        """Gets info about the subsystem given"""

        if subsystem_id == 1:
            return News("Horni")
        else:
            return News("Horni, ale naopak")

    def get_open_times(self, subsystem_id: int) -> list[OpenTime]:
        """Gets opening times of the subsystem given"""

        if subsystem_id == 0:
            return [
                OpenTime(x)
                for x in [
                    {
                        "id": "108",
                        "podsystem_id": "1",
                        "vydejna_id": "1",
                        "vydejna_nazev": "Restaurace",
                        "vydejna_zkratka": "R",
                        "vydejna_poradi": "1",
                        "od_popisek": "",
                        "od_poradi": "1",
                        "od_den_od": "Po",
                        "od_den_do": "Čt",
                        "od_cas_od": "11:00",
                        "od_cas_do": "20:00",
                    },
                    {
                        "id": "101",
                        "podsystem_id": "1",
                        "vydejna_id": "1",
                        "vydejna_nazev": "Restaurace",
                        "vydejna_zkratka": "R",
                        "vydejna_poradi": "1",
                        "od_popisek": "",
                        "od_poradi": "2",
                        "od_den_od": "Pá",
                        "od_den_do": "",
                        "od_cas_od": "11:00",
                        "od_cas_do": "19:30",
                    },
                    {
                        "id": "13",
                        "podsystem_id": "1",
                        "vydejna_id": "2",
                        "vydejna_nazev": "Jídelna",
                        "vydejna_zkratka": "J",
                        "vydejna_poradi": "2",
                        "od_popisek": "Snídaně",
                        "od_poradi": "1",
                        "od_den_od": "Po",
                        "od_den_do": "Pá",
                        "od_cas_od": "6:30",
                        "od_cas_do": "9:30",
                    },
                    {
                        "id": "97",
                        "podsystem_id": "1",
                        "vydejna_id": "2",
                        "vydejna_nazev": "Jídelna",
                        "vydejna_zkratka": "J",
                        "vydejna_poradi": "2",
                        "od_popisek": "Oběd",
                        "od_poradi": "2",
                        "od_den_od": "Po",
                        "od_den_do": "Pá",
                        "od_cas_od": "11:00",
                        "od_cas_do": "14:30",
                    },
                    {
                        "id": "105",
                        "podsystem_id": "1",
                        "vydejna_id": "2",
                        "vydejna_nazev": "Jídelna",
                        "vydejna_zkratka": "J",
                        "vydejna_poradi": "2",
                        "od_popisek": "Večeře",
                        "od_poradi": "3",
                        "od_den_od": "Po",
                        "od_den_do": "Čt",
                        "od_cas_od": "17:00",
                        "od_cas_do": "20:00",
                    },
                    {
                        "id": "109",
                        "podsystem_id": "1",
                        "vydejna_id": "2",
                        "vydejna_nazev": "Jídelna",
                        "vydejna_zkratka": "J",
                        "vydejna_poradi": "2",
                        "od_popisek": "Večeře",
                        "od_poradi": "4",
                        "od_den_od": "Pá",
                        "od_den_do": "Pá",
                        "od_cas_od": "17:00",
                        "od_cas_do": "19:30",
                    },
                ]
            ]
        else:
            return [
                OpenTime(x)
                for x in [
                    {
                        "id": "108",
                        "podsystem_id": "1",
                        "vydejna_id": "1",
                        "vydejna_nazev": "Restaurace",
                        "vydejna_zkratka": "R",
                        "vydejna_poradi": "1",
                        "od_popisek": "",
                        "od_poradi": "1",
                        "od_den_od": "Po",
                        "od_den_do": "Čt",
                        "od_cas_od": "11:00",
                        "od_cas_do": "20:00",
                    },
                    {
                        "id": "101",
                        "podsystem_id": "1",
                        "vydejna_id": "1",
                        "vydejna_nazev": "Restaurace",
                        "vydejna_zkratka": "R",
                        "vydejna_poradi": "1",
                        "od_popisek": "",
                        "od_poradi": "2",
                        "od_den_od": "Pá",
                        "od_den_do": "",
                        "od_cas_od": "11:00",
                        "od_cas_do": "19:30",
                    },
                    {
                        "id": "13",
                        "podsystem_id": "1",
                        "vydejna_id": "2",
                        "vydejna_nazev": "Jídelna",
                        "vydejna_zkratka": "J",
                        "vydejna_poradi": "2",
                        "od_popisek": "Snídaně",
                        "od_poradi": "1",
                        "od_den_od": "Po",
                        "od_den_do": "Pá",
                        "od_cas_od": "6:30",
                        "od_cas_do": "9:30",
                    },
                    {
                        "id": "97",
                        "podsystem_id": "1",
                        "vydejna_id": "2",
                        "vydejna_nazev": "Jídelna",
                        "vydejna_zkratka": "J",
                        "vydejna_poradi": "2",
                        "od_popisek": "Oběd",
                        "od_poradi": "2",
                        "od_den_od": "Po",
                        "od_den_do": "Pá",
                        "od_cas_od": "11:00",
                        "od_cas_do": "14:30",
                    },
                    {
                        "id": "105",
                        "podsystem_id": "1",
                        "vydejna_id": "2",
                        "vydejna_nazev": "Jídelna",
                        "vydejna_zkratka": "J",
                        "vydejna_poradi": "2",
                        "od_popisek": "Večeře",
                        "od_poradi": "3",
                        "od_den_od": "Po",
                        "od_den_do": "Čt",
                        "od_cas_od": "17:00",
                        "od_cas_do": "20:00",
                    },
                    {
                        "id": "109",
                        "podsystem_id": "1",
                        "vydejna_id": "2",
                        "vydejna_nazev": "Jídelna",
                        "vydejna_zkratka": "J",
                        "vydejna_poradi": "2",
                        "od_popisek": "Večeře",
                        "od_poradi": "4",
                        "od_den_od": "Pá",
                        "od_den_do": "Pá",
                        "od_cas_od": "17:00",
                        "od_cas_do": "19:30",
                    },
                ]
            ]

    def get_contact(self) -> list[Contact]:
        """Gets contacts to the subsystem given"""

        listus = [
            {
                "id": "1",
                "podsystem_id": "1",
                "maps": "50.079174,14.393236",
                "poradi": 1,
                "pozice": "Vedoucí menzy",
                "jmeno": "",
                "telefon": "234678291",
                "email": "menza-strahov@cvut.cz",
            },
            {
                "id": "2",
                "podsystem_id": "1",
                "maps": "50.079174,14.393236",
                "poradi": 2,
                "pozice": "Provoz",
                "jmeno": "",
                "telefon": "234678361",
                "email": "suz-provoznims@cvut.cz",
            },
            {
                "id": "3",
                "podsystem_id": "2",
                "maps": "50.105612,14.388666",
                "poradi": 2,
                "pozice": "Vedoucí menzy",
                "jmeno": "",
                "telefon": "234678560",
                "email": "menza-studdum@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "4",
                "podsystem_id": "3",
                "maps": "50.103927,14.394534",
                "poradi": 3,
                "pozice": "Vedoucí menzy",
                "jmeno": "",
                "telefon": "234678325",
                "email": "menza-technicka@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "5",
                "podsystem_id": "4",
                "maps": "50.053033,14.428932",
                "poradi": 4,
                "pozice": "Vedoucí menzy",
                "jmeno": "",
                "telefon": "234678550",
                "email": "menza-podoli@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "6",
                "podsystem_id": "5",
                "maps": "50.100882,14.386966",
                "poradi": 5,
                "pozice": "Vedoucí gastroúseku MK",
                "jmeno": "",
                "telefon": "234678480",
                "email": "gastro-mk@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "7",
                "podsystem_id": "6",
                "maps": "50.067097,14.424157",
                "poradi": 6,
                "pozice": "Vedoucí výdejny",
                "jmeno": "",
                "telefon": "234678559",
                "email": "vydejna-horska@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "15",
                "podsystem_id": "8",
                "maps": "50.076228,14.417538",
                "poradi": 7,
                "pozice": "Vedoucí výdejny",
                "jmeno": "",
                "telefon": "234678558",
                "email": "vydejna-karlak@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "9",
                "podsystem_id": "9",
                "maps": "50.13508,14.104551",
                "poradi": 8,
                "pozice": "Vedoucí",
                "jmeno": "",
                "telefon": "234678580",
                "email": "menza-kladno@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "25",
                "podsystem_id": "11",
                "maps": "50.08024566522555,14.390620674641108",
                "poradi": 9,
                "pozice": "Vedoucí",
                "jmeno": "",
                "telefon": "234678291",
                "email": "menza.strahov@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "12",
                "podsystem_id": "12",
                "maps": "50.103865,14.388157",
                "poradi": 10,
                "pozice": "Vedoucí bufetu",
                "jmeno": "",
                "telefon": "234678590",
                "email": "suz-megabuffat@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "24",
                "podsystem_id": "13",
                "maps": "50.1010400,14.3860111",
                "poradi": 11,
                "pozice": "Vedoucí",
                "jmeno": "",
                "telefon": "234678483",
                "email": "gastro-mk@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "13",
                "podsystem_id": "14",
                "maps": "50.079174,14.393236",
                "poradi": 12,
                "pozice": "IT",
                "jmeno": "Tomáš Kaňovský",
                "telefon": "234678370",
                "email": "tomas.kanovsky@cvut.cz",
                "poradi_web": "1",
            },
            {
                "id": "23",
                "podsystem_id": "15",
                "maps": "50.105102,14.389751",
                "poradi": 13,
                "pozice": "Vedoucí",
                "jmeno": "",
                "telefon": "725896859",
                "email": "suz-archicafe@cvut.cz",
                "poradi_web": "1",
            },
        ]
        return [Contact(x) for x in listus]

    def get_address(self) -> list[Address]:
        """Gets address of the subsystem given"""

        return [
            Address(
                {
                    "id": 1,
                    "podsystem_id": 1,
                    "podsystem_nazev": "Kocourkov",
                    "adresa": "Kocourkov 42",
                    "mapag": "50N 15E",
                }
            ),
            Address(
                {
                    "id": 2,
                    "podsystem_id": 2,
                    "podsystem_nazev": "Bavorov",
                    "adresa": "Bavorov 69",
                    "mapag": "50N 15E",
                }
            ),
        ]

    def get_week_info(self, subsystem_id: int) -> list[WeekInfo]:
        """Gets week dish menus available"""

        if subsystem_id == 1:
            return [
                WeekInfo(
                    {
                        "id": 1,
                        "popis": "Popísek 1",
                        "platnost_od": "2022-12-19",
                        "platnost_do": "2022-12-25",
                    }
                ),
            ]
        else:
            return [
                WeekInfo(
                    {
                        "id": 2,
                        "popis": "Popísek 1",
                        "platnost_od": "2022-12-19",
                        "platnost_do": "2022-12-25",
                    }
                ),
            ]

    def get_day_dish(self, week_id: int) -> list[DayDish]:
        """Gets a dish menu for the week id given"""

        return [
            DayDish(
                {
                    "id": 1,
                    "id_tyden": week_id,
                    "datum": "2022-12-23",
                    "den": 4,
                    "typstravy": 1,
                    "nazev": "Žrádlo 1",
                    "vaha": "69 g",
                    "typstravy_nazev": "Polejvka",
                }
            ),
            DayDish(
                {
                    "id": 2,
                    "id_tyden": week_id,
                    "datum": "2022-12-23",
                    "den": 4,
                    "typstravy": 2,
                    "nazev": "Žrádlo 2",
                    "vaha": "",
                    "typstravy_nazev": "Nakládka",
                }
            ),
            DayDish(
                {
                    "id": 3,
                    "id_tyden": week_id,
                    "datum": "2022-12-24",
                    "den": 5,
                    "typstravy": 3,
                    "nazev": "Žrádlo 3",
                    "vaha": "42 ks",
                    "typstravy_nazev": "Dokrmka",
                }
            ),
            DayDish(
                {
                    "id": 4,
                    "id_tyden": week_id,
                    "datum": "2022-12-24",
                    "den": 5,
                    "typstravy": 4,
                    "nazev": "Žrádlo 4",
                    "vaha": "420 ml",
                    "typstravy_nazev": "Dezertér",
                }
            ),
        ]

    def get_image_url(self, subsystem_id: int, name: str) -> str:
        """Gets URL of the given name"""
        # pylint: disable=W0613

        return (
            "https://agata.suz.cvut.cz"
            + f"/jidelnicky/showfoto.php?clPodsystem=1&xFile={name}"
        )
