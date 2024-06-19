import requests
from bs4 import BeautifulSoup
import pprint


def create_url_list():
    url_list = []
    for num in range(1, 3):
        page_url = f'https://news.ycombinator.com/news?p={str(num)}'
        url_list.append(page_url)
    return url_list


URL = create_url_list()


def get_page_content(url_list):
    content_list = ''
    for url in url_list:
        res = requests.get(url)
        content_list += res.text
    return content_list


result = get_page_content(URL)

website = BeautifulSoup(result, 'html.parser')
links = website.select('.titleline > a')
subtext = website.select('.subtext')


def sort_stories_by_votes(li):
    return sorted(li, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')

        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(links, subtext))
