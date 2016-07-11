# This code is so ugly. I don't care. This works, and that's all I care about.
# I'm convinced there is no elegant way of doing this.
import requests
import os
from lxml import html
from sys import argv

s = requests.Session()
bin_list = []
headers = {
    'Cookie': ''
}
os.popen('mkdir videos/{}'.format(argv[1]))


def login():
    DATA = {
        'user[email]': '',
        'user[password]': '',
        'authenticity_token': '',
    }
    r = s.post('https://egghead.io/users/sign_in', data=DATA, headers=headers)


def parse_bin(content, key):
    print(key)
    try:
        file = content.split(key)[1].split('" />')[0]
        bin_list.append('{}{}'.format(key, file))
    except IndexError:
        print('Failed on parse_bin')


def build_list():
    SSL_WISTIA = 'https://embed-ssl.wistia.com/deliveries/'
    WISTIA = 'http://embed.wistia.com/deliveries/'
    r = s.get('https://egghead.io/technologies/{}'.format(argv[1]))
    tree = html.fromstring(r.text)
    items = tree.xpath('//a[@class=""]')
    for item in range(0, len(items)):
        for i in items[item].items():
            if 'https://egg' in i[1]:
                t = s.get(i[1])
                try:
                    file = t.text.split(WISTIA)[1].split('" />')[0]
                    bin_list.append('{}{}'.format(WISTIA, file))
                except IndexError:
                    ssl_bin = t.text.split(SSL_WISTIA)[1].split('" />')[0]
                    bin_list.append('{}{}'.format(SSL_WISTIA, ssl_bin))
                    print('WE BROKE')
                    print(i)
                    item += 1
    download_list()


def download_bin(bin):
    file_name = bin.split('.bin')[0].split('deliveries/')[1]
    video = open('videos/{}/{}.mp4'.format(argv[1], file_name), 'wb')
    resp = requests.get(bin, stream=True)

    if not resp.ok:
        print('Request to the .bin file failed. Attempted url was %' % bin)

    for data in resp.iter_content(1024):
        video.write(data)


def download_list():
    for bin in bin_list:
        download_bin(bin)
