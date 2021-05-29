from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


class IndexView(View):
    template_name = 'index.html'

    def count_frequency(self, data):
        words = {}
        frequent_words = {}
        for i in data:
            if words.get(i):
                words[i] += 1
            else:
                words[i] = 1

        ans = sorted(words, key=words.get, reverse=True)[:10]
        for i in ans:
            frequent_words.update({i: words[i]})

        return frequent_words

    def is_valid_url(self, url):
        page = urlopen(url)  # only one time opening url
        check_url = '/'.join(url.split('/')[:4])
        if page.getcode() == 200 and check_url == 'https://en.wikipedia.org/wiki':  # page exists and is wiki url or not
            html_page = page.read()
            soup = BeautifulSoup(html_page, 'html.parser')

            content = soup.find(attrs={'id': 'bodyContent'}).text.lower()
            content = ' '.join(re.sub(r'[0-9!@#$%^&*(){}\[\]\-;–,.?:\"\\]', ' ', content).split()).split()  # search and replace spacial characters and numbers => ''
            # print(content)  # cleaned data ready
            return self.count_frequency(content)
        return None

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        url = request.POST.get('wiki-url')
        data = self.is_valid_url(url)
        if data:
            return render(request, self.template_name, context={'words': data})
        else:
            messages.error(request, 'Only Wikipedia URL Accepted.')
            return render(request, self.template_name)
