import logging
from PC.brain.navigation_map import NavigationMap

log = logging.getLogger(__name__)


class PersonLookup:

    def __init__(self):
        self.nav_map = NavigationMap()

        # Each entry: (list of names/nicknames, room_id)
        self.people = [

            # Top row
            (["alae","ammour", "alae ammour"], "prof",                 "1.39"),
            (["youssef", "rachidi","youssef rachidi"],          "1.38"),
            (["mephtha","gennoun","mephtha gennoun"],           "1.33"),
            (["nisrine", "lachgar","nisrine lachgar"],          "1.32"),
            (["sara","bakkali","sara bakkali"],                 "1.31"),
            (["hiba","sekkat","hiba sekkat"],                   "1.29"),
            (["oumaima", "moutik","oumaima moutik"],            "1.28"),
            (["badr","elkari","badr elkari"],                   "1.27"),
            (["mohammed","rhazzaf","mohammed rhazzaf"],         "1.26"),

            # Right corridor
            (["masrour"],                           "1.15"),
            (["abibaw"],                            "1.12"),
            (["mezzan"],                            "1.11"),
            (["abderrahmane", "abder"],             "1.10"),
            (["mehdaoui"],                          "1.07"),
            (["adamo"],                             "1.06"),
            (["zineddine", "zinou"],                "1.04"),

            # Left side
            (["loubna"],                            "1.46"),
            (["asmae"],                             "1.48"),
            (["hafid"],                             "1.49"),
            (["taha left", "taha 2"],               "1.51"),
            (["abdellah"],                          "1.52"),
            (["dir el hilali", "hilali"],           "1.55"),
            (["khaoula"],                           "1.57"),

            # Bottom row
            (["meriem"],                            "1.66"),

            # Top right
            (["saidou"],                            "1.19"),
            (["mouha", "mouhamed"],                 "1.16"),
        ]

    def find_person(self, query: str) -> dict | None:
        query = query.lower().strip()

        for names, room_id in self.people:
            for name in names:
                if query == name or query in name or name in query:
                    return self.nav_map.find(room_id)

        log.warning(f"No person match for: '{query}'")
        return None

    def list_people(self) -> list:
        """Returns all known names and nicknames as a flat list."""
        return [name for names, _ in self.people for name in names]