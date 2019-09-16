from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    id: str
    chat: str
    author: str
    text: str
    created_at: str
