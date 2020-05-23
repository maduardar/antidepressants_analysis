#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import lxml
import argparse
import os
import csv

from time import sleep
from collections import namedtuple

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='Url to parse', type=str)
args = parser.parse_args()

count_parse = 0

InnerBlock = namedtuple('Block', 'title,username,location,reputation,heading,virtues,limitations,text,'
                                 'recommendations_count,comments_count')

HEADERS = (
    'Название товара',
    'Username',
    'Локация(страна, город)',
    'Репутация',
    'Заголовок отзывыа',
    'Достоинства',
    'Недостатки',
    'Текст отзыва',
    'Сколько человек рекомендует отзыв',
    'Количество комментариев',
)


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.username}\t{self.location}\t{self.reputation}\t{self.heading}' \
               f'\t{self.virtues}\t{self.limitations}\t{self.text}\t{self.recommendations_count}' \
               f'\t{self.comments_count}'


class OtzovikParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-language': 'ru,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Cookie': 'refreg=https%3A%2F%2Fotzovik.com%2Freviews%2Fbukmekerskaya_kontora_liga_stavok%2F; ssid=162305530; ownerid=01d2ff67f1a6d0a1c066049ad2aad4; referal=1; ROBINBOBIN=e352db6dlh3da2484vsl84gtc3',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }
        self.result = []

        self.URL = args.url if args.url else str(input("Пожалуйста, введите URL\n"))

    def get_page(self, page: int = None):

        url = self.URL

        if page != 1 and page is not None:
            url += f'{page}/'

        r = self.session.get(url)

        return r.text

    def get_blocks(self, page: int):
        global count_parse

        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        title = soup.select_one('span.fn').get_text(strip=True)

        container = soup.select('div.item.status4.mshow0')

        for item in container:
            block = self.parse_block(item=item, title=title)
            self.result.append(block)

        count_parse = 0

    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.find('a', class_='pager-item last tooltip-top')
        if not container:
            print(soup.find_all('a', class_='pager-item nth'))
            container = soup.find_all('a', class_='pager-item nth')[-1].get_text(strip=True)
            if not container:
                return 1
            return int(container)

        if container:
            return int(container['title'][9:-1])
        else:
            return 1

    def parse_block(self, item, title):

        global count_parse

        count_parse += 1

        print(f"Идёт парсинг блока {count_parse} из 20")

        username_block = item.select_one('a.user-login')
        username = username_block.get_text(strip=True)

        location_block = item.select_one('div.user-info')
        for div in location_block:
            div = str(div)
            if div.startswith('<div>'):
                location = div[5:-6]
                break

        reputation_block = item.select_one('div.karma-line')
        reputation = reputation_block.select_one('span.karma')
        if 'class="karma karma1' in str(reputation):
            reputation = '+' + str(reputation.get_text())
        else:
            reputation = '-' + str(reputation.get_text())

        heading_block = item.select_one('a.review-title')
        heading = heading_block.get_text(strip=True)

        virtues_block = item.select_one('div.review-plus')
        virtues = virtues_block.get_text(strip=True)

        limitations = item.select_one('div.review-minus').get_text(strip=True)

        text_full = item.select_one('a.review-btn.review-read-link')
        text_full_link = text_full.get('href')
        sleep(10)
        r = self.session.get('https://otzovik.com/' + text_full_link)
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        text = soup.select_one('div.review-body.description')
        text = text.find_all(text=True)

        recommendations_count = item.select_one('span.review-btn.review-yes').get_text()

        comments_count = item.find('span', itemprop='commentCount').get_text(strip=True)

        return Block(
            title=title,
            username=username,
            location=location,
            reputation=reputation,
            heading=heading,
            virtues=virtues,
            limitations=limitations,
            text=text[0],
            recommendations_count=recommendations_count,
            comments_count=comments_count
        )

    def save_result(self):
        filename = args.url[27:-1] + '.csv'
        path = os.getcwd() + filename
        with open(path, 'w') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)

        print(f'Запись в файл завершена. Таблица сохранена по пути {path}')

    def run(self):
        pagination = self.get_pagination_limit()
        for page in range(1, pagination + 1):
            print(f'Парсинг страницы {page} из {pagination}')
            self.get_blocks(page=page)
        self.save_result()


if __name__ == "__main__":
    p = OtzovikParser()
    p.run()
