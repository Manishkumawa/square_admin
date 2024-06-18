from django import template

register = template.Library()

@register.filter(name='extract_policy_invoice')



def extract_policy_invoice(data_str):
    # Splitting the string to handle each dictionary separately
    data_list = [d.strip() for d in data_str.strip('[]').split('},')]

    # Extracting fields from the first dictionary
    fields = {}
    if data_list:
        first_dict = data_list[0].strip('{}')
        key = ''
        value = ''
        in_key = True
        in_quotes = False
        for char in first_dict:
            if char == ':' and in_key:
                in_key = False
            elif char == ',' and not in_quotes:
                fields[key.strip("'")] = value.strip("'")
                key = ''
                value = ''
                in_key = True
            elif char == "'":
                in_quotes = not in_quotes
            elif in_key:
                key += char
            else:
                value += char
        fields[key.strip("'")] = value.strip("'")

    return fields
