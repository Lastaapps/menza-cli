"""
Doc available at
https://github.com/Lastaapps/menza-backend
"""

from typing import Any

class Status:
    """Current global rating status"""

    def __init__(self, data: dict[str, Any]):
        self.id = int(data["id"])
        self.rate_count = int(data["rateCount"])
        self.rating = float(data["rating"])
        self.soldOutCount = int(data["soldOutCount"])

class Rate:
    """Rate payload"""

    def __init__(self, id: str, rating: int):
        self.id = id
        self.rating = rating

class Soldout:
    """Soldout payload"""

    def __init__(self, id: str):
        self.id = id
#{
#    "ratings": 1,
#    "average": 1.0,
#    "sold_out": 0,
#    "state_requests": 3,
#    "statistics_requests": 1
#}
class Statistics:
    """Today rating statistics"""

    def __init__(self, data: dict[str, Any]):
        self.ratings = int(data["ratings"])
        self.average = float(data["average"])
        self.sold_out = int(data["sold_out"])
        self.state_count = int(data["state_requests"])
        self.statistics_count = int(data["statistics_requests"])

