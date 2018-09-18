import re
import requests
import math
from requests import get
from bs4 import BeautifulSoup
from random import *

# import cgitb
# import cgi
#
# cgitb.enable() #This will show any errors on your webpage
#
# inputs = cgi.FieldStorage() #REMEMBER: We do not have inputs, simply a button to run the program. In order to get inputs, give each one a name and call it by inputs['insert_name']
#
# print "Content-type: text/html" #We are using HTML, so we need to tell the server
#
# print #Just do it because it is in the tutorial :P
#
# print "<title> MyPythonWebpage </title>"
#
# print "Whatever you would like to print goes here, preferably in between tags to make it look nice"
#User Input
print("Radom US vinyls. Type 'help' for options.")
url = 'https://www.discogs.com/'
while True:
    genre = input("Genre: ")
    if genre.lower() == "help":
        response = get(url)
        html_soup = BeautifulSoup(response.content, "html.parser")
        options = html_soup.find('div', class_ = 'more_facets_dialog')
        options_str = options.text
        options_str = re.sub(r'[0-9]+', '', options_str).replace(',', '').strip()
        option_list = re.split(r'\s{2,}', options_str)
        print('Options: ' + ', '.join(option_list))
    else:
        genre = genre.title().strip().replace(' ', '+')
        break

while True:
        style = input("Style: ")
        if style.lower() == 'help':
            url = 'https://www.discogs.com/search/?format_exact=Vinyl&genre_exact=' + genre + '&limit=250&country_exact=US'
            response = get(url)
            html_soup = BeautifulSoup(response.content, "html.parser")
            options = html_soup.find_all('div', class_ = 'more_facets_dialog')
            options_str = options[1].text
            options_str = re.sub(r'[0-9]+', '', options_str).replace(',', '').strip()
            option_list = re.split(r'\s{2,}', options_str)
            print('Options: ' + ', '.join(option_list))
        else:
            style = style.title().strip().replace(' ', '+')
            break

while True:
        decade = input("Decade: ")
        if decade.lower() == 'help':
            url = 'https://www.discogs.com/search/?style_exact=' +style +'&format_exact=Vinyl&genre_exact=' +genre
            response = get(url)
            html_soup = BeautifulSoup(response.content, "html.parser")
            options = html_soup.find('div', class_ = 'aside_left')
            options_str = options.text
            # options_str = re.sub("[^0-9]", " ", options_str)
            option_list = [s for s in options_str.split() if s.isdigit()]
            option_list = [s for s in option_list if len(s)==4]
            print('Options: ' + ', '.join(option_list))

        else:
            break

url = 'https://www.discogs.com/search/?limit=250&style_exact=' +style+ '&format_exact=Vinyl&genre_exact=' +genre+ '&decade=' +decade+ '&country_exact=US'
response = get(url)
html_soup = BeautifulSoup(response.content, "html.parser")

#find random page #
num_pages = html_soup.find('div', class_ = 'pagination top ')
# num_pages = html_soup.find('strong', class_ = 'pagination_total')
num_pages_str = num_pages.strong.text
start = num_pages_str.find('f')
num_pages_int = int(num_pages_str[start+2:].strip().replace(',', ''))

page = randint(1, int(math.ceil(num_pages_int/250.0)))

#redo url
url = 'https://www.discogs.com/search/?limit=250&style_exact=' +style+ '&format_exact=Vinyl&genre_exact=' +genre+ '&decade=' +decade+ '&page=' + str(page) + '&country_exact=US'
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')

#find random card
record_cards = html_soup.find_all('div', class_ = 'card')
#print(len(record_cards))
record_card = record_cards[randint(0,len(record_cards)-1)]
album = record_card.h4.a.text
artist = record_card.h5.a.text
album_artist = album + ' ' + artist

#price url
album_artist = re.sub(r'\W+', ' ', album_artist)

url = 'http://www.valueyourmusic.com/vinyl?utf8=%E2%9C%93&q='
for word in album_artist.split():
    url = url + word + '+'
url_lowest = url[0:-1] + '&sort=price_asc&utf8=%E2%9C%93'
url_highest = url[0:-1] + '&sort=price_desc&utf8=%E2%9C%93'

#find lowest price
response = get(url_lowest)
html_soup = BeautifulSoup(response.content, "html.parser")
prices = html_soup.find_all('div', class_ = 'item-basic-info')
if len(prices)>0:
    price1 = prices[0]
    low_price = price1.strong.text
else:
    low_price = "Not Found"

#find highest price
response = get(url_highest)
html_soup = BeautifulSoup(response.content, "html.parser")
prices = html_soup.find_all('div', class_ = 'item-basic-info')
if len(prices)>0:
    price1 = prices[0]
    high_price = price1.strong.text
else:
    high_price = "Not Found"

print("Album: " + album)
print("Artist: " + artist)
print("Low Price: " + low_price)
print("High Price: " + high_price)
