from abc import ABC
from dataclasses import dataclass
from typing import *


class Unit(ABC):
    pass


@dataclass
class Lit(Unit):
    value: Any
    stack: str


@dataclass
class Instr(Unit):
    name: str


@dataclass
class Input(Unit):
    name: str


@dataclass
class Block(Unit):
    items: List[Unit]
