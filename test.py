from get_proxy import RequestProxy


a = RequestProxy(frequency=1, speed=100)
headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }
for i in range(500):
    q = a.requests_get('https://www.championat.com/stat/football/2021-02-02.json', headers)
    print(q.status_code, i)
