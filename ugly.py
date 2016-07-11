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


def build_list():
    r = s.get('https://egghead.io/technologies/{}'.format(argv[1]))
    tree = html.fromstring(r.text)
    items = tree.xpath('//a[@class=""]')
    for item in items:
        for i in item.items():
            if 'https://egg' in i[1]:
                t = s.get(i[1])

                find_this = 'http://embed.wistia.com/deliveries/'
                try:
                    file = t.text.split(find_this)[1].split('" />')[0]
                    # print(file)
                    bin_list.append(
                        'http://embed.wistia.com/deliveries/{}\n'.format(file))
                except IndexError:
                    print(bin_list)
                    download_list()
                    return
                download_list()


def download_bin(bin):
    file_name = bin.split('.bin')[0].split('deliveries/')[1]
    with open('videos/{}/{}.mp4'.format(argv[1], file_name), 'wb') as video:
        resp = requests.get(bin, stream=True)

        if not resp.ok:
            print('Request to the .bin file failed. Attempted url was %' % bin)

        for data in resp.iter_content(1024):
            video.write(data)


def download_list():
    for bin in bin_list:
        download_bin(bin)
