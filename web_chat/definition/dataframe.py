from dataclasses import dataclass
from enum import Enum

class QueryIntent(Enum):
    CHAT = 0
    WEB = 1
    UNK = 2
