from django import template

register = template.Library()

@register.filter(name='toPersian')
def toPersian(value):
    value = str(value)
    dic = {'0':'۰','1':'۱','2':'۲','3':'۳','4':'۴','5':'۵','6':'۶','7':'۷','8':'۸','9':'۹'}
    for char in value:
        if char in dic.keys():
            value = value.replace(char,dic[char])
    return value

@register.filter(name='numToRange')
def numToRange(number):
    number = int(number)
    return range(1,number+1)

@register.filter(name='numPlus')
def numPlus(number):
    number = int(number)
    return number+1