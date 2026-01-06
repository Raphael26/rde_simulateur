from datetime import datetime
from typing import (
    Dict,
    List,
    Optional,
    TypedDict,
    Union,
)


class CustomerData(TypedDict):
    id: int
    name: str
    date_simulation: str
    description: str
    prime: float
    secteur: str
    typologie: str

