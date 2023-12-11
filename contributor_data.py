import requests
from bs4 import BeautifulSoup
import ast

"""
Donor Look up:
https://www.opensecrets.org/donor-lookup/results?name=buddy+bengel&order=desc&sort=D&zip=28562

https://www.opensecrets.org/donor-lookup/results? name = NAME &order=desc & sort=D & zip = ZIP
"""


# Methods for individual contributions


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


# Methods for federal PACs

"""
Searching: https://www.opensecrets.org/political-action-committees-pacs/lookup?txt=duke
<table class="DataTable-Partial dataTable no-footer" data-title="" data-paging="false" data-page-length="0" data-info="false" data-searching="false" data-filtercategories="null" data-filterindexes="null" data-checkboxfilters="null" data-selectfilters="null" data-colorcodeby="" data-uuid="32a58fe4-df75-48ac-9796-fa3d339ef023" 
data-collection="[{&quot;PAC Name&quot;:&quot;\u003ca href=\&quot;/political-action-committees-pacs/duke-energy/C00083535/summary/2024\&quot;\u003eDuke Energy\u003c/a\u003e&quot;,&quot;Type&quot;:&quot;PAC (#C00083535)&quot;,&quot;Most Recent Cycle Activity&quot;:&quot;2024&quot;},{&quot;PAC Name&quot;:&quot;\u003ca href=\&quot;/political-action-committees-pacs/duke-energy/C00429662/summary/2008\&quot;\u003eDuke Energy\u003c/a\u003e&quot;,&quot;Type&quot;:&quot;PAC (#C00429662)&quot;,&quot;Most Recent Cycle Activity&quot;:&quot;2008&quot;},{&quot;PAC Name&quot;:&quot;\u003ca href=\&quot;/political-action-committees-pacs/duke-energy/C00040907/summary/2000\&quot;\u003eDuke Energy\u003c/a\u003e&quot;,&quot;Type&quot;:&quot;PAC (#C00040907)&quot;,&quot;Most Recent Cycle Activity&quot;:&quot;2000&quot;},{&quot;PAC Name&quot;:&quot;\u003ca href=\&quot;/political-action-committees-pacs/duke-pac/C00814004/summary/2022\&quot;\u003eDuke PAC\u003c/a\u003e&quot;,&quot;Type&quot;:&quot;&quot;,&quot;Most Recent Cycle Activity&quot;:&quot;2022&quot;}]" data-columnwidthlimits="{}" data-disablesearchinput="true" data-presortformat="[]" id="DataTables_Table_0" role="grid">
                <thead>
                    <tr role="row"><th class="sorting" tabindex="0" aria-controls="DataTables_Table_0" rowspan="1" colspan="1" aria-label="PAC Name: activate to sort column ascending" style="width: 171.46875px;">PAC Name</th><th class="sorting" tabindex="0" aria-controls="DataTables_Table_0" rowspan="1" colspan="1" aria-label="Type: activate to sort column ascending" style="width: 214.984375px;">Type</th><th class="number-header sorting" tabindex="0" aria-controls="DataTables_Table_0" rowspan="1" colspan="1" aria-label="Most Recent Cycle Activity: activate to sort column ascending" style="width: 279.078125px;">Most Recent Cycle Activity</th></tr>
                </thead>
                <tbody>                                            
                <tr role="row" class="odd">
                        <td class=" color-category " style="height: 100%; vertical-align: middle;"><a href="/political-action-committees-pacs/duke-energy/C00083535/summary/2024">Duke Energy</a></td>
                        <td class=" " style="height: 100%; vertical-align: middle;">PAC (#C00083535)</td>
                        <td class="number " style="height: 100%; vertical-align: middle;">2024</td>
                    </tr><tr role="row" class="even">
                        <td class=" color-category " style="height: 100%; vertical-align: middle;"><a href="/political-action-committees-pacs/duke-energy/C00429662/summary/2008">Duke Energy</a></td>
                        <td class=" " style="height: 100%; vertical-align: middle;">PAC (#C00429662)</td>
                        <td class="number " style="height: 100%; vertical-align: middle;">2008</td>
                    </tr><tr role="row" class="odd">
                        <td class=" color-category " style="height: 100%; vertical-align: middle;"><a href="/political-action-committees-pacs/duke-energy/C00040907/summary/2000">Duke Energy</a></td>
                        <td class=" " style="height: 100%; vertical-align: middle;">PAC (#C00040907)</td>
                        <td class="number " style="height: 100%; vertical-align: middle;">2000</td>
                    </tr><tr role="row" class="even">
                        <td class=" color-category " style="height: 100%; vertical-align: middle;"><a href="/political-action-committees-pacs/duke-pac/C00814004/summary/2022">Duke PAC</a></td>
                        <td class=" " style="height: 100%; vertical-align: middle;"></td>
                        <td class="number " style="height: 100%; vertical-align: middle;">2022</td>
                    </tr></tbody>
            </table>
"""

def PACcontributions(name):
    namePlus = name.replace('_', '+')

    url = f"https://www.opensecrets.org/political-action-committees-pacs/lookup?txt={namePlus}"
    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    body = soup.body

    table = body.find_all('table')
    data = table[0].get('data-collection')
    data = ast.literal_eval(data)

    if len(data == 1):
        entry = data[0]['PAC Name']
        # print(test)
        entries = entry.split('"')
        # print(splittest)
        n = entries[2]
        n_url = entries[1]

        nsplit = n.split('<')
        n_actual = nsplit[0][1:]
        
        print(n_actual)
        print(n_url)
    elif len(data < 1):
        return('No Commmittees found')
        

    pacURL = f'https://www.opensecrets.org{n_url}'


if __name__ == '__main__':
    # name = input("name: ")
    # zipCode = input('zipCode: ')
    print(PACcontributions('duke'))