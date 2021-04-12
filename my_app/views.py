import requests
from django.shortcuts import render
from bs4 import BeautifulSoup

from pprint import pprint

from . import models

# places
LA = 'losangeles'

BASE_CRAIGSLIST_URL = 'https://{}.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_search = '%20'.join(search.split())
    final_url = BASE_CRAIGSLIST_URL.format(LA, final_search)
    response = requests.get(final_url)

    soup = BeautifulSoup(response.text, features='html.parser')

    post_listings = soup.find_all('li',  {'class': 'result-row'})

    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        post_price = post.find(class_='result-price')
        if post_price is None:
            post_price = 'no money mf'
        else:
            post_price = post_price.text

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = "https://media.tenor.com/images/dab27fca3d35ab2e391e8d73d7731996/tenor.gif"

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, "my_app/new_search.html", stuff_for_frontend)


if __name__ == '__main__':
    url = r'https://losangeles.craigslist.org/search/?query=python%20tutor'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, features='html.parser')

    post_listings = soup.find_all('li',  {'class': 'result-row'})
    post = post_listings[1].find(class_='result-image')
