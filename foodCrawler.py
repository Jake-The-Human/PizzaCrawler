import requests
from bs4 import BeautifulSoup
# not as fun as a pizza_spider
def food_spider(max_pages, town, state, food):
    page = 1
    while page <= max_pages:
        if page is 1:
            url = 'http://www.yellowpages.com/search?search_terms='+ food + '&geo_location_terms=' + town + '%2C+' + state
        else:
            url = "http://www.yellowpages.com/search?search_terms=" + food +"&geo_location_terms=" + town +"%2C%20"+ state +"&page=" + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        # in findAll the 'a' flag stand for anchor which indicates where links are in html
        for link in soup.findAll('a', {'class':'business-name'}):
            href = "http://www.yellowpages.com" + link.get('href')
            title = link.string
            if title is None:
                # gets rid of some addresses that don't work
                continue
            website = get_food_url(href)
            phone_num = get_food_phone(soup)
            print(title)
            print("\tYellow pages:",href)
            print("\tWebsite:",website)
            print("\tPhone number:",phone_num)
            print()

        page += 1

def get_food_url(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for food_link in soup.findAll('a', {'class':'secondary-btn website-link'}):
        href = food_link.get('href')
        return href

def get_food_phone(site_soup):
    for phone in site_soup.findAll('div', {'class':"phones phone primary"}):
        number = phone.string
        return number


#pizza_spider(1, "Lowell", "MA")
print(r'''
  food
  / ___|_ __ __ ___      _| | ___ _ __
 | |   | '__/ _` \ \ /\ / / |/ _ \ '__|
 | |___| | | (_| |\ V  V /| |  __/ |
  \____|_|  \__,_| \_/\_/ |_|\___|_|
''')
print("\nWelcome")
town = input("What town/city are you looking for pho in?\n->")
state = input("What state are you in?\n->")
food = input("What kind of food would you like to search?\n->")
page_str = input("How many pages do you want to search?\n->")
print("\nHere are the " + food + " places in your surrounding area!")
page = int(page_str)
food_spider(page, town.title(), state.upper(), food.lower())
