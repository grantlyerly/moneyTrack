import requests
from bs4 import BeautifulSoup

"""
Donor Look up:
https://www.opensecrets.org/donor-lookup/results?name=buddy+bengel&order=desc&sort=D&zip=28562

https://www.opensecrets.org/donor-lookup/results? name = NAME &order=desc & sort=D & zip = ZIP
"""


# Individual Functions


def collect_contributions(name, zipCode):
    namePlus = name.replace('_', '+')

    url = f"https://www.opensecrets.org/donor-lookup/results?name={namePlus}&order=desc&sorD&zip={zipCode}"

    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    body = soup.body
    
    data = body.find_all('tr')

    ret=[]

    for a in data[1:]:
        item = str(a)
        badstr = ['<tr>', '<td class="category orange">', '<td>', 
                  '</td>', '/tr', '<td class="u-nowrap">', '<br/>',
                  '\t', '<>', '<td class="category green">', '<td class="c-red u-center" colspan="8" style="font-size: 12px;"><b>FEDERAL LAW PROHIBITS THE USE OF CONTRIBUTOR INFORMATION FOR THE PURPOSE OF SOLICITING CONTRIBUTIONS OR FOR ANY COMMERCIAL PURPOSE.</b>']
        for char in badstr:
            item = item.replace(char, "")

        splitItem = item.split('\n')

        """
        Set up as follows:

        \n
        \n
        money to candidates
        \n
        \n
        name
        city, zip
        \n
        employer
        occupation
        date
        money
        recipient
        state
        \n
        """

        if len(splitItem) > 5:
            split_location = splitItem[6].split(',')

            results = {'category':splitItem[2], 'contributor': splitItem[5], 'city': split_location[0], 'zipCode': split_location[1].strip(' '), 
                   'employer': splitItem[8], 'occupation': splitItem[9], 'data': splitItem[10], 'amount':splitItem[11], 'recipient':splitItem[12], 'jurisdiction':splitItem[13]}
            
            ret.append(results)

    return(ret)


def parse_contributions(contribution):
    amount_str = contribution['amount'].strip('$')
    amount = int(amount_str.replace(',', ''))
    target = contribution['recipient']
    target_party = target[-2]

    return amount, target_party


def impact(name, zipCode):
    contrs = collect_contributions(name, zipCode)
    r = 0
    d = 0
    for contr in contrs:
        amount, tp = parse_contributions(contr)
        if tp == 'R':
            r += amount
        if tp == 'D':
            d += amount
        print(amount, tp)
    
    print("Republican = " + str(r))
    print("Democrat = " + str(d))

    perc = max((r/(r+d)), (d/(r+d)))
    party = 'R'
    amt = r
    if d > r:
        party = 'D'
        amt = d
    return(perc, party, amt)


if __name__ == '__main__':
    # name = input("name: ")
    # zipCode = input('zipCode: ')
    print(impact('buddy bengel', 28562))