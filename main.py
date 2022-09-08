from bs4 import BeautifulSoup
import requests
from datetime import datetime, date
from redis import Redis
from rq import Queue


url_to_parse = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273"
que = Queue(connection=Redis())
# img = que.enqueue(get_images, url_to_parse)
# page = requests.get(url_to_parse)
# bs = BeautifulSoup(page.text, 'lxml')


# data = bs.find('div', class_='clearfix').find('div', class_='image')
# images = bs.find_all('div', class_='image') #1
# titles = bs.find_all('div', class_='title') #2
# dates_of_post = bs.find_all('span', class_='date-posted')
# prices = bs.find_all('div', class_='price') #7

# var
# img_url  = ''
# oneprice = ''
# currency = ''
post_title = ''
post_date = ''


def get_images(url):
    images = []
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'lxml')
    all_images_data = bs.find_all('div', class_='image')

    for image in all_images_data:
        if image.img.has_attr('data-src'):
            images.append(image.img['data-src'])
    return images


# for i in get_images(url_to_parse):
#     print(i)


# #2
def get_titles(url):
    titles = []
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'lxml')
    all_titles_data = bs.find_all('div', class_='title')

    for title in all_titles_data:
        if title.text.lstrip().rstrip():
            titles.append(title.text.lstrip().rstrip())
    return titles

# for i in get_titles(url_to_parse):
#     print(i)


#3
def get_post_date(url):
    post_dates = []
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'lxml')
    all_dates_data = bs.find_all('span', class_='date-posted')

    for pd in all_dates_data:
        if pd.text.rstrip().lstrip()[2] == pd.text.rstrip().lstrip()[5] == '/':
            post_date = datetime.strptime(pd.text, '%d/%m/%Y').strftime("%d-%m-%Y")
            post_dates.append(post_date)
        else:
            post_dates.append(datetime.strptime(str(date.today()),'%Y-%m-%d').strftime('%d-%m-%Y'))
    return post_dates

# for i in get_post_date(url_to_parse):
#     print(i)

# # 7
def get_prices(url):
    prices = []
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'lxml')
    all_prices_data = bs.find_all('div', class_='price')
    for price in all_prices_data:
        if price.text:
            prc = price.text.lstrip().rstrip()
            #prices.append(prc)
            if prc.startswith('$') or prc.startswith('€') or prc.startswith('₴'):
                prices.append(prc)
                #prices.append(prc.split(prc[0])[1])
            else:
                prices.append('-'+prc)
    return prices

# for i in get_prices(url_to_parse):
#     print(i[0], ' ', i.split(i[0])[1])


def get_cityes(url):
    cityes = []
    page = requests.get(url_to_parse)
    bs = BeautifulSoup(page.text, 'lxml')
    all_cities_data = bs.find_all('div', class_='location')

    for city in all_cities_data:
        if city:
            cityes.append(city.span.text.lstrip().rstrip())
    return cityes

# for i in get_cityes(url_to_parse):
#     print(i)

def get_beds(url):
    beds = []
    page = requests.get(url_to_parse)
    bs = BeautifulSoup(page.text, 'lxml')
    all_beds_data = bs.find_all('span', class_='bedrooms')

    for bed in all_beds_data:
        if bed:
            onebed = bed.text.split(':')

            beds.append(onebed[1].lstrip().rstrip())
    return beds


