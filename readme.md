# Xiaomi Wifi Router Proxy translator
___

### For Russian description scroll below

Small proxy server based on `Flask` for translation of Xiaomi WiFi WebUI coming with Xiaomi routers known as using 
Chinese as the only language. 

Main features:

* translation to any language by just adding translated strings (currently only English and Russian are implemented)
* prevents tracking of user actions in WebUI (does not prevent from sending telemetry to Xiaomi)
* small footprint - Docker image is less than 75 Mb, idle RAM usage - ~54Mb, may probably run on Raspberry or other 
small computers as a separate service (not tested yet)
* ability to check the main language of browser and automatically provide proper translation; the user can change the 
language 'on the fly' by adding language code to URL

Current status of project:

* Desktop version: English translation >95% (hard to analyze, but most likely ~98%); Russian translation >80%
* Mobile version: English translation >80% (most likely >95%); Russian translation >25% (mobile has its own web app, and 
it is very glitchy and has limited functionality)
* Most of the screens are checked, but still may be some HTML formatting and CSS issues as well as grammar, spelling, 
syntax and not proper translations
* Tested on Xiaomi Redmi AC2100 router (firmware v.1.0.14 and v.2.0.23) and Chrome v.97 , Firefox v.96, Edge v.97; 
Android Chrome and Firefox

## Warnings and disclaimer

Do **NOT** use this proxy for firmware updates! The behavior was not tested.

Do **NOT** expose the port of this proxy to the internet as no type of security testing has been made

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Usage

The software acts just as a proxy and replaces Chinese strings in responses from the router. The proxy does not make any 
calls outside the router's address, so no leakage of any type of data is expected.

### Run locally from venv
```commandline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```
Open http://localhost:5000/ in browser 

### Run as a Docker container
```commandline
docker build -t miproxytranslator .
docker container run -d -p 5000:5000 miproxytranslator
```
You can restrict CPU and memory usage of the container if it is needed: 
```
docker container run --cpus="1" --memory="64m" -d -p 5000:5000 miproxytranslator
```
Open http://localhost:5000/ (or connect to the server where this container is running) in browser

### Setting up router's IP
Usually, Xiaomi router responds to miwifi.com address. Check if it works in your local network. This address is set up 
by default. If for any reason this does not work for you, the IP address of the router should be set up as an 
environment variable `MI_ROUTER_IP` before starting the server.

Locally in Windows you can do it by
```commandline
set MI_ROUTER_IP=192.168.1.1
```
in Linux
```commandline
MI_ROUTER_IP=192.168.1.1
```
To set it up in Docker image, uncomment the line in `Dockerfile`
```dockerfile
ENV MI_ROUTER_IP 192.168.1.1
```

### Setting up and changing translation language
By default, the language is English and the proxy checks the' Accept-Language' header in requests from the browser and 
provides the translation, if the **first** browser language is found in translations. Besides that, there are ways to 
explicitly set the language of translations:
* in URL: add `/en` or `/ru` (case sensitive) at the end of any URL and the language will be forced to this one.
* as an environment variable before starting the server `MI_ROUTER_TRANSLATION_LANG` (`en`, `ru` - case sensitive)
After setting the language by these 2 methods, checking browser language will not work. If for some reason is needed 
to restore it, add `/resetlang` at the end of any URL

## Описание на русском

Небольшой прокси-сервер, основанный на`Flask` для перевода веб-интерфейса роутеров Xiaomi, известных тем, что зачастую
идут исключительно с китайским языком.  


## Основные хар-ки:

* перевод на любой язык посредством добавления переведенных строк (на текущий момент сделаны только английский и русский)
* предотвражает отслеживание действий пользователя в веб-интерфейсе роутера (но не предотвращает от отсылки телеметрии 
 в Xiaomi)
* небольшой размер - образ Docker занимает менее 75 Мб, потребление памяти в простое - ~54Мб. Вероятно, может быть 
запущен на Raspberry или других небольших компьютерах как отдельный сервис (не проверялось)
* возможность проверки основного языка браузера и автоматически выдавать нужный язык перевода из имеющихся; пользователь
может изменить язык перевода "на лету" добавлением кода в адресную строку

## Текущее состояние проекта:

