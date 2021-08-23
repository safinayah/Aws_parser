from AbstactParser.Abstract_parser import AbstractFactory
from concrete_parsers.concrete_parsers import AroniumConcreteParser, ICG_ConcreteParser


class AroniumConcreteFactory(AbstractFactory):
    """
    Concrete Factories produce a family of aronium_parsers that belong to a single
    variant. The factory guarantees that resulting aronium_parsers are compatible. Note
    that signatures of the Concrete Factory's methods return an abstract
    Parser, while inside the method a concrete Parser is instantiated.
    """

    # can add other Functions
    def parser_base(self):
        return AroniumConcreteParser()


class ICG_ConcreteFactory(AbstractFactory):
    """
    Concrete Factories produce a family of aronium_parsers that belong to a single
    variant. The factory guarantees that resulting aronium_parsers are compatible. Note
    that signatures of the Concrete Factory's methods return an abstract
    Parser, while inside the method a concrete Parser is instantiated.
    """


    def parser_base(self):
        return ICG_ConcreteParser()
