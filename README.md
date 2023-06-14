![BeautifulSoupLogo](https://sixfeetup.com/blog/an-introduction-to-beautifulsoup/@@images/27e8bf2a-5469-407e-b84d-5cf53b1b0bb6.png)

# Домашнє завдання #9 (Основне завдання)

Виконується скрапінг[^1] сайту http://quotes.toscrape.com за допомогою бібліотеки [`Beautiful Soup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

[^1]: Web-скрапінг (англ. web scraping) - це автоматизований процес видобування даних з web-сайтів.

## Установка проекту

Для управління залежностями проекту використовується `pipenv`. Необхідно встановити `pipenv` перед виконанням наступних кроків:

- Склонируйте репозиторий:

  ```shell
  git clone https://github.com/sergiokapone/goit_python_web_hw9_bs4_.git
  ```

- Для встановлення залежностей використайте команду `pipenv install` або `pipenv sync`.

## Запуск скрапінгу

Скрапінг виконується за допомогою бібліотеки `Beautiful Soup` і відбувається в асинхронному режимі з використанням бібліотек `aiohttp`, `asyncio`.

Для виконання скрапінгу запустіть скрипт

```shell
python scrap.py
```

В результаті виконання скрипта створюються (або перезаписуються) два файли

- `qoutes.json` містить що містить інформацію про цитати з усіх сторінок сайту;
- `authors.json` що містить інформацію про авторів зазначених цитат.

## Завантаження даних в базу `MongoDB`

Для завантаження даних в базу запустіть скрипт

```shell
python upload.py
```

В результаті виконання скрипта інформація, що містилась в файлах `qoutes.json` та `authors.json` запишеться в базу даних.
