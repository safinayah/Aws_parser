"""
This code is made to extract the receipt data from the aronium point of sale
This parser code will extract the receipt's data as follows

1. Reads the file text that represents the receipt
2. Extract the metadata which is transaction id and datetime and remove it from the text
3. Extract the data form the text
4. Cast all numeric values to float or int. Note: int and float values are predefined in the constants file
5. Dumps the dict to get the json text
6. Upload data to Elasticsearch

"""

import json
import os
from types import SimpleNamespace

with open('aronium_constants.json') as json_file:
    """
    This method is to read the constants file and store it's values in a dict called constants_dict
    """
    constants_list = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))
    constants_dict = constants_list[0]


def restructure_items_table_format(items_table_dict):
    """
    This method is to reformat the item table data structure and change it from dict of lists(items,prices,quantities)
    to a list of dicts each dict contains one value for each key(item, price, quantity)
    The main restructure the data in a way to make queries aggregations easier
    :param items_table_dict: is a dict made of 3 lists respectively : items, quantities,prices
    :return: list of dicts each dict made of three records: item_name, quantity, price
    """
    items = []
    lists_length = len(items_table_dict['quantities'])
    for i in range(lists_length):
        item_dict = {'item_name': items_table_dict['items'][i], 'quantity': items_table_dict['quantities'][i],
                     'price': items_table_dict['prices'][i]}
        items.append(item_dict)
    return items


def extract_receipt_data(_file_lines):
    """
    This method extracts the data from the receipt.
    The logic here is to parse the receipt based on the main splitters are used in the receipt
    In the receipts we have the two main splitters are the colon symbol and the multiplication
    the colon splits the receipts' headers and footers
    and the multiplication sign splits the quantity and price
    once all of those cases are extracted
    we get all the receipt parsed except the item name and the total price
    the total will be attached to the price so will be removed from the price text
    Once everything is extracted add the items to a list
    :param _file_lines:
    :return:
    """
    try:
        items, quantities, prices, _sub_receipt_dataset = [], [], [], {}

        for line in _file_lines:
            if constants_dict.keys_values_splitter in line:

                _record = line.split(constants_dict.keys_values_splitter)
                key = _record[0].strip()
                value = _record[1].strip()
                _sub_receipt_dataset[key] = value
            elif constants_dict.quantity_price_splitter in line:
                table_record = line.split(constants_dict.quantity_price_splitter)
                quantities.append(table_record[0].strip())
                priceXquantity = table_record[1].split(' ')
                priceXquantity = list(filter(None, priceXquantity))
                prices.append(priceXquantity[0])
            else:
                item = line.strip()
                items.append(item)

        items_table_list = {"items": list(filter(None, items)), "quantities": [int(i) for i in quantities],
                            "prices": [float(i) for i in prices]}
        items_dict = restructure_items_table_format(items_table_list)
        _sub_receipt_dataset['items'] = items_dict
        return _sub_receipt_dataset
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


def create_final_receipt_dict(transaction_id, transaction_datetime, _sub_receipt_dataset):
    """
    :param transaction_id: the receipt transaction id
    :param transaction_datetime: receipt datetime
    :param _sub_receipt_dataset: a dict of the following keys with their values: user, Order No., Items count, TOTAL,
     Cash, Paid amount
    :return:
    """
    try:

        _sub_receipt_dataset['transaction_id'] = transaction_id
        _sub_receipt_dataset['transaction_datetime'] = transaction_datetime
        _final_receipt_dataset = _sub_receipt_dataset
        return _final_receipt_dataset
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


def extract_transaction_id(receipt_text):
    """
    This method reads the key word of the transaction in the receipt text in order to extract the transaction id
    :param receipt_text: The full receipt text
    :return: transaction id
    """
    _transaction_id = (receipt_text[receipt_text.index(constants_dict.transaction_id_keyword) + len(
        constants_dict.transaction_id_keyword):])
    _transaction_id = _transaction_id.split()[0]
    return _transaction_id