* Версия для настольных ПК: Перевод на английский >95% (сложно оценить, скорее всего ~98%); на русский >80%
* Версия для мобильных устройств: Перевод на английский >80% (скорее всего >95%); на русский >25% (мобильная версия 
 крайне глючная и имеет ограниченный функционал - ей лучше не пользоваться, даже напрямую с роутера)
* Большинство страниц проверены, но все еще могут быть проблемы с HTML форматированием и CSS, также могут быть 
грамматические, синтаксические и смысловые ошибки
* Проверялось на Xiaomi Redmi AC2100 роутер (ПО v.1.0.14 и v.2.0.23) и Chrome v.97, Firefox v.96, Edge v.97; Android 
Chrome и Firefox

## Предупреждения и отказ от обязательств

**НЕ** используйте прокси для обновления прошивки роутера! Тестирование не проводилось.

**НЕ** открывайте порт прокси во внешнюю сеть (Интернет) никаких тестов безопасности не проводилось.

ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ, ПОМИМО 
ПРОЧЕГО, ГАРАНТИИ КОММЕРЧЕСКОЙ ПРИГОДНОСТИ, ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННОЙ ЦЕЛИ И НЕНАРУШЕНИЯ ПРАВ. НИ ПРИ КАКИХ 
ОБСТОЯТЕЛЬСТВАХ АВТОРЫ ИЛИ ОБЛАДАТЕЛИ АВТОРСКОГО ПРАВА НЕ НЕСУТ ОТВЕТСТВЕННОСТЬ ПО ЛЮБЫМ ПРЕТЕНЗИЯМ, УЩЕРБАМ ИЛИ ДРУГОЙ 
ОТВЕТСТВЕННОСТИ, БУДЬ ТО В ДЕЙСТВИИ КОНТРАКТА, ДЕЛИКТА ИЛИ В ПРОТИВНОМ СЛУЧАЕ, ВОЗНИКАЮЩИЕ ИЗ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ 
ИЛИ В СВЯЗИ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ ИЛИ ИСПОЛЬЗОВАНИЕМ ИЛИ ДРУГИМИ ДЕЙСТВИЯМИ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ. 

## Использование

Программа всего лишь играет роль прокси-сервера и заменяет строки на китайском языке в ответах роутера. Прокси не делает
никаких вызовов, кроме как на адрес роутера, поэтому никаких утечек данных не должно происходить.

### Запуск локально в venv
```commandline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```
Откройте http://localhost:5000/ в браузере 

### Запуск как контейнер Docker
```commandline
docker build -t miproxytranslator .
docker container run -d -p 5000:5000 miproxytranslator
```
Вы можете ограничить использование CPU и памяти контейнером, если необходимо: 
```
docker container run --cpus="1" --memory="64m" -d -p 5000:5000 miproxytranslator
```
Откройте http://localhost:5000/ (или подключитесь к серверу, где контейнер запущен) в браузере

### Настройка IP адреса роутера
Обычно, роутеры Xiaomi откликаются на адрес miwifi.com в локальной сети. Проверьте, работает ли это в Вашей сети.
Это адрес забит по умолчанию в прокси. Если по каким-то причинам он не работает, необходимо принудительно задать
IP адрес роутера как переменную окружения `MI_ROUTER_IP` до запуска прокси

Локально в Windows это можно сделать как
```commandline
set MI_ROUTER_IP=192.168.1.1
```
в Linux
```commandline
MI_ROUTER_IP=192.168.1.1
```
Для того чтобы установить в Docker, раскомментируйте строку в `Dockerfile`
```dockerfile
ENV MI_ROUTER_IP 192.168.1.1
```

### Установка и изменение языка перевода
По умолчанию, язык - английский и прокси проверяет заголовок в 'Accept-Language' в запросах браузера и выдает перевод,  
если **первый** язык браузера есть в переводе. Кроме этого, существуют еще способы принудительного задания языка:
* в адресной строке: добавьте `/en` или `/ru` (строчные буквы) в конце любого адреса и язык принудительно переключится 
на заданный.
* как переменную окружения `MI_ROUTER_TRANSLATION_LANG` до запуска сервереа (`en`, `ru` - строчными буква, см. выше)
После задания языка этими двуми способами, проверка языка браузера работать не будет. Если по каким-то причинам ее 
нужно опять включить, добавьте `/resetlang` в конец адресной строки 
