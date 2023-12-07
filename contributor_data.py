import requests
from bs4 import BeautifulSoup

"""
Donor Look up:
https://www.opensecrets.org/donor-lookup/results?name=buddy+bengel&order=desc&sort=D&zip=28562

https://www.opensecrets.org/donor-lookup/results? name = NAME &order=desc & sort=D & zip = ZIP
"""

def collect(name, zipCode):
    namePlus = name.replace('_', '+')

    url = f"https://www.opensecrets.org/donor-lookup/results?name={namePlus}&order=desc&sorD&zip={zipCode}"

    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    body = soup.body
    
    data = body.find_all('tr')
    str_data = []

    for a in data:
        item = str(a)
        badstr = ['<tr>', '<td class="category orange">', '<td>', 
                  '</td>', '/tr', '<td class="u-nowrap">', '<br/>',
                  '\t', '<>']
        for char in badstr:
            item = item.replace(char, "")
        
        new_str = str()
        for index in range(len(item)-1):
            if item[index] != '\n':
                new_str += item[index]
            else:
                if index != 0:
                    if item[index-1] != '\n':
                        new_str += ','

        new_item = new_str.split(',')
        str_data.append(new_item)


    test = str_data[1]

    print(type(str_data))
    print(type(test))

    print(str_data)

if __name__ == '__main__':
    collect('buddy bengel', 28562)