"""Testing implementation of rating api"""

from .lasta_api import LastaApi
from .lasta_entity import Statistics, Status
import random


class LastaApiMock(LastaApi):
    """Testing implementation of rating api"""

    def __init__(self):
        self.data: dict[str, Status] = {}
        self.data["BUtopenec"] = Status(
            {
                "id": "BUtopenec",
                "combined": {
                    "audience": 1,
                    "average": 4,
                },
            }
        )
        self.data["KUtopenka"] = Status(
            {
                "id": "KUtopenka",
                "combined": {
                    "audience": 1,
                    "average": 3,
                },
            }
        )

    def get_status(self, menza_id: str) -> list[Status]:
        """Gets the current rating status"""

        return list(self.data.values())

    def get_statistics(self) -> Statistics:
        """Gets the current statistics"""

        rating_count = sum({x.audience for x in self.data.values()})
        state = random.randint(42, 69)
        statistics = random.randint(42, 69)

        return Statistics(
            {
                "rating_requests": rating_count,
                "state_requests": state,
                "statistics_requests": statistics,
            }
        )

    def post_rating(
        self, menza_id: str, dish_id: str, dish_name: str, rating: int
    ) -> list[Status]:
        """Rates a dish with BE id given"""

        if dish_id in self.data:
            item = self.data[dish_id]
            item.rating = round(
                (1.0 * item.audience * item.audience + rating) / (item.audience + 1)
            )
            item.audience += 1
        else:
            self.data[dish_id] = Status(
                {
                    "id": dish_id,
                    "combined": {
                        "audience": 1,
                        "average": rating,
                    },
                }
            )

        return list(self.data.values())
