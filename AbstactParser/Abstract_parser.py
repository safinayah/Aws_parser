from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    """
    The Abstract Factory interface declares a set of methods that return
    different abstract aronium_parsers. These aronium_parsers are called a family and are
    related by a high-level theme or concept. aronium_parsers of one family are usually
    able to collaborate among themselves. A family of aronium_parsers may have several
    variants, but the aronium_parsers of one variant are incompatible with aronium_parsers of
    another.
    """

    @abstractmethod
    def parser_base(self):
        pass


class AbstractParser(ABC):
    """
    Here's the the base interface of another Parser. All aronium_parsers can interact
    with each other, but proper interaction is possible only between aronium_parsers of
    the same concrete variant.
    """

    @abstractmethod
    def parser_function(self):
        pass
