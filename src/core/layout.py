import json
from dataclasses import dataclass
from typing import List, Dict, Any


LAYOUT_FILE = "layout.json"


@dataclass
class Rect:
    x1: int
    y1: int
    x2: int
    y2: int


@dataclass
class Zone:
    name: str
    rect: Rect


@dataclass
class Stage:
    rect: Rect


@dataclass
class Exit:
    rect: Rect


class Layout:
    def __init__(self, path: str = LAYOUT_FILE):
        with open(path, "r") as f:
            data = json.load(f)

        self.width: int = int(data["width"])
        self.height: int = int(data["height"])

        self.zones: List[Zone] = [
            Zone(
                name=z["name"],
                rect=Rect(
                    x1=int(z["x1"]),
                    y1=int(z["y1"]),
                    x2=int(z["x2"]),
                    y2=int(z["y2"]),
                ),
            )
            for z in data["zones"]
        ]

        st = data["stage"]
        self.stage = Stage(
            rect=Rect(
                x1=int(st["x1"]),
                y1=int(st["y1"]),
                x2=int(st["x2"]),
                y2=int(st["y2"]),
            )
        )

        self.exits: List[Exit] = [
            Exit(
                rect=Rect(
                    x1=int(ex["x1"]),
                    y1=int(ex["y1"]),
                    x2=int(ex["x2"]),
                    y2=int(ex["y2"]),
                )
            )
            for ex in data["exits"]
        ]

    def get_zone_by_name(self, name: str) -> Zone:
        for z in self.zones:
            if z.name.lower() == name.lower():
                return z
        raise ValueError(f"Zone '{name}' not found")

    def as_dict(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "zones": [
                {"name": z.name, "x1": z.rect.x1, "y1": z.rect.y1, "x2": z.rect.x2, "y2": z.rect.y2}
                for z in self.zones
            ],
            "stage": {
                "x1": self.stage.rect.x1,
                "y1": self.stage.rect.y1,
                "x2": self.stage.rect.x2,
                "y2": self.stage.rect.y2,
            },
            "exits": [
                {
                    "x1": ex.rect.x1,
                    "y1": ex.rect.y1,
                    "x2": ex.rect.x2,
                    "y2": ex.rect.y2,
                }
                for ex in self.exits
            ],
        }
