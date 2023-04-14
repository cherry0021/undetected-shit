import re

def formatted_number_with_comma(number):
    return ("{:,}".format(number))


def str_to_int(text, decimal_point = 0):
    text = text.replace(',', '')
    text = text.strip()
    
    number = float(text)
    if decimal_point:
        return round(number, decimal_point)
    else:
        return int(number)
    
def numbers_within_str(text, decimal_point=0):
    text = text.strip()
    text = text.replace(',', '')
    
    numbers = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', text)
    for i in range(len(numbers)):
        if decimal_point == None:
            numbers[i] = float(numbers[i])
        if decimal_point == 0:
            numbers[i] = int(numbers[i])
        else:
            numbers[i] = float(numbers[i])
            numbers[i] = round(numbers[i], decimal_point)          
    
    return numbers