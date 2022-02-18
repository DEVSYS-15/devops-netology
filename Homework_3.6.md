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

origin:         AS41275
netname:        LEALTA-BB
descr:          Lealta LLC

```
5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`
````bash
    traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
     1  172.17.2.1 [*]  0.209 ms  0.161 ms  0.134 ms
     2  95.131.149.1 [AS41275]  1.870 ms  1.845 ms  1.861 ms
     3  89.207.216.16 [AS41275]  1.376 ms 89.207.216.18 [AS41275]  1.351 ms  1.327 ms
     4  142.250.160.102 [AS15169]  2.135 ms  2.229 ms  2.064 ms
     5  * * *
     6  108.170.227.82 [AS15169]  1.361 ms 108.170.250.129 [AS15169]  2.469 ms 108.170.226.164 [AS15169]  1.629 ms
     7  108.170.250.34 [AS15169]  2.069 ms 108.170.250.51 [AS15169]  2.014 ms  1.977 ms
     8  * 209.85.255.136 [AS15169]  19.420 ms 142.251.49.158 [AS15169]  14.286 ms
     9  74.125.253.109 [AS15169]  37.797 ms 209.85.254.20 [AS15169]  15.312 ms 74.125.253.109 [AS15169]  36.330 ms
    10  216.239.46.139 [AS15169]  15.144 ms 216.239.57.5 [AS15169]  14.142 ms 72.14.236.73 [AS15169]  18.440 ms
    11  * * *
    12  * * *
    13  * * *
    14  * * *
    15  * * *
    16  * * *
    17  * * *
    18  * * *
    19  * * *
    20  8.8.8.8 [AS15169]  15.588 ms  16.741 ms  15.051 ms
````

6. Повторите задание 5 в утилите `mtr`. На каком участке наибольшая задержка - delay?
```bash
(172.17.2.240)                                                                           2022-02-19T00:45:13+0300
Keys:  Help   Display mode   Restart statistics   Order of fields   quit
                                                                            Packets               Pings
 Host                                                                     Loss%   Snt   Last   Avg  Best  Wrst StDev
 1. AS???    172.17.2.1                                                    0.0%     5    0.3   0.3   0.3   0.3   0.0
 2. AS41275  95.131.149.1                                                  0.0%     5    1.2   1.1   1.0   1.2   0.1
 3. AS41275  89.207.216.16                                                 0.0%     5    1.4   1.5   1.3   2.1   0.3
 4. AS15169  142.250.160.102                                               0.0%     5    2.2   2.2   2.2   2.3   0.1
 5. AS15169  108.170.250.33                                                0.0%     5    2.8   2.7   2.5   3.2   0.3
 6. AS15169  108.170.250.34                                                0.0%     5    2.3   2.4   2.3   2.4   0.1
 7. AS15169  142.251.49.24                                                 0.0%     5   14.0  14.2  14.0  14.3   0.1
 8. AS15169  108.170.235.64                                                0.0%     5   16.7  16.6  16.4  17.0   0.3
 9. AS15169  172.253.51.247                                                0.0%     4   17.5  17.3  16.7  17.7   0.4
10. ???
11. ???
12. ???
13. ???
14. ???
15. ???
16. ???
17. ???
18. ???
19. AS15169  8.8.8.8                                                       0.0%     4   13.8  14.3  13.8  15.7   0.9

```

7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой `dig`
  ```bash
      dig  dns.goggle.com
        
        ; <<>> DiG 9.16.6 <<>> dns.goggle.com
        ;; global options: +cmd
        ;; Got answer:
        ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 34940
        ;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 13, ADDITIONAL: 1
        
        ;; QUESTION SECTION:
        ;dns.goggle.com.			IN	A
        
        ;; ANSWER SECTION:
       * dns.goggle.com.		214	IN	A	162.242.150.89
       * dns.goggle.com.		269	IN	A	176.34.241.253
       * dns.goggle.com.		269	IN	A	23.253.58.227
        
        ;; AUTHORITY SECTION:
        com.			7081	IN	NS	l.gtld-servers.net.
        com.			7081	IN	NS	a.gtld-servers.net.
        com.			7081	IN	NS	f.gtld-servers.net.
        com.			7081	IN	NS	j.gtld-servers.net.
        com.			7081	IN	NS	e.gtld-servers.net.
        com.			7081	IN	NS	i.gtld-servers.net.
        com.			7081	IN	NS	k.gtld-servers.net.
        com.			7081	IN	NS	d.gtld-servers.net.
        com.			7081	IN	NS	b.gtld-servers.net.
        com.			7081	IN	NS	g.gtld-servers.net.
        com.			7081	IN	NS	m.gtld-servers.net.
        com.			7081	IN	NS	c.gtld-servers.net.
        com.			7081	IN	NS	h.gtld-servers.net.
        
        ;; ADDITIONAL SECTION:
        a.gtld-servers.net.	15960	IN	A	192.5.6.30
        
        ;; Query time: 188 msec
        ;; SERVER: 172.17.2.1#53(172.17.2.1)
        ;; WHEN: Sat Feb 19 00:53:12 MSK 2022
        ;; MSG SIZE  rcvd: 320

   

   ```
8. Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`
```bash
    dig -x 176.34.241.253

        ; <<>> DiG 9.16.6 <<>> -x 176.34.241.253
        ;; global options: +cmd
        ;; Got answer:
        ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2229
        ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
        
        ;; QUESTION SECTION:
        ;253.241.34.176.in-addr.arpa.	IN	PTR
        
        ;; ANSWER SECTION:
        253.241.34.176.in-addr.arpa. 227 IN	PTR	ns2.uniregistry-dns.net.
        
        ;; Query time: 80 msec
        ;; SERVER: 172.17.2.1#53(172.17.2.1)
        ;; WHEN: Sat Feb 19 01:06:56 MSK 2022
        ;; MSG SIZE  rcvd: 82
        
    dig -x 23.253.58.227
        
        ; <<>> DiG 9.16.6 <<>> -x 23.253.58.227
        ;; global options: +cmd
        ;; Got answer:
        ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64696
        ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
        
        ;; QUESTION SECTION:
        ;227.58.253.23.in-addr.arpa.	IN	PTR
        
        ;; ANSWER SECTION:
        227.58.253.23.in-addr.arpa. 814	IN	PTR	ns1.uniregistry-dns.net.
        
        ;; Query time: 180 msec
        ;; SERVER: 172.17.2.1#53(172.17.2.1)
        ;; WHEN: Sat Feb 19 01:08:35 MSK 2022
        ;; MSG SIZE  rcvd: 81
        
    dig -x 162.242.150.89

        ; <<>> DiG 9.16.6 <<>> -x 162.242.150.89
        ;; global options: +cmd
        ;; Got answer:
        ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 63359
        ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
        
        ;; QUESTION SECTION:
        ;89.150.242.162.in-addr.arpa.	IN	PTR
        
        ;; ANSWER SECTION:
        89.150.242.162.in-addr.arpa. 462 IN	PTR	ns2.uniregistry-dns.com.
        
        ;; Query time: 480 msec
        ;; SERVER: 172.17.2.1#53(172.17.2.1)
        ;; WHEN: Sat Feb 19 01:10:26 MSK 2022
        ;; MSG SIZE  rcvd: 82
        

   
   ```
    
В качестве ответов на вопросы можно приложите лог выполнения команд в консоли или скриншот полученных результатов.
