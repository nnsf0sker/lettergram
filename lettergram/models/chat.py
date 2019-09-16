from typing import Tuple
from typing import FrozenSet
from dataclasses import dataclass


@dataclass(frozen=True)
class Chat:
    id: str
    name: str
    users: FrozenSet[str]
    created_at: str
    related_messages: Tuple[str, ...]
