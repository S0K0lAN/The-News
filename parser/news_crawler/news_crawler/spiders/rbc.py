import scrapy


class RbcSpider(scrapy.Spider):
    name = "rbc"
    allowed_domains = ["www.rbc.ru"]
    start_urls = ["https://www.rbc.ru/",
                  "https://www.rbc.ru/politics/",
                  "https://www.rbc.ru/sport/",
                  "https://www.rbc.ru/business/",
                  "https://www.rbc.ru/economics/",
                  "https://www.rbc.ru/crypto/"]
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Задержка 2 секунды между запросами
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': True,  # Соблюдать robots.txt
        'DEPTH_LIMIT': 2,  # Ограничить глубину обхода
    }

    def parse(self, response):
        print(response)