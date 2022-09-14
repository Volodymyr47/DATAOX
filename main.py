from bs4 import BeautifulSoup
import requests
from datetime import datetime, date

from models import PostHead


url_to_parse = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'
max_page = 999

page = requests.get(url_to_parse)
bs = BeautifulSoup(page.text, 'lxml')
all_data = bs.find_all()
post_head = PostHead()


class PageScrap:

    def get_data(self, source):
        '''
        Get whole data from one page
        '''
        for data in source:
            ti = ''
            im = ''
            da = ''
            pr = ''
            cr = ''
            lo = ''
            ds = ''
            br = ''

            title = data.find('div', class_='title')
            if not title is None:
                ti = title.text.lstrip().rstrip()

            image = data.find('div', class_='image')
            if not image is None:
                im_ = image.find('img')
                if not im_ is None:
                    if im_.has_attr('data-src'):
                         im = im_['data-src']

            post_date = data.find('span', class_='date-posted')
            if not post_date is None:
                if post_date.text.rstrip().lstrip()[2] == post_date.text.rstrip().lstrip()[5] == '/':
                    new_post_date = datetime.strptime(post_date.text, '%d/%m/%Y').strftime("%d-%m-%Y")
                    da = new_post_date
                else:
                    da = datetime.strptime(str(date.today()),'%Y-%m-%d').strftime('%d-%m-%Y')

            price = data.find('div', class_='price')
            if not price is None:
                prc = price.text.lstrip().rstrip()
                if prc.startswith('$') or prc.startswith('€') or prc.startswith('₴'):
                    pr = prc.split(prc[0])[1]
                    cr = prc[0]
                else:
                    pr = prc
                    cr = '-'

            location = data.find('div', class_='location')
            if not location is None:
                lo = location.span.text.lstrip().rstrip()

            description = data.find('div', class_='description')
            if not description is None:
                ds = description.text.lstrip().rstrip()

            bedroom = data.find('span', class_='bedrooms')
            if not bedroom is None:
                bedroom_ = bedroom.text.split(':')
                br = bedroom_[1].lstrip().rstrip()

            # add whole data to DB
            post_head.add_data(ti, im, da, pr, cr, lo, ds, br)
        return 'Operation completed'

    def is_last_page(self, url):
        '''
        Сheck whether this page is the last one
        '''
        p = requests.get(url)
        b = BeautifulSoup(p.text, 'lxml')
        test_data = b.find_all('div', class_='image')
        if len(test_data) == 0:
            return True
        else:
            return False

# new scraping instance
scraping = PageScrap()

# scraping first page only
print(scraping.get_data(all_data))

# scraping pages from second to last
for i in range(2, max_page):
    next_url_to_parse = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i}/c37l1700273'
    print(next_url_to_parse)
    if not scraping.is_last_page(next_url_to_parse):
        page_next = requests.get(next_url_to_parse)
        bs_next = BeautifulSoup(page_next.text, 'lxml')
        all_data_next = bs_next.find_all()
        print(scraping.get_data(all_data_next))
    else:
        print('All pages have been scraping')
        break
