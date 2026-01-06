from typing import Union, Optional

import reflex as rx

class User(rx.Model, table=True):
    username: str
    password: str
    oAuth: Optional[bool]
    phone_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    superuser: Optional[bool]