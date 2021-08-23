import  re
def parse_text(file_data):

    # ------------------------------------------------------------------------------
    items_list = re.findall(r'\b[^\d\W]+\b', file_data)
    reversed_list = items_list[::-1]
    items = []
    items.append(reversed_list[6])
    for i in reversed(reversed_list):
        if reversed_list[7] != 'No':
            items.append(i)
    # Extract Receipt No
    # ------------------------------------------------------------------------------
    order_No = re.search(r'[\n\r].*Transaction ID:\s*([^\n\r]*)', file_data)
    order_No = order_No[0].replace("Order No.:", "")
    order_No = order_No.lstrip()
    # Extract Cashier name
    # ------------------------------------------------------------------------------
    cashier_name = re.search(r'[\n\r].*User:\s*([^\n\r]*)', file_data)
    cashier_name = cashier_name[0].replace("User:", "")
    cashier_name = cashier_name.lstrip()
    # Extracts Date
    # ------------------------------------------------------------------------------
    date = re.search(r'\d{2}/\d{2}/\d{4}', file_data)
    receipt_date = date.group()
    # Extracts time
    # ------------------------------------------------------------------------------
    receipt_time = re.findall(r'\s(\d{1,2}:\d{1,2}:\d{1,2}\s?(?:AM|PM|am|pm))', file_data)
    # Extracts total number of items
    # ------------------------------------------------------------------------------
    products = re.findall(r"(\d+)x", file_data)
    products_total = 0
    for item in products:
        products_total += int(item)
    # Extracts amount paid and change returned
    # ------------------------------------------------------------------------------
    lines = file_data.splitlines()
    line_list = []
    # print(lines)
    for i in lines:
        a_string = i.rstrip("\n")
        a_string = i.split("\n")

        line_list.append(a_string[0])
    for i in line_list:
        i = i.strip()
        if i == '':
            line_list.remove(i)
    line_list = line_list[: len(line_list) - 2]

    last_lines = line_list[-3:]
    total = last_lines[0]
    cash = last_lines[1]
    files_data = []
    cash = cash.replace(',','.')
    total = total.replace(',','.')
    money_returned = float(cash) - float(total)
    files_data.append((items, cashier_name, receipt_time, receipt_date, order_No, int(products_total), total,
                       cash, money_returned))
    data_set = {"product": items, "cashier_name":cashier_name,'receipt_time':receipt_time,'receipt_date':receipt_date,"order_No":order_No,'products_total':int(products_total),"total":total}
    print(data_set)
    return data_set