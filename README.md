# requests_proxy
class RequestProxy <br />
Принимает не обязательные парамерты frequency, country, protocol, anonymity, speed, count
<br />
Метод requests_get - делает get запрос с использование proxy, автоматически меняет proxy сервер, усли указана частота смены
Метод requests_post - делает post запрос ...

Class GetProxy

Принимат на вход не обязательные параметры country, protocol, anonymity, speed, count

Метод get_proxy возвращает список с proxy серверами, количество сереров указывается параметром count (подефолту 1)

Метод get_proxy_yield возвращает объект генератор со всеми найденными прокси
