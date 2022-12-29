"""
Doc available at
https://github.com/Lastaapps/menza-backend
"""

from typing import Any


class DataClass:
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


class Status(DataClass):
    """Current global rating status"""

    def __init__(self, data: dict[str, Any]):
        self.id = str(data["id"])
        self.rate_count = int(data["rateCount"])
        self.rating = float(data["rating"])
        self.sold_out_count = int(data["soldOutCount"])


class Rate(DataClass):
    """Rate payload"""

    def __init__(self, id: str, rating: int):
        self.id = id
        self.rating = rating


class Soldout(DataClass):
    """Soldout payload"""

    def __init__(self, id: str):
        self.id = id


class Statistics(DataClass):
    """Today rating statistics"""

    def __init__(self, data: dict[str, Any]):
        self.ratings = int(data["ratings"])
        self.average = float(data["average"])
        self.sold_out = int(data["sold_out"])
        self.state_count = int(data["state_requests"])
        self.statistics_count = int(data["statistics_requests"])