def prepare_receipt_text(_file_lines):
    """
    This method reads the file text(receipt text) to extract the receipt metadata, and clean them from the whole text,
    to prepare the text fo r the parser
    :param _file_lines: The full file text
    :return: list of the receipt text without the transaction id and the transaction id as the
    """
    # TODO remove the AM,PM replace statements and handle 12 hour datetime system

    _file_lines = _file_lines.replace('PM', ' ')
    _file_lines = _file_lines.replace('AM', ' ')
    _file_lines = _file_lines.replace(constants_dict.currency, '  ')

    transaction_id = extract_transaction_id(_file_lines)
    _file_lines = _file_lines.replace(constants_dict.transaction_id_keyword + transaction_id, '')
    _file_lines = _file_lines.replace(transaction_id, '')
    lines_list = _file_lines.splitlines()
    transaction_datetime = (str(lines_list[constants_dict.datetime_info_line])).strip()
    del (lines_list[constants_dict.datetime_info_line])

    _cleaned_receipt_text = {"lines_list": lines_list, "transaction_id": transaction_id,
                             "transaction_datetime": transaction_datetime}

    return _cleaned_receipt_text


def format_datetime(_current_datetime):
    """
    This method formats the data to match the ES needed datetime format
    :param _current_datetime:
    :return: datetime in ES format
    """
    import datetime
    _current_datetime = str(_current_datetime)
    _current_datetime = _current_datetime.rstrip()
    _current_datetime = _current_datetime.lstrip()
    try:
        _current_datetime = datetime.datetime.strptime(_current_datetime, constants_dict.main_date_format)
    except:
        _current_datetime = datetime.datetime.strptime(_current_datetime, constants_dict.alternative_date_format)
    _current_datetime = _current_datetime.strftime(constants_dict.ES_date_format)
    return _current_datetime


def upload_data(data_record, index_name):
    """
        This method connects with ES and upload to the needed index
        :param data_record: records to be uploaded: parsed receipt in our case
        :param index_name: the index
    """

    if data_record:
        from elasticsearch import Elasticsearch
        import configparser

        config = configparser.ConfigParser()
        config.read(constants_dict.ES_ini_file)

        es = Elasticsearch(
            cloud_id=config['ELASTIC']['cloud_id'],
            http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
        )
        es.info()

        es.index(
            index=index_name,
            body=data_record)
        es.indices.refresh(index=index_name)
        # print({'_shards': {'total': 2, 'successful': 1, 'failed': 0}})
    else:
        print(constants_dict.None_data_error_msg)


def cast_numeric_values_to_float(_final_receipt_dataset):
    """
    This method casts the numeric values to int, or float. Note: int, float "Keys" are predefined
    :param _final_receipt_dataset: the dict the contains the whole data with all data as "string"
    :return: same dict but with numeric values as float or int
    """
    for i in constants_dict.int_values:
        _final_receipt_dataset[i] = int(_final_receipt_dataset[i])
    for i in constants_dict.float_values:
        _final_receipt_dataset[i] = float(_final_receipt_dataset[i])
    return _final_receipt_dataset


def generate_json_records(dataset_record):
    """
    dumps the dataset record from dict to json text
    :param dataset_record: dataset record as a dit
    :return: dataset record as json text
    """
    my_date = dataset_record['transaction_datetime']

    import datetime
    my_date = datetime.datetime.strptime(my_date, '%m/%d/%Y %H:%M:%S')

    dataset_record["transaction_datetime"] = my_date.isoformat()
    return json.dumps(dataset_record,indent=5)


def aronium_parser():
    for filename in os.listdir(constants_dict.directory_name):
        current_file = open(constants_dict.directory_name + filename, 'rb').read()
        file_lines = current_file.decode('utf-8')
        cleaned_receipt_text = prepare_receipt_text(file_lines)
        sub_receipt_dataset = extract_receipt_data(cleaned_receipt_text['lines_list'])
        receipt_dataset = create_final_receipt_dict(
            cleaned_receipt_text['transaction_id'],
            cleaned_receipt_text['transaction_datetime'],
            sub_receipt_dataset
        )

        casted_dataset = cast_numeric_values_to_float(receipt_dataset)
        record = generate_json_records(casted_dataset)
        return record
