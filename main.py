from __future__ import annotations

from ConcreteFactories.ConcreteFactories import AroniumConcreteFactory, ICG_ConcreteFactory


def aronium_running_code(factory):
    """
    The client code works with factories and parsers only through abstract
    types: AbstractFactory and AbstractParser. This lets you pass any factory
    or Parser subclass to the client code without breaking it.
    """
    aronium_parser = factory.parser_base()
    return aronium_parser.parser_function()


def icg_running_code(factory):
    """
    The client code works with factories and parsers only through abstract
    types: AbstractFactory and AbstractParser. This lets you pass any factory
    or Parser subclass to the client code without breaking it.
    """
    ICG_parser = factory.parser_base()
    return ICG_parser.parser_function()


def pick_parser(_POS_name):
    if _POS_name == "Aronium":
        return aronium_running_code(AroniumConcreteFactory())

    elif _POS_name == "ICG":
        return icg_running_code(ICG_ConcreteFactory())


def check_symbols(file_lines, symbols):
    # print(type(file_lines))
    for i in symbols['splitter_symbols']:
        if i in file_lines:

            return True
        else:
            return False
        #


def check_keywords(_file_lines, parser_1, parser_2):
    for i in parser_1['Keywords']:

        if i in _file_lines:
            if check_symbols(_file_lines, parser_1):
                return 'Aronium_splitter'
        elif check_symbols(_file_lines, parser_2):

            if check_symbols(_file_lines, parser_2):
                return
        return 'No receipts'


#     Aronium_POS = "Aronium"
#     ICG_POS = "ICG"
#
#     ICG_Structured_receipt = pick_parser(ICG_POS)
#     Aronium_structured_receipt = pick_parser(Aronium_POS)
#
#     print('ICG :', ICG_Structured_receipt, "\nAronium: ", Aronium_structured_receipt)
#
if __name__ == "__main__":

    """
    The client code can work with any concrete factory class.
    """
    """
    The client code can work with any concrete factory class.
    """
    Aronium_POS = "Aronium"
    ICG_POS = "ICG"

    ICG_Structured_receipt = pick_parser(ICG_POS)
    Aronium_structured_receipt = pick_parser(Aronium_POS)

    print(ICG_Structured_receipt,"\n", Aronium_structured_receipt)
    # aronium_parser_splitter = {"POS_name": "Aronium",
    #                            "splitter_symbols": [":", " x "],
    #                            "Keywords": ['Receipt No.: '],
    #                            # TODO "Lase_needed_field": 1
    #                            }
    # aronium_parsers_regex = {"POS_name": "Aronium",
    #                          "parser_type": "Regex",
    #                          "splitter_symbols": [":", " X "],
    #                          "Keywords": ['Transaction ID:'],
    #                          # TODO "Lase_needed_field": 1
    #                          }
    #
    # Aronium_POS = "Aronium"
    # ICG_POS = "ICG"
    # import os
    #
    # for subdir, dirs, files in os.walk('Receipts'):
    #     for file in files:
    #         file_name = (os.path.join(subdir, file))
    #         current_file = open(file_name, 'rb').read()
    #         file_lines = current_file.decode(
    #             'utf-8')  # Aronium_structured_receipt = pick_parser(Aronium_POS,aronium_parsers)
    #
    #         keywords_flag = check_keywords(file_lines, aronium_parser_splitter,
    #                                        aronium_parsers_regex)
    #         structured_receipt = ''
    #         if keywords_flag =="Aronium_splitter":
    #             Aronium_Structured_receipt = pick_parser(Aronium_POS)
    #             print(Aronium_Structured_receipt)
    #
    #             structured_receipt = aronium_running_code(AroniumConcreteFactory())
    #         elif keywords_flag == 'Aronium_Regex':
    #             structured_receipt = icg_running_code(ICG_ConcreteFactory())
    #             Aronium_Structured_receipt = pick_parser(Aronium_POS)
    # else:
    #     "No Parsers found "
    #
    # print(Aronium_Structured_receipt)
