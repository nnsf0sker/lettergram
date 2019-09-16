from abc import ABCMeta
from abc import abstractmethod
from typing import Set
from typing import Tuple
from typing import Optional

from lettergram.models.user import User
from lettergram.models.chat import Chat
from lettergram.models.message import Message


class DBAdapter(metaclass=ABCMeta):
    @abstractmethod
    def add_user(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def add_chat(self, name: str, user_ids: Set[str]) -> Optional[Chat]:
        pass

    @abstractmethod
    def add_message(self, chat_id: str, author_id: str, text: str) -> Optional[Message]:
        pass

    @abstractmethod
    def get_user_chats(self, user_id: str) -> Tuple[Chat, ...]:
        pass

    @abstractmethod
    def get_chat_messages(self, chat_id: str) -> Tuple[Message, ...]:
        pass
