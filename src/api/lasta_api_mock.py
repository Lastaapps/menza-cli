from .lasta_api import LastaApi
from .lasta_entity import *

class LastaApiMock(LastaApi):

    def __init__(self):
        self.data: dict[str, Status] = {}
        self.data["BUtopenec"] = Status({"id": "BUtopenec", "rateCount": 1, "rating": 4, "soldOutCount": 0})
        self.data["KUtopenka"] = Status({"id": "KUtopenka", "rateCount": 1, "rating": 3, "soldOutCount": 0})

    def get_status(self) -> list[Status]:
        """Gets the current rating status"""

        return [x for x in self.data.values()]

    def get_statistics(self) -> Statistics:
        """Gets the current statistics"""

        rating_count = sum([x.rate_count for x in self.data.values()])
        average = 3.1415926536
        sold_out = sum([x.sold_out_count for x in self.data.values()])
        statistics = rating_count + sold_out

        return Statistics({"ratings": rating_count, "average": average, "sold_out": sold_out, "statistics_requests": statistics})

    def post_rating(self, id: str, rating: int) -> list[Status]:
        """Rates a dish with BE id given"""

        if id in self.data:
            item = self.data[id]
            item.rating = round((item.rate_count * item.rate_count + rating) / (item.rate_count + 1))
            item.rate_count += 1
        else:
            self.data[id] = Status({"id": id, "rateCount": 1, "rating": rating, "soldOutCount": 0})

        return [x for x in self.data.values()]

    def post_sold_out(self, id: str) -> list[Status]:
        """Marks a dish with BE id given as sold out"""

        if id in self.data:
            self.data[id].sold_out_count += 1
        else:
            self.data[id] = Status({"id": id, "rateCount": 0, "rating": 0, "soldOutCount": 1})

        return [x for x in self.data.values()]

    def dish_id(self, menza_name: str, dish_name: str) -> str:
        """Creates dish id according to BE standard"""
        return menza_name[:1] + dish_name[:8]