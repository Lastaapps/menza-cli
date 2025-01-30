"""
Doc available at
https://github.com/Lastaapps/menza-backend
"""

from typing import Any


class DataClass:
    """Defines common toString() method"""

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, obj: Any):
        return isinstance(obj, DataClass) and obj.__dict__ == self.__dict__


class Status(DataClass):
    """Current global rating status"""

    def __init__(self, data: dict[str, Any]):
        self.id = str(data["id"])
        self.rating = float(data["combined"]["average"])
        self.audience = int(data["combined"]["audience"])


class Rate(DataClass):
    """Rate payload"""

    def __init__(self, dish_id: str, name: str, taste: int):
        self.dishID = dish_id
        self.nameCs = name
        self.taste = taste


class Statistics(DataClass):
    """Today rating statistics"""

    def __init__(self, data: dict[str, Any]):
        self.ratings = int(data["rating_requests"])
        self.state_count = int(data["state_requests"])
        self.statistics_count = int(data["statistics_requests"])
