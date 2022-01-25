from bs4 import BeautifulSoup
import requests
import pandas as pd



path1 = 'https://www.zingat.com/istanbul-satilik-daire'
b = []
gsm =[]
nsm = []
bathrooms = []
rooms = []
prices = []

for i in range(1,49):
    path = 'https://www.zingat.com/istanbul-satilik-daire?page=' + str(i)
    zingat = requests.get(path)
    content = zingat.content
    soup = BeautifulSoup(content, 'html.parser')

    links = soup.find_all('a', {'class': 'zl-card-inner'})
    for l in links:
        cellpath = path1 + l.get('href')
        cellzin = requests.get(cellpath)
        cellcontnt = cellzin.content
        cellsoup = BeautifulSoup(cellcontnt, 'html.parser')

        price = cellsoup.find('strong', {'itemprop': 'price'})
        if price != None:
            prices.append((price.text))
        else:
            prices.append('None')

        attr = cellsoup.find_all('li', {'class': 'col-md-6'})
        for a in attr:
            if 'banyo' in a.strong.text.lower():
                bathrooms.append(a.span.text.strip())
            elif 'banyo' in a.strong.text.lower() and a.strong.text.lower()== None:
                bathrooms.append('None')
            elif 'brüt' in a.strong.text.lower():
                gsm.append(a.span.text.strip())
            elif 'brüt' in a.strong.text.lower() and a.strong.text.lower()== None:
                gsm.append('None')
            elif 'net' in a.strong.text.lower():
                nsm.append(a.span.text.strip())
            elif 'net' in a.strong.text.lower() and a.strong.text.lower()== None:
                nsm.append('None')
            elif 'oda' in a.strong.text.lower():
                rooms.append(a.span.text.strip())
            elif 'oda' in a.strong.text.lower() and a.strong.text.lower()== None:
                rooms.append('None')

print(len(nsm))
print(len(bathrooms))
print(len(gsm))
print(len(prices))
print(len(rooms))

d = {'nsm':nsm[0:982],'gsm':gsm[0:982],'bathrooms':bathrooms[0:982],'rooms':rooms[0:982],'prices':prices[0:982]}
df = pd.DataFrame(data=d)
print(df)

writer = pd.ExcelWriter('Zingat_House_sale_Datas.xlsx')
df.to_excel(writer)
writer.save()
