from datetime import datetime
import operator
import requests
from bs4 import BeautifulSoup

call_sign_dict = {}
for x in range(1, 10):
    url = 'https://www.ae7q.com/query/list/GenLicAvail.php?REGION={}'.format(x)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tables = [soup.body.find_all('table')[15], soup.body.find_all('table')[16]]
    for y in tables:
        for z in y.find_all('tr')[2:]:
            cells = z.find_all('td')
            call_sign_cell = cells[0]
            call_sign = call_sign_cell.kbd.get_text()
            
            expiry_date_cell = cells[4]
            expiry_date_string = expiry_date_cell.get_text().encode('utf-8')[:10]
            if len(expiry_date_string) == 10:
                expiry_date =  datetime.strptime(expiry_date_string, '%Y-%m-%d').date()
                
                if expiry_date not in call_sign_dict:
                    call_sign_dict[expiry_date] = []
                call_sign_dict[expiry_date].append(call_sign)
    
for x in sorted(call_sign_dict.items(), key=operator.itemgetter(0)):
    for y in x:
        print(y)