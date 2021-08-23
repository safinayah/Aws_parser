from AbstactParser.Abstract_parser import AbstractParser

from Parser_scripts.ICG_parser import ICG_parser
from Parser_scripts.aronium_splitter import aronium_parser


class AroniumConcreteParser(AbstractParser):
    def parser_function(self):
        return aronium_parser()


class ICG_ConcreteParser(AbstractParser):
    def parser_function(self):
        return ICG_parser()
