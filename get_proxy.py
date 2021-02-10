import requests

from bs4 import BeautifulSoup
from codes import *


def error(func):
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            print("Error")

class GetProxy:
    """
    GetProxy(county=-1, protocol=-1, anonymity=-1, speed=-1, count=1)
    country-'AF', 'AL', 'AR', 'AM', 'AU', 'AT', 'BD', 'BY', 'BZ', 'BJ', 'BO', 'BA', 'BW', 'BR', 'BG',
            'BF', 'KH', 'CM', 'CA', 'CL', 'CN', 'CO', 'CG', 'CD', 'CR', 'HR', 'CY', 'CZ', 'DK', 'DO', 'EC',
            'SV', 'GQ', 'FI', 'FR', 'GE', 'DE', 'GR', 'GN', 'HN', 'HU', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IT',
            'JP', 'KZ', 'KE', 'KR', 'KG', 'LA', 'LV', 'LB', 'LY', 'LT', 'MK', 'MW', 'MY', 'MV', 'MU', 'MX',
            'MD', 'MN', 'MZ', 'NP', 'NL', 'NI', 'NG', 'PK', 'PS', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'PR',
            'RO', 'RU', 'RS', 'SC', 'SG', 'SK', 'SI', 'SO', 'ZA', 'ES', 'SD', 'SZ', 'SE', 'SY', 'TW', 'TZ',
            'TH', 'TN', 'TR', 'UG', 'UA', 'GB', 'US', 'UY', 'UZ', 'VN', 'VG', 'ZM', 'ZW'
    protocol - h - http, s - https, 4 - socks4, 5 - socks5
    anonymity - 0 - no, 1 - low, 2 - average, 3 - hight
    speed - 0....100000
    count - number of proxy servers
    """
    def __init__(self, country=-1, protocol=-1, anonymity=-1, speed=-1, count=1):
        self.url = 'https://hidemy.name/ru/proxy-list/?'
        if country != -1 and country in country_codes: self.url += f'country={country}&'
        if speed != -1: self.url += f'maxtime={speed}&'
        if protocol != -1 and protocol in type_codes: self.url += f'type={protocol}&'
        if anonymity != -1 and anonymity in anon_codes: self.url += f'anon={anonymity}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
        }
        self.count = count

        self.proxy_list = []

    def get_proxy(self):
        """
        :return: list poxy server ip:port
        """
        self.proxy_list = []
        for j in range(min(self.count//64 + 1, 31)):
            for i in self.get_soup(f'{self.url}start={j*64}').find('tbody', {'id': 'list'}).find_all('tr'):
                self.proxy_list.append(f"{i.find_all('td')[0].text}:{i.find_all('td')[1].text}")
                if self.proxy_list.__len__() == self.count:
                    return self.proxy_list

    def get_proxy_yield(self):
        """
        :return: generator proxy server ip;port
        """
        for j in range(30):
            for i in self.get_soup(f'{self.url}start={j*64}').find('tbody', {'id': 'list'}).find_all('tr'):
                yield f"{i.find_all('td')[0].text}:{i.find_all('td')[1].text}"

    def get_soup(self, url):
        """
        :param url: url page
        :return: BeautifulSoup object for url page
        """
        return BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml')


class RequestProxy(GetProxy):
    def __init__(self, frequency=-1, country=-1, protocol=-1, anonymity=-1, speed=-1, count=1):
        super().__init__(country, protocol, anonymity, speed, count)
        if False in [type(i) == int for i in [frequency, country, protocol, anonymity, speed, count]]:
            raise TypeError("All class variables must be int")
        if frequency != -1:
            self.prox = self.get_proxy_yield()
            self.now = {'http': f'http://{next(self.prox)}'}
        else:
            self.prox = self.get_proxy()
            self.now = {'http': f'http://{self.prox[0]}'}
        self.num = 0
        self.freq = frequency

    @error
    def requests_get(self, url, headers=None, data=None, cookies=None, auth=None):
        if type(self.prox) == list:
            return requests.get(url, headers=headers, data=data, cookies=cookies, auth=auth, proxies=self.now)
        else:
            self.next_prox()
            return requests.get(url, headers=headers, data=data, cookies=cookies, auth=auth, proxies=self.now)

    @error
    def requests_post(self, url, headers=None, data=None, cookies=None, auth=None):
        if type(self.prox) == list:
            return requests.post(url, headers=headers, data=data, cookies=cookies, auth=auth, proxies=self.now)
        else:
            self.next_prox()
            return requests.post(url, headers=headers, data=data, cookies=cookies, auth=auth, proxies=self.now)

    @error
    def next_prox(self):
        self.num += 1
        if self.num % self.freq == 0:
            try:
                self.now['http'] = f'http://{next(self.prox)}'
            except:
                self.prox = self.get_proxy_yield()
                self.now['http'] = f'http://{next(self.prox)}'
