import datetime
import sqlmodel
import reflex as rx
from typing import Optional

class SimulationResult(rx.Model, table=True):
    user_id: int
    name: Optional[str]
    beneficiary: Optional[str]
    chosen_date: str
    departement: str
    secteur: str
    typologie: str
    fiche: str
    description: str
    parameters: str
    result_eur: float
    result_cumacs: Optional[float]
    date_simulation: Optional[str]
    # cumacs_multiplier: Optional[float]