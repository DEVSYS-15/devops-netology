# Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

1. Работа c HTTP через телнет.
- Подключитесь утилитой телнет к сайту stackoverflow.com
`telnet stackoverflow.com 80`
- отправьте HTTP запрос
```bash
GET /questions HTTP/1.0
HOST: stackoverflow.com
[press enter]
[press enter]
```
- В ответе укажите полученный HTTP код, что он означает?
```shell

    telnet stackoverflow.com 80
    Trying 151.101.1.69...
    Connected to stackoverflow.com.
    Escape character is '^]'.
    
    
    GET /questions HTTP/1.0
    HOST: stackoverflow.com
    
    HTTP/1.1 301 Moved Permanently # Ресурс перемещен навсегда
    cache-control: no-cache, no-store, must-revalidate # директивы ответа кэша
    location: https://stackoverflow.com/questions # полный адрес 
    x-request-guid: da4cadc1-6aff-4ccc-b48c-396aaee2e16c # идентификатор клиента 
    feature-policy: microphone 'none'; speaker 'none' # позволяет разработчику сделать так, чтобы во время просмотра его сайта включались и отключались некоторые возможности браузера.
    content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com # Реализует механизм защиты от угроз межсайтового выполнения скриптов.
    Accept-Ranges: bytes # это маркер, который использует сервер, чтобы уведомить клиента о поддержке "запросов по кускам"
    Date: Sun, 13 Feb 2022 11:00:44 GMT # ну тут понятно))
    Via: 1.1 varnish # добавлять в запрос каждый прокси, через который проходит запрос — для идентификации прокси
    Connection: close # Указывает, что клиент или сервер хотели бы закрыть соединение. Это значение по умолчанию для запросов HTTP/1.0.
    X-Served-By: cache-hel1410032-HEL #
    X-Cache: MISS #
    X-Cache-Hits: 0 #
    X-Timer: S1644750045.780027,VS0,VE110 #
    Vary: Fastly-SSL #
    X-DNS-Prefetch-Control: off #
    Set-Cookie: prov=13279bc3-2a41-f0d3-614f-75df68299018; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly #
    
    Connection closed by foreign host.

```
2. Повторите задание 1 в браузере, используя консоль разработчика F12.
- откройте вкладку `Network`
- отправьте запрос http://stackoverflow.com
- найдите первый ответ HTTP сервера, откройте вкладку `Headers`
- укажите в ответе полученный HTTP код.
- проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?
- приложите скриншот консоли браузера в ответ.
```shell
GET	
scheme	https
host	stackoverflow.com
filename	/
Адрес	151.101.1.69:443
Состояние 200 OK
Версия HTTP/2
Передано51,97 КБ (размер 174,14 КБ)
``` 
[Homework_3.6](https://drive.google.com/drive/folders/1L8qDKrHzsj7bi6EWvVZEvEUoXIWTe7OX)
3. Какой IP адрес у вас в интернете?
```bash
$ curl https://ipecho.net/plain
95.131.149.246
 ```
4. Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой `whois`
```text
address:        Lovitel LLC


netname:        LEALTA-BB
descr:          Lealta LLC

```
5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`

6. Повторите задание 5 в утилите `mtr`. На каком участке наибольшая задержка - delay?

7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой `dig`

8. Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`

В качестве ответов на вопросы можно приложите лог выполнения команд в консоли или скриншот полученных результатов.
